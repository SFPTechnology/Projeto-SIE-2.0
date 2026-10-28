"""B01 isolated browser auth UI smoke, synthetic transport only.

NEVER logs in to a real Supabase user; all outbound Auth calls are intercepted.
"""
import os
from playwright.sync_api import expect, sync_playwright
from test_browser_flow import servers, WEB_URL

AUTH_URL="https://fozrymsidnaxmuvxxfhh.supabase.co"


def test_b01_default_config_fails_closed_in_real_browser(servers):
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        page=browser.new_page()
        outbound=[]
        page.route(AUTH_URL+"/**",lambda route: (outbound.append(route.request.url),route.abort()))
        page.goto(WEB_URL+"/auth-v201.html",wait_until="networkidle")
        expect(page.get_by_role("heading",name="Acesso aos projetos")).to_be_visible()
        expect(page.locator("#status")).to_contain_text("chave pública")
        page.locator("#email").fill("fixture@example.invalid")
        page.locator("#password").fill("notarealpassword")
        page.locator("#login").click()
        expect(page.locator("#status")).to_contain_text("Não foi possível autenticar")
        assert outbound==[]
        assert page.evaluate("localStorage.length")==0
        assert page.evaluate("sessionStorage.length")==0
        browser.close()


def test_b01_synthetic_login_backend_check_and_logout(servers):
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        page=browser.new_page()
        outbound=[]
        page.route("**/auth-v201.public-config.js",lambda route:route.fulfill(
            status=200,content_type="application/javascript",
            body='window.SIE_V201_PUBLIC_CONFIG={supabaseUrl:"'+AUTH_URL+
            '",publishableKey:"sb_publishable_test_only",apiBase:"http://127.0.0.1:8000"}'))
        cors={"access-control-allow-origin":"*",
              "access-control-allow-methods":"GET,POST,OPTIONS",
              "access-control-allow-headers":"apikey,authorization,content-type"}
        def fake_token(route):
            if route.request.method=="OPTIONS":
                return route.fulfill(status=204,headers=cors)
            outbound.append("login")
            route.fulfill(status=200,content_type="application/json",
                         body='{"access_token":"synthetic_bearer_for_browser_e2e_only"}',
                         headers=cors)
        page.route(AUTH_URL+"/auth/v1/token?grant_type=password",fake_token)
        def fake_me(route):
            if route.request.method=="OPTIONS":
                return route.fulfill(status=204,headers=cors)
            auth=route.request.headers.get("authorization","")
            assert auth=="Bearer synthetic_bearer_for_browser_e2e_only"
            outbound.append("verified-api")
            route.fulfill(status=200,content_type="application/json",
                         body='{"user_id":"11111111-1111-4111-8111-111111111111",'+
                         '"authorization_source":"auth_server_verified"}',
                         headers={"access-control-allow-origin":"*"})
        page.route("http://127.0.0.1:8000/api/v2/sie/auth/me",fake_me)
        page.route(AUTH_URL+"/auth/v1/logout?scope=local",lambda route:route.fulfill(
            status=204,headers={"access-control-allow-origin":"*"}))
        page.goto(WEB_URL+"/auth-v201.html",wait_until="networkidle")
        expect(page.locator("#status")).to_contain_text("Configuração pública pronta")
        page.locator("#email").fill("a@example.invalid")
        page.locator("#password").fill("synthetic-pass-123")
        page.locator("#login").click()
        expect(page.locator("#signed-in")).to_be_visible()
        assert outbound==["login","verified-api"]
        assert page.evaluate("localStorage.length")==0
        assert page.evaluate("sessionStorage.length")==0
        page.locator("#logout").click()
        expect(page.locator("#login-form")).to_be_visible()
        assert page.locator("#password").input_value()==""
        browser.close()
