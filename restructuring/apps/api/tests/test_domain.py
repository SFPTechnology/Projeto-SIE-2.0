from decimal import Decimal
import pytest
from sie_api.domain.models import CircuitoEletrico
from sie_api.domain.gates import EvidenciaNormativa, StatusEngenharia, status_liberacao

def test_domain_valid_circuit():
    c = CircuitoEletrico("C1", Decimal("20"), Decimal("15"), Decimal("220"))
    assert c.corrente_a == Decimal("20")

@pytest.mark.parametrize("corrente", ["0", "-1", "NaN", "Infinity"])
def test_invalid_current(corrente):
    with pytest.raises(ValueError):
        CircuitoEletrico("C1", Decimal(corrente), Decimal("10"), Decimal("127"))

def test_gate_missing_evidence_blocks():
    assert status_liberacao(None) == StatusEngenharia.BLOQUEADO

def test_gate_partial_evidence_pending():
    e = EvidenciaNormativa("Fonte", "v1", "Tabela 1", True, False)
    assert status_liberacao(e) == StatusEngenharia.PENDENTE

def test_client_claims_do_not_approve_normative_gate():
    e = EvidenciaNormativa("Fonte", "v1", "Tabela 1", True, True)
    assert status_liberacao(e) == StatusEngenharia.PENDENTE


def test_missing_reference_blocks_even_if_flags_claim_success():
    e = EvidenciaNormativa("Fonte", "v1", " ", True, True)
    assert status_liberacao(e) == StatusEngenharia.BLOQUEADO
