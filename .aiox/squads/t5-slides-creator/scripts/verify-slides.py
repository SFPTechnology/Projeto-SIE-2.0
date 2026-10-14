#!/usr/bin/env python3
"""
verify-slides.py — Technical smoke test for rendered slide decks.

Complement to qa-inspector (which does PPTEval/GAD/narrative scoring).
This script is purely technical: does HTML open? Does JS run without errors?
Does layout hold across viewports? Are there console warnings?

Not a design/content check. Run BEFORE qa-inspector to catch technical
breakage that would invalidate any subsequent design review.

Usage:
    python verify-slides.py path/to/deck.html
    python verify-slides.py path/to/index.html --slides 10
    python verify-slides.py deck.html --viewports 1920x1080,768x1024,375x667
    python verify-slides.py deck.html --output /tmp/screenshots
    python verify-slides.py deck.html --show  # non-headless, keep browser open

Dependencies:
    pip install playwright
    playwright install chromium

Output:
    - Screenshots in output_dir (default: {html_dir}/verify-screenshots/)
    - verify-report.yaml with pass/fail verdict + errors
    - Exit code 0 on pass, 1 on fail

Integration:
    qa-inspector's *run-killer-gate can shell out to this script
    for SCALE-* and technical smoke checks before PPTEval.
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime


def parse_viewport(s):
    """Parse WxH string into dict."""
    try:
        w, h = s.split('x')
        return {'width': int(w), 'height': int(h)}
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid viewport format: '{s}' (expected WIDTHxHEIGHT)")


def verify_html(
    html_path,
    viewports=None,
    slides=0,
    output_dir=None,
    show=False,
    wait_ms=2000,
    report_path=None,
):
    """
    Verify HTML rendering + capture screenshots + collect errors.
    Returns: 0 on pass, 1 on fail.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.")
        print("Run: pip install playwright && playwright install chromium")
        return 2

    html_path = Path(html_path).resolve()
    if not html_path.exists():
        print(f"ERROR: HTML file does not exist: {html_path}")
        return 2

    # Output dir setup
    if output_dir is None:
        output_dir = html_path.parent / 'verify-screenshots'
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if report_path is None:
        report_path = html_path.parent / 'verify-report.yaml'

    file_url = html_path.as_uri()
    stem = html_path.stem

    if viewports is None:
        viewports = [{'width': 1920, 'height': 1080}]

    # Collectors
    console_errors = []
    console_warnings = []
    page_errors = []
    screenshots_taken = []

    report = {
        'script': 'verify-slides.py',
        'html_file': str(html_path),
        'verified_at': datetime.utcnow().isoformat() + 'Z',
        'viewports_tested': viewports,
        'slide_mode': slides > 0,
        'results_per_viewport': [],
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not show)

        for viewport in viewports:
            vp_label = f"{viewport['width']}x{viewport['height']}"
            print(f"\n→ Testing at {vp_label}")

            context = browser.new_context(
                viewport=viewport,
                device_scale_factor=2,  # retina for cleaner screenshots
            )
            page = context.new_page()

            # Hook error collectors
            vp_console_errors = []
            vp_console_warnings = []
            vp_page_errors = []

            def handle_console(msg, errors=vp_console_errors, warnings=vp_console_warnings):
                if msg.type == 'error':
                    errors.append(f"[{vp_label}] {msg.text}")
                elif msg.type == 'warning':
                    warnings.append(f"[{vp_label}] {msg.text}")

            def handle_pageerror(err, errors=vp_page_errors):
                errors.append(f"[{vp_label}] {str(err)}")

            page.on('console', handle_console)
            page.on('pageerror', handle_pageerror)

            # Navigate + wait
            page.goto(file_url, wait_until='networkidle')
            page.wait_for_timeout(wait_ms)

            vp_result = {
                'viewport': vp_label,
                'console_errors': len(vp_console_errors),
                'console_warnings': len(vp_console_warnings),
                'page_errors': len(vp_page_errors),
                'error_details': vp_page_errors + vp_console_errors[:10],
                'screenshots': [],
            }

            # Slide mode: traverse deck by pressing ArrowRight
            if slides > 0:
                for i in range(slides):
                    sc_name = f"{stem}-vp{vp_label}-slide-{str(i + 1).zfill(2)}.png"
                    sc_path = output_dir / sc_name
                    page.screenshot(path=str(sc_path), full_page=False)
                    vp_result['screenshots'].append(sc_name)
                    screenshots_taken.append(str(sc_path))
                    print(f"  ✓ slide {i + 1} → {sc_name}")

                    if i < slides - 1:
                        page.keyboard.press('ArrowRight')
                        page.wait_for_timeout(500)  # let transition settle

            # Single-page mode
            else:
                sc_name = f"{stem}-vp{vp_label}.png"
                sc_path = output_dir / sc_name
                page.screenshot(path=str(sc_path), full_page=False)
                vp_result['screenshots'].append(sc_name)
                screenshots_taken.append(str(sc_path))

                full_name = f"{stem}-vp{vp_label}-full.png"
                full_path = output_dir / full_name
                page.screenshot(path=str(full_path), full_page=True)
                vp_result['screenshots'].append(full_name)
                screenshots_taken.append(str(full_path))
                print(f"  ✓ screenshot → {sc_name} (+ full-page)")

            # Aggregate
            console_errors.extend(vp_console_errors)
            console_warnings.extend(vp_console_warnings)
            page_errors.extend(vp_page_errors)

            report['results_per_viewport'].append(vp_result)

            if show:
                print(f"  (browser kept open — press Enter to close this viewport)")
                input()

            context.close()

        browser.close()

    # Final report
    total_page_errors = len(page_errors)
    total_console_errors = len(console_errors)
    total_console_warnings = len(console_warnings)

    report['total_page_errors'] = total_page_errors
    report['total_console_errors'] = total_console_errors
    report['total_console_warnings'] = total_console_warnings
    report['screenshots_total'] = len(screenshots_taken)
    report['verdict'] = 'PASS' if total_page_errors == 0 else 'FAIL'

    # Write report (simple YAML-ish — no external yaml dep)
    report_lines = []
    for key, value in report.items():
        if key in ('error_details', 'results_per_viewport'):
            continue  # nested, handle below
        report_lines.append(f"{key}: {json.dumps(value) if not isinstance(value, (str, int)) else value}")

    report_lines.append("results_per_viewport:")
    for vp_result in report['results_per_viewport']:
        report_lines.append(f"  - viewport: {vp_result['viewport']}")
        report_lines.append(f"    page_errors: {vp_result['page_errors']}")
        report_lines.append(f"    console_errors: {vp_result['console_errors']}")
        report_lines.append(f"    console_warnings: {vp_result['console_warnings']}")
        if vp_result['error_details']:
            report_lines.append(f"    error_details:")
            for err in vp_result['error_details']:
                report_lines.append(f"      - {json.dumps(err)}")
        report_lines.append(f"    screenshots_count: {len(vp_result['screenshots'])}")

    report_path = Path(report_path)
    report_path.write_text('\n'.join(report_lines) + '\n')

    # Console output
    print("\n" + "=" * 60)
    print("VERIFY REPORT")
    print("=" * 60)
    print(f"HTML file:              {html_path}")
    print(f"Viewports tested:       {len(viewports)}")
    print(f"Screenshots captured:   {len(screenshots_taken)}")
    print(f"Page errors (JS/throw): {total_page_errors}")
    print(f"Console errors:         {total_console_errors}")
    print(f"Console warnings:       {total_console_warnings}")
    print(f"Report saved:           {report_path}")
    print(f"Screenshots dir:        {output_dir}")

    if total_page_errors > 0:
        print(f"\n❌ PAGE ERRORS ({total_page_errors}):")
        for e in page_errors[:20]:
            print(f"  - {e}")
        if total_page_errors > 20:
            print(f"  ... and {total_page_errors - 20} more")

    if total_console_errors > 0:
        print(f"\n⚠️  CONSOLE ERRORS ({total_console_errors}):")
        for e in console_errors[:10]:
            print(f"  - {e}")
        if total_console_errors > 10:
            print(f"  ... and {total_console_errors - 10} more")

    print("\n" + "=" * 60)
    if total_page_errors == 0:
        print("✅ VERDICT: PASS (no page errors)")
    else:
        print("❌ VERDICT: FAIL (page errors present, must fix before release)")
    print("=" * 60)

    return 0 if total_page_errors == 0 else 1


