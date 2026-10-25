"""Offline SQLite and registered artifact backup. Stop all writers first.

No in-place restore is supported. The returned root map must be used to configure
the restored local service (including SIE_F10_ARTIFACT_ROOT).
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile

from .data_lifecycle import copy_database, validate


FORMAT = 'SIE-F11-MULTI-ROOT-1'


def _hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _inventory(root):
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Raiz ausente ou redirecionada')
    found = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink() or (not path.is_file() and not path.is_dir()):
            raise ValueError('Link simbolico ou entrada especial recusada')
        if path.is_file():
            found[path.relative_to(root).as_posix()] = _hash(path)
    return found


def _rows(db_path):
    with sqlite3.connect(db_path) as db:
        validate(db)
        if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='artefatos_f10'").fetchone():
            return []
        return db.execute('SELECT artifact_root,destination_relative,manifest_sha256,state '
                          'FROM artefatos_f10').fetchall()


def _verify_rows(rows, roots):
    for root, relative, manifest_hash, state in rows:
        if root not in roots or not Path(root).is_absolute():
            raise ValueError('Raiz registrada sem copia')
        path = Path(relative)
        if path.is_absolute() or not path.parts or any(p in ('', '.', '..') for p in path.parts):
            raise ValueError('Caminho registrado inseguro')
        if state != 'PUBLISHED':
            raise ValueError('Publicacao em andamento ou falha; reconciliar antes do backup')
        folder = roots[root] / path
        if folder.is_symlink() or not folder.is_dir():
            raise ValueError('Artefato registrado ausente')
        manifest = folder / 'manifest.json'
        if not manifest.is_file() or manifest.is_symlink() or _hash(manifest) != manifest_hash:
            raise ValueError('Manifesto registrado invalido')
        payload = json.loads(manifest.read_text(encoding='utf-8'))
        for name, digest in payload['files_sha256'].items():
            if Path(name).name != name or not (folder / name).is_file() or _hash(folder / name) != digest:
                raise ValueError('Arquivo registrado invalido')


def backup(database, destination):
    """Create a new verified directory from every registry root; never overwrite."""
    database = Path(database).resolve()
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.sie-f11-backup-', dir=destination.parent))
    try:
        copy_database(database, stage / 'database.sqlite')
        rows = _rows(stage / 'database.sqlite')
        roots = sorted({row[0] for row in rows})
        if any(not Path(root).is_absolute() for root in roots):
            raise ValueError('Raiz registrada nao absoluta')
        if any(destination == Path(root) or destination.is_relative_to(Path(root)) for root in roots):
            raise ValueError('Destino dentro de raiz registrada')
        copied = {}
        for index, root in enumerate(roots):
            origin = Path(root)
            if origin.is_symlink() or not origin.is_dir():
                raise ValueError('Raiz registrada ausente ou redirecionada')
            original_inventory = _inventory(origin)
            target = stage / 'roots' / f'{index:04d}'
            shutil.copytree(origin, target, symlinks=True)
            if _inventory(target) != original_inventory or _inventory(origin) != original_inventory:
                raise ValueError('Arquivos alterados durante backup')
            copied[root] = target
        _verify_rows(rows, copied)
        manifest = {'format': FORMAT, 'database_sha256': _hash(stage / 'database.sqlite'),
                    'roots': [{'original': root, 'directory': f'roots/{i:04d}',
                               'files_sha256': _inventory(copied[root])} for i, root in enumerate(roots)]}
        (stage / 'bundle.json').write_text(json.dumps(manifest, sort_keys=True), encoding='utf-8')
        destination.mkdir(mode=0o700)  # fail if another process reserved the name
        try:
            shutil.copyfile(stage / 'database.sqlite', destination / 'database.sqlite')
            if roots:
                shutil.copytree(stage / 'roots', destination / 'roots')
            if _hash(destination / 'database.sqlite') != manifest['database_sha256'] or any(
                _inventory(destination / item['directory']) != item['files_sha256'] for item in manifest['roots']
            ):
                raise ValueError('Copia final incompleta')
            shutil.copyfile(stage / 'bundle.json', destination / 'bundle.json')
        except BaseException:
            shutil.rmtree(destination)
            raise
        return manifest
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def restore(bundle, destination_db, destination_roots):
    """Restore to two new paths; roots are placed under destination_roots."""
    bundle = Path(bundle).absolute()
    destination_db, destination_roots = Path(destination_db).absolute(), Path(destination_roots).absolute()
    if bundle.is_symlink() or not bundle.is_dir():
        raise ValueError('Pacote invalido')
    if (bundle / 'bundle.json').is_symlink() or (bundle / 'database.sqlite').is_symlink():
        raise ValueError('Link simbolico no pacote')
    if any(p.exists() or p.is_symlink() for p in (destination_db, destination_roots)):
        raise FileExistsError('Destino ja existe')
    if destination_roots == destination_db.parent or destination_db.is_relative_to(destination_roots):
        raise ValueError('Destinos sobrepostos')
    manifest = json.loads((bundle / 'bundle.json').read_text(encoding='utf-8'))
    if manifest.get('format') != FORMAT or _hash(bundle / 'database.sqlite') != manifest['database_sha256']:
        raise ValueError('Pacote alterado ou formato desconhecido')
    roots = {}
    for i, row in enumerate(manifest['roots']):
        if row['directory'] != f'roots/{i:04d}' or row['original'] in roots:
            raise ValueError('Mapa de raizes invalido')
        source = bundle / row['directory']
        if _inventory(source) != row['files_sha256']:
            raise ValueError('Pacote alterado ou incompleto')
        roots[row['original']] = source
    # A staging directory placed below the bundle or a live source root can be
    # encountered by copytree while it is being populated, leading to recursive
    # copies or contaminating the original artifact inventory.
    destinations = (destination_db.resolve(), destination_roots.resolve())
    protected = (bundle.resolve(), *(Path(root).resolve() for root in roots))
    if any(dst == source or dst.is_relative_to(source)
           for dst in destinations for source in protected):
        raise ValueError('Destino dentro do pacote ou de raiz original')
    rows = _rows(bundle / 'database.sqlite')
    if set(roots) != {row[0] for row in rows}:
        raise ValueError('Mapa de raizes diverge do banco')
    _verify_rows(rows, roots)
    destination_db.parent.mkdir(parents=True, exist_ok=True)
    destination_roots.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.sie-f11-db-', dir=destination_db.parent)
    os.close(fd)
    stage_db = Path(name)
    stage_roots = Path(tempfile.mkdtemp(prefix='.sie-f11-roots-', dir=destination_roots.parent))
    try:
        os.chmod(stage_db, 0o600)
        shutil.copyfile(bundle / 'database.sqlite', stage_db)
        mapping = {original: str(destination_roots / f'{i:04d}') for i, original in enumerate(roots)}
        for i, source in enumerate(roots.values()):
            shutil.copytree(source, stage_roots / f'{i:04d}', symlinks=True)
        with sqlite3.connect(stage_db) as db:
            validate(db)
            if rows:
                db.executemany('UPDATE artefatos_f10 SET artifact_root=? WHERE artifact_root=?',
                               [(new, old) for old, new in mapping.items()])
            validate(db)
        _verify_rows(_rows(stage_db), {mapping[old]: stage_roots / f'{i:04d}' for i, old in enumerate(roots)})
        destination_roots.mkdir(mode=0o700)  # exclusive reservation, no directory replacement
        try:
            shutil.copytree(stage_roots, destination_roots, dirs_exist_ok=True)
            os.link(stage_db, destination_db)  # exclusive file creation, no overwrite race
        except BaseException:
            shutil.rmtree(destination_roots)
            raise
        return {'database': str(destination_db), 'root_mapping': mapping}
    finally:
        stage_db.unlink(missing_ok=True)
        if stage_roots.exists():
            shutil.rmtree(stage_roots)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    create = commands.add_parser('backup')
    create.add_argument('--db', required=True)
    create.add_argument('--bundle', required=True)
    recover = commands.add_parser('restore')
    recover.add_argument('--bundle', required=True)
    recover.add_argument('--db', required=True)
    recover.add_argument('--roots', required=True)
    args = parser.parse_args(argv)
    result = backup(args.db, args.bundle) if args.operation == 'backup' else restore(args.bundle, args.db, args.roots)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
