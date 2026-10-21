"""SQLite local lifecycle; no production migration or in-place restore."""
import os
import sqlite3
from pathlib import Path

UP = (
    'ALTER TABLE projetos ADD COLUMN criado_em TEXT',
    'ALTER TABLE projetos ADD COLUMN excluido_em TEXT',
    'UPDATE projetos SET criado_em=atualizado_em',
    "ALTER TABLE eventos_auditoria ADD COLUMN autor TEXT NOT NULL DEFAULT 'LEGACY_UNKNOWN' CHECK(autor IN ('LOCAL_OWNER','LEGACY_UNKNOWN'))",
    'CREATE INDEX f03_ativos ON projetos(excluido_em)',
)
DOWN = (
    'DROP INDEX f03_ativos',
    'ALTER TABLE eventos_auditoria DROP COLUMN autor',
    'ALTER TABLE projetos DROP COLUMN excluido_em',
    'ALTER TABLE projetos DROP COLUMN criado_em',
)


def migrate(db, target=1):
    if target not in (0, 1):
        raise ValueError('Versao desconhecida')
    db.execute('BEGIN IMMEDIATE')
    try:
        db.execute('CREATE TABLE IF NOT EXISTS schema_migrations(version INTEGER PRIMARY KEY CHECK(version=1))')
        version = db.execute('SELECT coalesce(max(version),0) FROM schema_migrations').fetchone()[0]
        if version == 0 and target == 1:
            for sql in UP:
                db.execute(sql)
            db.execute('INSERT INTO schema_migrations VALUES(1)')
        elif version == 1 and target == 0:
            if db.execute('SELECT 1 FROM projetos WHERE excluido_em IS NOT NULL LIMIT 1').fetchone():
                raise ValueError('Downgrade perderia exclusao logica')
            for sql in DOWN:
                db.execute(sql)
            db.execute('DELETE FROM schema_migrations')
        db.commit()
    except BaseException:
        db.rollback()
        raise


def validate(db):
    if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
        raise ValueError('Integridade comprometida')
    if db.execute('PRAGMA foreign_key_check').fetchall():
        raise ValueError('Vinculos inconsistentes')


def copy_database(source, destination):
    source, destination = Path(source).resolve(), Path(destination).absolute()
    if not source.is_file():
        raise ValueError('Origem ausente')
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(fd)
    try:
        with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as src:
            validate(src)
            with sqlite3.connect(destination) as dst:
                src.backup(dst)
                validate(dst)
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
    return destination


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['backup', 'restore'])
    parser.add_argument('source')
    parser.add_argument('destination')
    args = parser.parse_args()
    copy_database(args.source, args.destination)
    print('Copia isolada criada e verificada')


if __name__ == '__main__':
    main()
