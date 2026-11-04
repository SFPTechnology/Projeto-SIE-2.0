"""C15: compare read-only aggregate inventories, NEVER a database backup.

No network/DB access, credentials, export, SQL writes or migration authority.
The expected inventory comes from reviewed historical 15-table baseline.
A stable aggregate snapshot is only a preliminary source-readback gate.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

SOURCE="hlbksclcandbsyqrsbmx"
DEST="fozrymsidnaxmuvxxfhh"
BASELINE={
    "dependencia_bancadas":0,
    "dependencia_cargas_adicionais":52,
    "dependencia_edicoes_manuais":17,
    "dependencia_retornos_downstream":0,
    "dependencia_validacao":0,
    "dependencias":41,
    "dimensionamento_condutores_overrides":2,
    "dimensionamento_condutores_resultado":3,
    "dimensionamento_disjuntores_overrides":2,
    "eventos_auditoria":1805,
    "parametros_edp_overrides":2,
    "projetos":5,
    "queda_tensao_config":5,
    "secoes_otimizadas_operacoes":0,
    "secoes_otimizadas_projeto":0,
}
BOOKKEEPING="sie_schema_migrations"
SCHEMA_COLUMNS=99
SELECTED_PROJECTS=5


def assess_source_inventory(inventory: dict) -> dict:
    """Fail closed on drift, misattribution, missing evidence and fake GO."""
    if type(inventory) is not dict:
        raise ValueError("inventory must be an object")
    if inventory.get("source_project_ref")!=SOURCE:
        raise ValueError("wrong source reference")
    if inventory.get("destination_project_ref")!=DEST:
        raise ValueError("wrong destination reference")
    if inventory.get("capture_method")!="READ_ONLY_AGGREGATE_SQL":
        raise ValueError("capture not a documented read-only inventory")
    raw=inventory.get("table_counts")
    if type(raw) is not dict or set(raw)!=set(BASELINE):
        raise ValueError("not exactly 15 operational tables")
    if any(type(v) is not int or v<0 for v in raw.values()):
        raise ValueError("invalid source row counts")
    columns=inventory.get("operational_columns")
    selected=inventory.get("selected_projects")
    if type(columns) is not int or type(selected) is not int:
        raise ValueError("missing schema or selection counts")
    if inventory.get("contains_personal_data") is not False:
        raise ValueError("inventory must contain aggregates only")
    # Preserving historical audit records is mandatory: dangling references
    # are not permission to drop or fabricate audit events during ETL.
    null_refs=inventory.get("audit_without_room_reference")
    dangling_refs=inventory.get("audit_unresolved_room_reference")
    if (type(null_refs) is not int or type(dangling_refs) is not int or
        null_refs<0 or dangling_refs<0 or
        null_refs+dangling_refs>raw["eventos_auditoria"]):
        raise ValueError("invalid audit reference inventory")
    unexpected_claims=["real_backup_verified", "real_restore_verified",
                       "source_cutoff_approved","remote_migration_go","real_import_go"]
    if any(inventory.get(c) is not False for c in unexpected_claims):
        raise ValueError("source readback cannot assert backup, restore or GO")
    changes={
        name:{"baseline":BASELINE[name],"observed":raw[name]}
        for name in BASELINE if raw[name]!=BASELINE[name]
    }
    if columns!=SCHEMA_COLUMNS:
        changes["operational_columns"]={"baseline":SCHEMA_COLUMNS,"observed":columns}
    if selected!=SELECTED_PROJECTS:
        changes["selected_projects"]={"baseline":SELECTED_PROJECTS,"observed":selected}
    for name,baseline,observed in (("audit_without_room_reference",469,null_refs),
                                   ("audit_unresolved_room_reference",10,dangling_refs)):
        if baseline!=observed:
            changes[name]={"baseline":baseline,"observed":observed}
    total=sum(raw.values())
    status="STABLE_AGGREGATE_READBACK" if not changes else "DRIFT_REQUIRES_REVIEW"
    return {
        "status":status,
        "source_project_ref":SOURCE,
        "selected_projects":selected,
        "operational_tables":len(raw),
        "operational_columns":columns,
        "source_total_rows":total,
        "audit_without_room_reference":null_refs,
        "audit_unresolved_room_reference":dangling_refs,
        "audit_events_must_be_preserved":True,
        "source_drift":changes,
        "real_source_backup":"NOT_VERIFIED",
        "consistent_cutoff":"NOT_VERIFIED",
        "target_backup_restore":"NOT_VERIFIED",
        "auth_owner_binding":"NOT_VERIFIED",
        "real_migration_go":False,
        "remote_ddl_go":False,
        "gate_gc":"BLOCKED",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inventory",required=True,type=Path)
    args=p.parse_args()
    data=json.loads(args.inventory.read_text(encoding="utf-8-sig"))
    print(json.dumps(assess_source_inventory(data),sort_keys=True,indent=2))


if __name__=="__main__":
    main()
