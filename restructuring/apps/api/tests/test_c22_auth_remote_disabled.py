"""C22: real Supabase Auth requires an explicit opt-in; default is synthetic-only."""
from pathlib import Path
import subprocess


def test_default_browser_config_blocks_remote_auth_before_fetch():
    script = Path(__file__).with_name("c22_auth_remote_disabled.cjs")
    completed = subprocess.run(["node", str(script)], check=True, capture_output=True, text=True)
    assert "PASS: default Auth configuration blocks every remote call" in completed.stdout


def test_real_auth_opt_in_is_strict_boolean_not_truthy_text():
    source = (Path(__file__).resolve().parents[2] / "web" / "auth-v201.js").read_text(encoding="utf-8")
    assert "cfg.allowRealAuth !== true" in source
    assert "SYNTHETIC_ONLY" in source
