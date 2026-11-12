"""C18: read-only/offline migration readiness for SIE2 preproduction.

Only checks inspected versioned files, review state and non-sensitive
aggregate baselines; NEVER connects to Supabase or writes to any DB.
No-backup directive does not magically provide recovery or Auth provenance.
Legacy import is optional when the active scope is greenfield.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path

DEST="fozrymsidnaxmuvxxfhh"
SOURCE="hlbksclcandbsyqrsbmx"
MIGRATION_FILES=(
    "20261028102000_sie_a03_indexes_v201.sql",
    "20261028102100_sie_a04_revision_lifecycle_v201.sql",
    "20261028153000_sie_b04_idempotency_backend_grants_v201.sql",
    "20261028203000_sie_c03_electrical_domain_v201.sql",
)
EXPECTED_APPLIED=("20261027195557",)

def assess(contract:dict, migration_dir:Path, *, actual_applied:tuple[str,...],
           auth_users:int, auth_sessions:int, dest_projects:int,
           source_projects:int|None=None, legacy_real_etl_enabled:bool=False)->dict:
    if not isinstance(contract,dict) or contract.get("supabase_project_ref")!=DEST:
        raise ValueError("wrong SIE2 destination contract")
    if not isinstance(migration_dir,Path) or not migration_dir.is_dir():
        raise ValueError("missing versioned migrations")
    expected={f.split("_",1)[0] for f in MIGRATION_FILES}
    if tuple(actual_applied)!=EXPECTED_APPLIED:
        raise ValueError("remote migration drift from verified GF02 baseline")
    counts=(auth_users,auth_sessions,dest_projects)
    if any(type(x) is not int or x<0 for x in counts):
        raise ValueError("invalid read-only row counts")
    if source_projects is not None and (type(source_projects) is not int or source_projects<0):
        raise ValueError("invalid legacy source project count")
    files=[]
    for name in MIGRATION_FILES:
        p=migration_dir/name
        if not p.is_file():
            raise ValueError("missing migration: "+name)
        data=p.read_bytes()
        if not data.strip():
            raise ValueError("empty migration: "+name)
        files.append({"name":name,"version":name.split("_",1)[0],
                      "sha256":sha256(data).hexdigest(),"bytes":len(data)})
    if len({f["version"] for f in files})!=4 or expected&set(actual_applied):
        raise ValueError("migration version collision")
    current=contract.get("effective_user_decision_20261104",{})
    cancelled_c17=current.get("c17_execution_permitted") is False
    greenfield=contract.get("current_delivery_scope",{}).get("strategy")=="GREENFIELD_NO_LEGACY_IMPORT"
    auth=contract.get("preproduction_authorization",{})
    if (auth.get("project_ref")!=DEST or
        auth.get("migration_application_approved_conditionally") is not True):
        raise ValueError("no scoped preproduction consent")
    backup=auth.get("backup_real_state")
    restore=auth.get("restore_real_state")
    blockers=[]
    if backup!="VERIFIED" or restore!="VERIFIED":
        blockers.append("DESTINATION_RECOVERY_ALTERNATIVE_PENDING" if cancelled_c17 else
                        "NO_VERIFIED_RECOVERABLE_DESTINATION_BACKUP_AND_RESTORE")
    if auth_sessions==0:
        blockers.append("NO_VERIFIED_REAL_AUTH_SESSION")
    if dest_projects:
        blockers.append("DESTINATION_NOT_EMPTY_REVIEW_DRIFT")
    if not greenfield:
        if source_projects!=5:
            blockers.append("SOURCE_FIVE_PROJECT_INVENTORY_DRIFT")
        if not legacy_real_etl_enabled:
            blockers.append("REAL_ETL_IMPLEMENTATION_DISABLED")
    # Refusing C17 is an execution constraint, not a failed safety check.
    # No alternative verifier exists here: editable flags cannot prove recovery.
    if cancelled_c17 and "DESTINATION_RECOVERY_ALTERNATIVE_PENDING" not in blockers:
        blockers.append("DESTINATION_RECOVERY_ALTERNATIVE_PENDING")
    # Even successful dry-run/CI and all editable flags are insufficient:
    # concrete restoration, human identity evidence and externally verified
    # migration readbacks are mandatory before real data movement.
    return {
        "gate":"GC",
        "stage":"C18_READ_ONLY_EXECUTION_READINESS",
        "destination":DEST,"source":SOURCE,
        "delivery_strategy":"GREENFIELD_NO_LEGACY_IMPORT" if greenfield else "LEGACY_IMPORT_SCOPED",
        "legacy_import_requirement":"DEFERRED_OPTIONAL" if greenfield else "REQUIRED",
        "migration_order":[f["version"] for f in files],
        "migration_files":files,
        "actual_applied_before_work":list(actual_applied),
        "evidence_provenance":"SUPPLIED_BASELINE_INPUTS_NOT_LIVE_SUPABASE_READBACK",
        "input_counts_are_not_current_live_verification":True,
        "read_only_observations":{
            "auth_users":auth_users,"auth_sessions":auth_sessions,
            "destination_projects":dest_projects,"source_projects":source_projects},
        "blockers":sorted(set(blockers)),
        "migrations_remote_go":False,
        "real_import_go":False,
        "gate_gc":"BLOCKED",
        "honors_user_no_remote_backup_decision":cancelled_c17,
        "recovery_requirement":"INDEPENDENTLY_PROVEN_DESTINATION_RECOVERY",
        "recovery_alternative_verified_by_this_check":False,
        "approval_is_execution_priority_not_evidence":True,
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--contract",required=True,type=Path)
    p.add_argument("--migrations",required=True,type=Path)
    p.add_argument("--applied",nargs="+",default=list(EXPECTED_APPLIED))
    p.add_argument("--auth-users",type=int,required=True)
    p.add_argument("--auth-sessions",type=int,required=True)
    p.add_argument("--dest-projects",type=int,required=True)
    p.add_argument("--source-projects",type=int,default=None)
    args=p.parse_args()
    contract=json.loads(args.contract.read_text(encoding="utf-8-sig"))
    print(json.dumps(assess(contract,args.migrations,actual_applied=tuple(args.applied),
        auth_users=args.auth_users,auth_sessions=args.auth_sessions,
        dest_projects=args.dest_projects,source_projects=args.source_projects),
        ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
