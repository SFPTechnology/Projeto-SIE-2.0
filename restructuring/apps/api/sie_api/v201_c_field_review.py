"""C02 offline exact-field review verifier. Data preservation is not engineering approval."""
from __future__ import annotations
import csv
from io import StringIO
from collections import Counter

EXPECTED={"SOURCE_ONLY_NO_INFER":15,"PROFESSIONAL_REVIEW_REQUIRED":7,
          "ZERO_ROWS_ARCHIVE_CONTRACT":22,"SCHEMA_AND_USER_REVIEW_REQUIRED":1}
HEADER=["legacy_table","legacy_column","source_type","proposed_route",
        "decision","basis","rows_at_readback","status"]

def verify_field_review(source_matrix: str,review_matrix: str)->dict:
    if not isinstance(source_matrix,str) or not isinstance(review_matrix,str):
        raise ValueError("both CSVs required")
    source=list(csv.DictReader(StringIO(source_matrix)))
    reviewed=list(csv.DictReader(StringIO(review_matrix)))
    if len(source)!=99 or len(reviewed)!=45 or (
        reviewed and list(reviewed[0])!=HEADER
    ):
        raise ValueError("C02 source/review matrix incomplete")
    keys=set()
    flagged=set()
    for entry in source:
        pair=(entry["legacy_table"],entry["legacy_column"])
        if pair in keys or not all(entry.get(k) for k in ("legacy_table","legacy_column","source_sql_type")):
            raise ValueError("C02 missing/duplicate source columns")
        keys.add(pair)
        if entry["disposition"]=="QUARANTINE_UNMAPPED":
            flagged.add(pair)
    reviewed_keys=set()
    counts=Counter()
    for entry in reviewed:
        pair=(entry["legacy_table"],entry["legacy_column"])
        if pair not in flagged or pair in reviewed_keys:
            raise ValueError("invented/duplicated review field")
        reviewed_keys.add(pair)
        decision=entry["decision"]
        if decision not in EXPECTED:
            raise ValueError("unknown review disposition")
        counts[decision]+=1
        if not entry["basis"].strip() or not entry["proposed_route"].strip():
            raise ValueError("unsupported field review")
        try:
            n=int(entry["rows_at_readback"])
        except ValueError:
            raise ValueError("invalid source count") from None
        if n<0 or (decision=="ZERO_ROWS_ARCHIVE_CONTRACT" and n!=0):
            raise ValueError("wrong zero-row preservation contract")
        needed=("PROFESSIONAL_SIGNOFF_PENDING" if decision=="PROFESSIONAL_REVIEW_REQUIRED"
                else "SCHEMA_MAPPING_REVIEW_PENDING" if decision=="SCHEMA_AND_USER_REVIEW_REQUIRED"
                else "ARCHIVE_ONLY_REVIEWED")
        if entry["status"]!=needed:
            raise ValueError("not an externally signed review")
    if reviewed_keys!=flagged or counts!=Counter(EXPECTED):
        raise ValueError("all 45 fields require explicit controlled disposition")
    return {"scope":"45_OF_45_FIELDS_CLASSIFIED",
            "source_inventory":"99_OF_99_COLUMNS_TRACKED",
            "distribution":dict(counts),
            "data_preservation_design":"PASS_DEVELOPMENT",
            "canonical_mapping_approved":False,
            "professional_signoff_approved":False,
            "live_import_authorized":False,
            "gate_gc":"BLOCKED"}
