from hashlib import sha256
from pathlib import Path

import pytest

from sie_api.normative_inventory import SOURCE_SPECS, inventory_sources, main


def test_source_inventory_hashes_actual_bytes(tmp_path):
    source = tmp_path / "sources" / "document.pdf"
    source.parent.mkdir()
    source.write_bytes(b"%PDF-example\n")
    report = inventory_sources(tmp_path, [("EXAMPLE", "sources/document.pdf", "PDF_CANDIDATE")])
    item = report["entries"][0]
    assert item["state"] == "PRESENT_UNVERIFIED"
    assert item["sha256"] == sha256(source.read_bytes()).hexdigest()
    assert item["size_bytes"] == len(source.read_bytes())
    assert report["normative_conformity_verified"] is False
    assert item["normative_validation"] == "NOT_PERFORMED"


def test_missing_source_is_explicit_and_never_approved(tmp_path):
    report = inventory_sources(tmp_path, [("MISSING", "missing.pdf", "PDF_CANDIDATE")])
    assert report["sources_present"] == 0
    assert report["sources_missing"] == 1
    assert report["entries"][0]["state"] == "MISSING"
    assert report["entries"][0]["sha256"] is None
    assert report["repository_approval"] is False


@pytest.mark.parametrize("path", ["../outside.pdf", "/tmp/outside.pdf", "other/../../x.pdf"])
def test_source_path_cannot_escape_root(tmp_path, path):
    with pytest.raises(ValueError, match="fora do repositorio"):
        inventory_sources(tmp_path, [("ATTACK", path, "PDF")])


def test_rejects_symlink_escape(tmp_path):
    external = tmp_path.parent / f"outside-{tmp_path.name}.pdf"
    external.write_bytes(b"sample")
    try:
        (tmp_path / "alias.pdf").symlink_to(external)
        with pytest.raises(ValueError, match="fora do repositorio"):
            inventory_sources(tmp_path, [("LINK", "alias.pdf", "PDF")])
    finally:
        external.unlink()


def test_empty_or_duplicate_source_ids_are_not_accepted(tmp_path):
    with pytest.raises(ValueError, match="duplicado"):
        inventory_sources(tmp_path, [("X", "one", "PDF"), ("X", "two", "PDF")])


def test_cli_reports_missing_sources_with_nonzero_exit(tmp_path, capsys):
    assert main(["--root", str(tmp_path), "--require-all"]) == 2
    assert '"normative_conformity_verified": false' in capsys.readouterr().out


def test_inventory_cli_json_is_written_without_norm_text(tmp_path):
    output = tmp_path / "result.json"
    assert main(["--root", str(tmp_path), "--output", str(output)]) == 0
    written = output.read_text(encoding="utf-8")
    assert "SOURCE_INTEGRITY_INVENTORY_ONLY" in written
    assert "normative_validation" in written
    assert "NOT_PERFORMED" in written
    assert len(SOURCE_SPECS) == 6
