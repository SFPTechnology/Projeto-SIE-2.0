"""C01/C02/C07: validate real-source selection and full-column mapping OFFLINE.

Read-only manifest verifier. No Supabase connection, DDL, DML or credentials.
Self-declared ownership is not an authenticated user, staging GO or cutover.
"""
from __future__ import annotations
import csv
from hashlib import sha256
from io import StringIO
import json
from uuid import UUID

SOURCE="hlbksclcandbsyqrsbmx"
DESTINATION="fozrymsidnaxmuvxxfhh"
REQUIRED_COLUMNS=("legacy_table","legacy_column","source_sql_type",
                  "target","disposition","rule_or_blocker")
ALLOWED_DISPOSITIONS=frozenset({
    "DIRECT","DIRECT_NULLABLE","PRESERVE_PROVENANCE","PRESERVE_SOURCE_ONLY",
    "QUARANTINE_ID_MAP","QUARANTINE_TRANSFORM","QUARANTINE_IDENTITY",
    "QUARANTINE_UNMAPPED","REVIEW_REQUIRED","LEGACY_RESULT"})

def _sha(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(",",":"),
        ensure_ascii=False,allow_nan=False).encode("utf-8")).hexdigest()

def verify_selection(selection:dict, matrix_text:str)->dict:
    if type(selection) is not dict or not isinstance(matrix_text,str):
        raise ValueError("selection and CSV required")
    src,dst=selection.get("source"),selection.get("destination")
    if not isinstance(src,dict) or not isinstance(dst,dict):
        raise ValueError("source/destination required")
    if src.get("project_ref")!=SOURCE or dst.get("project_ref")!=DESTINATION:
        raise ValueError("unexpected project identity")
    if selection.get("contract_version")!="SIE-C-OWNER-SELECTION-1":
        raise ValueError("unsupported selection contract")
    rows=selection.get("projects")
    if not isinstance(rows,list) or len(rows)!=5:
        raise ValueError("exactly five independently identified projects required")
    if selection.get("owner_declaration",{}).get("scope")!="ALL_FIVE_LEGACY_PROJECTS":
        raise ValueError("owner declaration missing")
    keys=set()
    for row in rows:
        if type(row) is not dict:
            raise ValueError("bad project record")
        key=row.get("legacy_id")
        if not isinstance(key,str) or not key.startswith("proj-") or key in keys:
            raise ValueError("legacy project ID duplicate/invalid")
        keys.add(key)
        if row.get("selection")!="MIGRATE":
            raise ValueError("unapproved source selection")
        if not isinstance(row.get("name"),str) or not row["name"].strip():
            raise ValueError("source project name missing")
        for count_field in ("rooms","additional_loads"):
            if type(row.get(count_field)) is not int or row[count_field]<0:
                raise ValueError("invalid source count")
    if sum(x["rooms"] for x in rows)!=src.get("room_count") or (
        sum(x["additional_loads"] for x in rows)!=src.get("additional_load_count")
    ) or src.get("project_count")!=5:
        raise ValueError("source ledger counts conflict")
    matrix=list(csv.DictReader(StringIO(matrix_text)))
    if not matrix or tuple(matrix[0].keys())!=REQUIRED_COLUMNS:
        raise ValueError("invalid matrix header or empty mapping")
    seen=set()
    unmapped=[]
    tables=set()
    for entry in matrix:
        if any(not isinstance(entry.get(key),str) or not entry[key].strip()
               for key in REQUIRED_COLUMNS):
            raise ValueError("mapping missing source type or disposition")
        key=(entry["legacy_table"],entry["legacy_column"])
        if key in seen:raise ValueError("duplicate mapping column")
        seen.add(key)
        tables.add(entry["legacy_table"])
        if entry["disposition"] not in ALLOWED_DISPOSITIONS:
            raise ValueError("unrecognized mapping disposition")
        if entry["disposition"] in (
            "QUARANTINE_UNMAPPED","QUARANTINE_IDENTITY",
            "QUARANTINE_TRANSFORM","REVIEW_REQUIRED","QUARANTINE_ID_MAP"
        ):
            unmapped.append(".".join(key))
    if len(tables)!=15 or len(matrix)!=99:
        raise ValueError("operational schema inventory differs: re-read source")
    requested=selection.get("release",{})
    if any(requested.get(key) is not False for key in (
        "real_import_authorized","remote_ddl_authorized",
        "production_deploy_authorized","main_or_f12_write_authorized"
    )):
        raise ValueError("manifest attempted to authorize remote operations")
    owner=dst.get("target_auth_user_id")
    if owner is not None:
        # UUID syntax alone is not proof the user exists, owns the records,
        # or has an authenticated session. Never auto-promote to APPROVED.
        try:
            parsed=UUID(str(owner))
            if parsed.int==0:raise ValueError()
        except (ValueError,AttributeError,TypeError):
            raise ValueError("invalid target Auth identity") from None
    return {
        "scope":"ALL_FIVE_LEGACY_PROJECTS","user_intent":"CONFIRMED",
        "selection_integrity":"PASS",
        "source_project_count":len(rows),
        "source_room_count":src["room_count"],
        "source_additional_load_count":src["additional_load_count"],
        "mapped_column_count":len(matrix),
        "source_table_count":len(tables),
        "review_or_quarantine_column_count":len(unmapped),
        "source_legacy_ids_sha256":_sha(sorted(keys)),
        "matrix_sha256":sha256(matrix_text.encode("utf-8")).hexdigest(),
        "target_auth_verified":False,
        "independent_owner_attestation":"PENDING",
        "normative_signoff":"PENDING",
        "real_import_authorized":False,
        "gate_gc":"BLOCKED",
        "blockers":["SOURCE_CUTOFF_BACKUP_AND_DRIFT_READBACK",
                    "TARGET_AUTH_IDENTITY_AND_OWNER_BINDING",
                    "SOURCE_COLUMNS_REVIEW_AND_QUARANTINE",
                    "ISOLATED_STAGING_AND_RESTORE_TEST",
                    "PROFESSIONAL_ELECTRICAL_SIGNOFF",
                    "E02_E06_APPROVAL_AND_FULL_QA"]
    }

def main():
    from pathlib import Path
    base=Path(__file__).resolve().parents[4]
    path=base/"docs/implantacao-sie-2-0/GREENFIELD"
    manifest=json.loads((path/"C01_C07_SELECTION_ALL_FIVE_V201.json").read_text(encoding="utf-8"))
    matrix=(path/"C02_MATRIZ_COMPLETA_OPERACIONAL_V201.csv").read_text(encoding="utf-8")
    print(json.dumps(verify_selection(manifest,matrix),indent=2,sort_keys=True))

if __name__=="__main__":
    main()
