import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('diag', ROOT / 'scripts/f01_copilot_diagnostics.py')
diag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diag)
audit_spec = importlib.util.spec_from_file_location('audit', ROOT / 'scripts/f01_qa_workflow_audit.py')
audit = importlib.util.module_from_spec(audit_spec)
audit_spec.loader.exec_module(audit)

class DiagnosticsTests(unittest.TestCase):
    def test_smoke_alternative_writer_is_required(self):
        source = (ROOT / '.github/workflows/f01-copilot-qa-isolated.yml').read_text()
        self.assertTrue(audit.check(source)['safe_static_configuration'])
        mutant = source.replace("--available-tools='view,create,edit,apply_patch'", "--available-tools='view,create,edit'")
        self.assertFalse(audit.check(mutant)['safe_static_configuration'])

    def test_profiles_require_literal_alternative_writers_without_execute(self):
        profiles = {name: (ROOT / '.github/agents' / (name + '.agent.md')).read_text() for name in audit.AGENTS}
        self.assertEqual(audit.check_profiles(profiles), [])
        for name in audit.AGENTS:
            mutant = dict(profiles)
            mutant[name] = mutant[name].replace("'apply_patch', ", '')
            self.assertTrue(audit.check_profiles(mutant))
            mutant[name] = profiles[name].replace("'skill']", "'skill', 'execute']")
            self.assertTrue(audit.check_profiles(mutant))

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
