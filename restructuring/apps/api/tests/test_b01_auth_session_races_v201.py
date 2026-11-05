"""Execute production browser JS with deterministic synthetic HTTP, no live Auth."""
from pathlib import Path
import subprocess


def test_browser_auth_async_session_isolation():
    script = Path(__file__).with_name("b01_auth_session_races_v201.cjs")
    subprocess.run(["node", str(script)], check=True, capture_output=True, text=True)
