"""C06 CLI and C04 no-false-approval regression."""
from __future__ import annotations
from pathlib import Path
import json
from uuid import UUID
import pytest
from sie_api.v201_dev_store import DevStore
from sie_api.v201_c_cli import main
from sie_api.v201_c_normative import resolve_rule

A="11111111-1111-4111-8111-111111111111"

def test_cli_denied_without_explicit_isolated_dev_flag(monkeypatch,tmp_path):
    monkeypatch.delenv("SIE_V201_C_ETL_DEV",raising=False)
    monkeypatch.setenv("SIE_ENV","test")
    with pytest.raises(SystemExit):
        main(["stage","--database",str(tmp_path/"s.sqlite3"),
              "--manifest",str(tmp_path/"manifest.json"),"--owner",A,
              "--project",A,"--revision",A,"--idempotency-key","cli-test-0001"])

def test_cli_synthetic_happy_path(monkeypatch,tmp_path,capsys):
    monkeypatch.setenv("SIE_ENV","test")
    monkeypatch.setenv("SIE_V201_C_ETL_DEV","1")
    db=(tmp_path/"data.sqlite3").resolve()
    store=DevStore(str(db))
    proj=store.create_project(A,"CLI DEV","cli-project-test")["id"]
    rev=store.create_revision(A,proj,"cli-revision-test")["id"]
    manifest=(tmp_path/"fixture.json").resolve()
    manifest.write_text(json.dumps({"source_kind":"SYNTHETIC_TEST","rooms":[],
        "loads":[],"circuits":[],"links":[]}),encoding="utf-8")
    args=["stage","--database",str(db),"--manifest",str(manifest),
          "--owner",A,"--project",proj,"--revision",rev,
          "--idempotency-key","cli-batch-fixture"]
    assert main(args)==0
    assert json.loads(capsys.readouterr().out)["reconciliation"]["state"]=="PASS_DEV_SYNTHETIC"
    assert main(args)==0
    assert json.loads(capsys.readouterr().out)["batch"]["counts"]["loads"]==0

def test_mutable_catalog_cannot_grant_approval(tmp_path):
    registry={"schema_version":1,"records":[{
      "id":"FAKE-APPROVAL","revision":1,"status":"APPROVED",
      "verified_data":True,"evidence_sha256":"a"*64,
      "approved_by":"anyone","approval_reference":"untrusted-claim"}]}
    path=tmp_path/"forged-registry.json"
    path.write_text(json.dumps(registry),encoding="utf-8")
    decision=resolve_rule("FAKE-APPROVAL",revision=1,path=path)
    assert decision["status"]=="REVIEW_REQUIRED"
    assert decision["reason"]=="TRUSTED_APPROVAL_ATTESTATION_REQUIRED"
