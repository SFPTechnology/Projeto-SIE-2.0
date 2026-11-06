"""C01/C07 read-only drift checker; NEVER a backup or import authorization.

Expected and current reports are summaries produced from one consistent SQL
statement per observation. A mismatch prevents cutover, including same-count
payload modifications. Do not use unhashed row identifiers as an approval.
"""
from __future__ import annotations
from hmac import compare_digest
import re

TABLES=("projetos","dependencias","dependencia_bancadas",
 "dependencia_cargas_adicionais","dependencia_edicoes_manuais",
 "dependencia_validacao","dependencia_retornos_downstream",
 "eventos_auditoria","parametros_edp_overrides",
 "dimensionamento_condutores_overrides","dimensionamento_condutores_resultado",
 "dimensionamento_disjuntores_overrides","queda_tensao_config",
 "secoes_otimizadas_operacoes","secoes_otimizadas_projeto")
HEX=re.compile(r"^[0-9a-f]{64}$")

def fingerprint_sql():
    """Literal SELECT-only statement for manual read-back against legacy PG17.

    Rows are canonically represented by PG17 jsonb->text within one statement.
    Identical SQL/query version must be used on both observations. The result
    is not a transactionally durable export nor substitute for a cold backup.
    """
    clauses=[]
    for name in TABLES:
        clauses.append(
            "SELECT '"+name+"' AS table_name, count(*)::integer AS count_rows, "
            "encode(pg_catalog.sha256(pg_catalog.convert_to("
            "coalesce(string_agg(pg_catalog.to_jsonb(t)::text,E'\\n' "
            "ORDER BY pg_catalog.to_jsonb(t)::text),''),'UTF8')),"
            "'hex') AS rows_sha256 FROM public."+name+" t")
    return "\nUNION ALL\n".join(clauses)+";"

def _checked(fingerprint):
    if type(fingerprint) is not dict or (
        fingerprint.get("contract_version")!="SIE-C-LEGACY-READONLY-FINGERPRINT-1"
    ) or fingerprint.get("source_project_ref")!="hlbksclcandbsyqrsbmx":
        raise ValueError("invalid source fingerprint contract")
    entries=fingerprint.get("tables")
    if type(entries) is not list or len(entries)!=len(TABLES):
        raise ValueError("incomplete source inventory")
    found={}
    for row in entries:
        if type(row) is not dict:
            raise ValueError("bad fingerprint row")
        name=row.get("table_name")
        cnt=row.get("count_rows")
        digest=row.get("rows_sha256")
        if (name not in TABLES or name in found or type(cnt) is not int or
            cnt<0 or not isinstance(digest,str) or not HEX.fullmatch(digest)):
            raise ValueError("invalid or repeated source table fingerprint")
        found[name]=(cnt,digest)
    if set(found)!=set(TABLES):
        raise ValueError("missing table fingerprint")
    if sum(v[0] for v in found.values())!=fingerprint.get("total_rows"):
        raise ValueError("inconsistent source totals")
    return found

def compare_readbacks(expected, observed):
    """Metadata-only comparison; never permits cutting over automatically."""
    before,after=_checked(expected),_checked(observed)
    changes=[]
    for table in TABLES:
        a,b=before[table],after[table]
        if a[0]!=b[0] or not compare_digest(a[1],b[1]):
            changes.append({"table":table,"count_before":a[0],"count_after":b[0],
                            "payload_changed":not compare_digest(a[1],b[1])})
    return {"drift_state":"BLOCKED_CHANGED_SOURCE" if changes else "PASS_SAME_OBSERVATION",
            "changed_tables":changes,"compared_tables":len(TABLES),
            "real_import_authorized":False,"restore_test_done":False,
            "source_backup_verified":False,"gate_gc":"BLOCKED"}
