"""F11: a complete F10 export cannot remain current across project revisions."""

import pytest

from sie_api.persisted_source_f10 import publish_from_repository, verify_against_repository
from sie_api.representation_f10 import ArtifactError
from test_full_f10_integration import prepare_full


def test_full_document_is_stale_after_saved_revision_and_requires_new_run(tmp_path):
    repo, project_id, run_id = prepare_full(tmp_path)
    old = tmp_path / "revision-2" / "bundle"
    publish_from_repository(repo, project_id, 2, run_id, "full-v1", old, full=True)
    assert verify_against_repository(repo, old)["currentness"] == "CURRENT"

    saved = repo.carregar(project_id)
    data = saved["dados"]
    data["floor_plan_f10"]["revision_id"] = "3"
    data["floor_plan_f10"]["placements"][0]["x"] = 12
    repo.salvar(project_id, saved["nome"], data, 2)

    assert verify_against_repository(repo, old)["currentness"] == "STALE"
    with pytest.raises(ArtifactError):
        publish_from_repository(repo, project_id, 3, run_id, "full-v1", tmp_path / "premature", full=True)

    repo.executar_calculo_f10(project_id, 3, run_id)
    new = tmp_path / "revision-3" / "bundle"
    publish_from_repository(repo, project_id, 3, run_id, "full-v1", new, full=True)
    assert verify_against_repository(repo, new)["currentness"] == "CURRENT"
    assert verify_against_repository(repo, old)["currentness"] == "STALE"
