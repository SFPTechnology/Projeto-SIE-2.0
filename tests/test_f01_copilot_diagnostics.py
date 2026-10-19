import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('diag', ROOT / 'scripts/f01_copilot_diagnostics.py')
diag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diag)

class DiagnosticsTests(unittest.TestCase):
    def test_redacts_before_bounding(self):
        secret = 'github_pat_' + 'x' * 30000
        result = diag.sanitize('Authorization: Bearer abc\nghp_ABC123 token=abc\n' + secret, [secret])
        self.assertNotIn(secret, result)
        self.assertNotIn('abc', result)
        self.assertNotIn('ghp_ABC123', result)
        self.assertLess(len(result), diag.LIMIT)

    def test_basic_auth_and_ansi_secret(self):
        result = diag.sanitize('Authorization: Basic abc123\nauthorization: basic def456\nse\x1b[31mcret', ['secret'])
        for value in ('abc123', 'def456', 'secret'):
            self.assertNotIn(value, result)

    def test_whitelist_only_missing_streams_and_no_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'raw.stdout').write_text('secret-value')
            (root / 'session.json').write_text('DO NOT ARCHIVE')
            diag.collect(root, 'secret-value')
            out = root / 'sanitized'
            self.assertEqual(set(p.name for p in out.iterdir()), {'stdout', 'stderr', 'version.txt', 'exit-code.txt', 'NOTICE.txt'})
            self.assertEqual((out / 'stdout').read_text(), '[REDACTED]')
            self.assertIn('NOT AVAILABLE', (out / 'stderr').read_text())

    def test_limit_and_symlink_rejection(self):
        self.assertIn('TRUNCATED', diag.sanitize('x' * 20000))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'secret').write_text('do-not-follow')
            (root / 'raw.stdout').symlink_to(root / 'secret')
            diag.collect(root)
            self.assertIn('NOT AVAILABLE', (root / 'sanitized/stdout').read_text())

if __name__ == '__main__':
    unittest.main()
