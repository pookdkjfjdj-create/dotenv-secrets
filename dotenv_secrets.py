#!/usr/bin/env python3
"""dotenv-secrets -- generate, validate, and manage .env files for secure development."""

from __future__ import annotations

import os
import pathlib
import re
import secrets
import string
import sys

_VALID_KEY = re.compile(r'^[A-Z_][A-Z0-9_]*$')


def _looks_like_real_secret(key: str, val: str) -> bool:
    if len(val) < 16:
        return False
    charset = set(val)
    if len(charset) > 15 and len(val) > 20:
        dangerous = ('sk-', 'ghp_', 'xox', 'AKIA', 'AIza', 'ey')
        if any(val.startswith(p) for p in dangerous):
            return True
    return False


def validate(env_path: str | pathlib.Path = '.env') -> tuple[int, list[str]]:
    p = pathlib.Path(env_path)
    if not p.exists():
        return 1, [f'File {p} does not exist']
    errors: list[str] = []
    for i, line in enumerate(p.read_text().splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if '=' not in stripped:
            errors.append(f'  line {i}: no "=" found ("{stripped[:40]}")')
            continue
        key = stripped.split('=', 1)[0].strip()
        val = stripped.split('=', 1)[1].strip()
        if not _VALID_KEY.match(key):
            errors.append(f'  line {i}: key {key!r} does not match [A-Z_][A-Z0-9_]*')
        if not val:
            errors.append(f'  line {i}: key {key!r} has empty value')
        if _looks_like_real_secret(key, val):
            errors.append(
                f'  line {i}: key {key!r} contains what looks like a real secret -- use a placeholder'
            )
    return 0, errors


def generate_secret(length: int = 32) -> str:
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*()-_=+'
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_template(keys: str, output: str = '.env') -> None:
    pathlib.Path(output).write_text(
        '# Template -- replace placeholders with real values\n'
        + '\n'.join(f'{k.strip()}=' for k in keys.split(',') if k.strip())
        + '\n',
    )
    print(f'Template written to {output}')


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h'):
        print('Usage:')
        print('  python -m dotenv_secrets validate [.env]')
        print('  python -m dotenv_secrets template KEY1,KEY2,... [output]')
        print('  python -m dotenv_secrets secret [length]')
        return
    cmd = sys.argv[1]
    if cmd == 'validate':
        path = sys.argv[2] if len(sys.argv) > 2 else '.env'
        code, errs = validate(path)
        print(f'Validating {path}...')
        if not errs:
            print('  All OK -- no secrets or formatting issues found')
        else:
            for e in errs:
                print(e)
        sys.exit(code)
    elif cmd == 'template':
        create_template(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '.env')
    elif cmd == 'secret':
        length = int(sys.argv[2]) if len(sys.argv) > 2 else 32
        print(generate_secret(length))
    else:
        print(f'Unknown command: {cmd}')
        sys.exit(1)


if __name__ == '__main__':
    main()
