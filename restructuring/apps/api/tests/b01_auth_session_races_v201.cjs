const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../../web/auth-v201.js'), 'utf8');
const deferred = () => { let resolve; const promise = new Promise(r => resolve = r); return {promise, resolve}; };
const response = (data, ok = true) => ({ok, json: async () => data});
const session = {access_token: 'synthetic_access_token_for_tests', refresh_token: 'synthetic_refresh', expires_in: 3600};
const identity = {user_id: 'fixture-A', authorization_source: 'auth_server_verified'};
function harness() {
  const elements = new Map();
  const timers = new Map(); let timerId = 0;
  const document = {hidden: false, addEventListener() {}, getElementById(id) {
    if (!elements.has(id)) elements.set(id, {hidden: id === 'signed-in', value: '', textContent: '', addEventListener() {}});
    return elements.get(id);
  }};
  const ctx = vm.createContext({document, location: {origin: 'http://127.0.0.1:5173'},
    window: {SIE_V201_PUBLIC_CONFIG: {supabaseUrl: 'https://fozrymsidnaxmuvxxfhh.supabase.co',
      publishableKey: 'sb_publishable_fixture', apiBase: 'http://127.0.0.1:8000'}},
    setTimeout(fn) {timers.set(++timerId, fn); return timerId;}, clearTimeout(id) {timers.delete(id);},
    fetch: async url => response(url.includes('/auth/me') ? identity : session)});
  vm.runInContext(source, ctx);
  return {ctx, elements, timers, run: code => vm.runInContext(code, ctx)};
}
(async () => {
  // A login finishing after logout must never reactivate the local session.
  {
    const h = harness(); const wait = deferred();
    h.ctx.fetch = async url => url.includes('grant_type=password') ? wait.promise : response(identity);
    const login = h.run('signIn("fixture@example.invalid", "synthetic")');
    const rejected = assert.rejects(login, /superseded/);
    await h.run('signOut()'); wait.resolve(response(session)); await rejected;
    assert.equal(h.run('accessToken'), null);
    assert.equal(h.elements.get('signed-in').hidden, true);
  }
  // A timer refresh from A finishing after a new login B must not clear B.
  {
    const h = harness(); await h.run('signIn("a@example.invalid", "synthetic")');
    const wait = deferred();
    h.ctx.fetch = async url => url.includes('grant_type=refresh_token') ? wait.promise : response(identity);
    [...h.timers.values()][0]();
    await h.run('signOut()');
    h.ctx.fetch = async url => response(url.includes('/auth/me') ? {...identity, user_id:'fixture-B'} : session);
    await h.run('signIn("b@example.invalid", "synthetic")');
    wait.resolve(response(session));
    for(let i=0;i<12;i++) await Promise.resolve();
    assert.equal(h.run('verifiedUserId'), 'fixture-B');
    assert.equal(h.elements.get('signed-in').hidden, false);
  }
  // HTTP rejection is not proof of remote revocation; local tokens still clear.
  for (const ok of [false, true]) {
    const h = harness(); await h.run('signIn("a@example.invalid", "synthetic")');
    h.ctx.fetch = async () => response({}, ok);
    await h.run('signOut()');
    assert.equal(h.run('accessToken'), null);
    assert.equal(h.run('refreshToken'), null);
    assert.match(h.elements.get('status').textContent, ok ? /Tokens anteriores/ : /não foi possível confirmar revogação/);
  }
  console.log('PASS: login/logout race, stale refresh isolation, HTTP logout failure/success');
})().catch(error => { console.error(error); process.exitCode = 1; });
