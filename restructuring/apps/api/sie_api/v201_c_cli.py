"""C06 CLI: synthetic DEV staging only, never a remote database writer.

Example:
  SIE_ENV=test SIE_V201_C_ETL_DEV=1 python -m sie_api.v201_c_cli stage \
    --database /absolute/sie2-c.sqlite3 --manifest /absolute/synthetic.json \
    --owner UUID --project UUID --revision UUID --idempotency-key c06-fixture-001
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from .v201_dev_store import DevStore, Invalid
from .v201_c_etl import stage_synthetic, reconcile_synthetic

def main(argv=None):
    parser=argparse.ArgumentParser(description="SIE 2.0 C06 synthetic DEV ETL")
    sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("stage",help="stage synthetic authorized fixture in isolated SQLite DEV")
    for name in ("database","manifest","owner","project","revision","idempotency-key"):
        p.add_argument("--"+name,required=True)
    args=parser.parse_args(argv)
    if os.environ.get("SIE_ENV") not in {"dev","test"} or os.environ.get("SIE_V201_C_ETL_DEV")!="1":
        parser.error("C06 CLI disabled: requires isolated DEV/TEST flag")
    db=Path(args.database)
    manifest=Path(args.manifest)
    if not db.is_absolute() or db.suffix!=".sqlite3" or not manifest.is_absolute() or not manifest.is_file():
        parser.error("database/manifest must be absolute; database suffix .sqlite3")
    if manifest.stat().st_size>262144:
        parser.error("manifest exceeds 256 KiB")
    try:
        payload=json.loads(manifest.read_text(encoding="utf-8"))
        store=DevStore(str(db))
        result=stage_synthetic(store,args.owner,args.project,args.revision,
                               args.idempotency_key,payload)
        reconciliation=reconcile_synthetic(store,args.owner,args.project,args.revision,result)
    except (ValueError,KeyError,OSError) as exc:
        parser.error("synthetic staging rejected: "+str(exc))
    print(json.dumps({"batch":result,"reconciliation":reconciliation},
                     ensure_ascii=False,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