def main():
    parser = argparse.ArgumentParser(
        description="Verify rendered HTML deck via Playwright (technical smoke test)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python verify-slides.py outputs/slides-creator/aiox/Q3-review/index.html
  python verify-slides.py deck.html --slides 10
  python verify-slides.py deck.html --viewports 1920x1080,768x1024
  python verify-slides.py deck.html --output /tmp/ss --show
""",
    )
    parser.add_argument("html_path", help="HTML file to verify (deck.html or index.html)")
    parser.add_argument(
        "--viewports",
        default="1920x1080",
        help="Comma-separated viewports WxH (default: 1920x1080)",
    )
    parser.add_argument(
        "--slides",
        type=int,
        default=0,
        help="Slide mode: screenshot first N slides by pressing ArrowRight (default: 0 = single page)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output directory for screenshots (default: {html_dir}/verify-screenshots/)",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Report file path (default: {html_dir}/verify-report.yaml)",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Non-headless mode: open real browser, wait after each viewport",
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=2000,
        help="Milliseconds to wait after page load before screenshot (default: 2000)",
    )

    args = parser.parse_args()

    try:
        viewports = [parse_viewport(v) for v in args.viewports.split(",")]
    except ValueError as e:
        print(f"ERROR: {e}")
        return 2

    return verify_html(
        html_path=args.html_path,
        viewports=viewports,
        slides=args.slides,
        output_dir=args.output,
        show=args.show,
        wait_ms=args.wait,
        report_path=args.report,
    )


if __name__ == "__main__":
    sys.exit(main())
