#!/usr/bin/env python3
"""Archive only bounded, redacted CLI streams; never environment or session files."""
import argparse
import os
from pathlib import Path
import re

LIMIT = 16384

def sanitize(text, secrets=()):
    text = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', text)
    for value in secrets:
        if value:
            text = text.replace(value, '[REDACTED]')
    text = re.sub(r'(?is)-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----', '[REDACTED PRIVATE KEY]', text)
    text = re.sub(r'(?i)\b(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]+', '[REDACTED TOKEN]', text)
    text = re.sub(r'(?i)(authorization\s*[:=]\s*)(?:basic\s+|bearer\s+|token\s+)?[^\s,;]+', r'\1[REDACTED]', text)
    text = re.sub(r'(?i)((?:token|secret|password|api[_-]?key)\s*[=:]\s*)[^\s,;]+', r'\1[REDACTED]', text)
    # Redact before truncation so long credentials cannot leave partial prefixes.
    return text[:LIMIT] + ('\n[TRUNCATED]\n' if len(text) > LIMIT else '')

def collect(root, secret=''):
    out = root / 'sanitized'
    out.mkdir(parents=True, exist_ok=True)
    for name in ('raw.stdout', 'raw.stderr', 'version.txt', 'exit-code.txt'):
        src = root / name
        # No recursion and no session, config, env or arbitrary directory uploads.
        value = src.read_text(errors='replace') if src.is_file() and not src.is_symlink() else '[NOT AVAILABLE]\n'
        target = name.replace('raw.', '')
        (out / target).write_text(sanitize(value, (secret,)), encoding='utf-8')
    (out / 'NOTICE.txt').write_text('Sanitized bounded execution diagnostics only. Not a QA report, evidence approval or normative signoff. No session/config/environment files collected.\n')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, required=True)
    args = p.parse_args()
    collect(args.root, os.environ.get('COPILOT_GITHUB_TOKEN', ''))
