"""F11 local resilience invariants; timings are recorded by the CLI probe."""

import pytest

from sie_api.resilience_probe_f11 import probe


def test_concurrent_revision_timeout_outage_and_corruption_fail_closed(tmp_path):
    result = probe(tmp_path, payload_kib=128, readers=8, writers=4)
    assert result['winners'] == 1
    assert result['conflicts'] == 3
    assert result['revision_after_failure'] == 2
    assert result['corruption_rejected'] is True
    assert result['read_p95_ms'] >= 0


@pytest.mark.parametrize('payload,readers,writers', [(0, 8, 4), (901, 8, 4),
                                                   (128, 0, 4), (128, 8, 1)])
def test_probe_bounds_reject_unsafe_configuration(tmp_path, payload, readers, writers):
    with pytest.raises(ValueError, match='bounded'):
        probe(tmp_path, payload_kib=payload, readers=readers, writers=writers)
