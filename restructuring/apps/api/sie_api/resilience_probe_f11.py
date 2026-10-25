"""Reproducible local F11 probe; no production data or network dependency."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import socket
import sqlite3
import statistics
import tempfile
from threading import Barrier
from time import perf_counter
from uuid import uuid4

from .storage import ConflitoRevisao, RepositorioProjetos


def _milliseconds(start):
    return round((perf_counter() - start) * 1000, 3)


def _p95(values):
    ordered = sorted(values)
    return ordered[max(0, (len(ordered) * 95 + 99) // 100 - 1)]


def probe(directory: str | Path, *, payload_kib: int = 256,
          readers: int = 32, writers: int = 8) -> dict:
    if not 1 <= payload_kib <= 900 or not 1 <= readers <= 500 or not 2 <= writers <= 32:
        raise ValueError('Probe parameters outside bounded local range')
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    db_path = root / 'probe.sqlite'
    if db_path.exists():
        raise FileExistsError(db_path)
    repo = RepositorioProjetos(db_path)
    project_id = str(uuid4())
    data = {'payload': 'x' * (payload_kib * 1024)}
    start = perf_counter()
    repo.salvar(project_id, 'F11 probe', data, 0)
    create_ms = _milliseconds(start)

    times = []
    for _ in range(readers):
        start = perf_counter()
        assert repo.carregar_revisao(project_id, 1)['dados'] == data
        times.append(_milliseconds(start))

    barrier = Barrier(writers)

    def competing_write(i):
        local = RepositorioProjetos(db_path)
        barrier.wait(timeout=10)
        start = perf_counter()
        try:
            local.salvar(project_id, 'F11 probe', {'winner': i}, 1)
            return 'saved', _milliseconds(start)
        except ConflitoRevisao:
            return 'conflict', _milliseconds(start)

    start = perf_counter()
    with ThreadPoolExecutor(max_workers=writers) as pool:
        results = list(pool.map(competing_write, range(writers)))
    concurrent_ms = _milliseconds(start)
    assert sorted(status for status, _ in results) == ['conflict'] * (writers - 1) + ['saved']
    assert repo.carregar(project_id)['revisao'] == 2

    with sqlite3.connect(db_path, timeout=0.1) as exclusive:
        exclusive.execute('BEGIN EXCLUSIVE')
        start = perf_counter()
        try:
            with sqlite3.connect(db_path, timeout=0.05) as blocked:
                blocked.execute('INSERT INTO eventos_auditoria(projeto_id,acao,revisao,criado_em) '
                                "VALUES(?, 'probe', 2, 'probe')", (project_id,))
        except sqlite3.OperationalError as exc:
            if 'locked' not in str(exc):
                raise
            lock_timeout_ms = _milliseconds(start)
        else:
            raise AssertionError('Write unexpectedly succeeded under exclusive lock')
        exclusive.rollback()
    assert repo.carregar(project_id)['revisao'] == 2

    # A bound but unlistened loopback port models a failed local transport only. It makes no
    # assertion about the browser's retry policy or a remote deployment.
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        unused_port = listener.getsockname()[1]
        start = perf_counter()
        try:
            socket.create_connection(('127.0.0.1', unused_port), timeout=0.2)
        except OSError:
            outage_ms = _milliseconds(start)
        else:
            raise AssertionError('Unlistened loopback port unexpectedly accepted connection')
    assert repo.carregar(project_id)['revisao'] == 2

    # Corrupt a disposable copy; the historical revision hash must fail closed.
    with sqlite3.connect(db_path) as db:
        db.execute('DROP TRIGGER f01_versao_sem_update')
        db.execute("UPDATE versoes_projeto SET dados_json='{}' WHERE projeto_id=? AND revisao=1",
                   (project_id,))
    try:
        repo.carregar_revisao(project_id, 1)
    except ValueError as exc:
        if 'Integridade' not in str(exc):
            raise
    else:
        raise AssertionError('Corrupt historical revision accepted')

    return {
        'scope': 'LOCAL_SYNTHETIC_NON_NORMATIVE', 'payload_kib': payload_kib,
        'readers': readers, 'writers': writers,
        'create_ms': create_ms, 'read_p95_ms': _p95(times),
        'read_median_ms': round(statistics.median(times), 3),
        'concurrent_total_ms': concurrent_ms,
        'write_p95_ms': _p95([duration for _, duration in results]),
        'winners': 1, 'conflicts': writers - 1,
        'lock_timeout_ms': lock_timeout_ms, 'network_outage_ms': outage_ms,
        'corruption_rejected': True, 'revision_after_failure': 2,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--payload-kib', type=int, default=256)
    parser.add_argument('--readers', type=int, default=32)
    parser.add_argument('--writers', type=int, default=8)
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory(prefix='sie-f11-resilience-') as directory:
        print(json.dumps(probe(directory, payload_kib=args.payload_kib,
                               readers=args.readers, writers=args.writers), sort_keys=True))


if __name__ == '__main__':
    main()
