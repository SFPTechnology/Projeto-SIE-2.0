"""Ensaio de cálculo com proveniência REAL dos algoritmos, sem afirmar norma."""
from hashlib import sha256
from inspect import getsource
import json
from .domain.engines import (selecionar_condutor, selecionar_disjuntor,
                             calcular_queda_tensao_monofasica)
from uuid import uuid4

ALGOS = (
    "sie_api.domain.engines.selecionar_condutor:v1",
    "sie_api.domain.engines.selecionar_disjuntor:v1",
    "sie_api.domain.engines.calcular_queda_tensao_monofasica:v1",
)
TYPE = "LOCAL_UNVERIFIED_ALGORITHM_TRACE_NOT_NORMATIVE_ATTESTATION"


def _canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False)


def preparar_registro(projeto_id, revisao, circuito_nome, entrada, resultado):
    """Apenas dados efetivamente recebidos/calculados pelo servidor, não regras ABNT."""
    item = {
        "id": str(uuid4()), "projeto_id": projeto_id,
        "revisao_projeto": revisao, "circuito_nome": circuito_nome,
        "entrada": entrada, "resultado": resultado,
        "algorithm_ids_executed": list(ALGOS),
        "algorithm_function_source_sha256": {
            "selecionar_condutor": sha256(getsource(selecionar_condutor).encode("utf-8")).hexdigest(),
            "selecionar_disjuntor": sha256(getsource(selecionar_disjuntor).encode("utf-8")).hexdigest(),
            "calcular_queda_tensao_monofasica": sha256(getsource(calcular_queda_tensao_monofasica).encode("utf-8")).hexdigest(),
        },
        "normative_rule_ids_used_verified": [],
        "normative_cells_used_verified": [],
        "source_values_verified": False,
        "reported_normative_source_origin": "CLIENT_DECLARATION_NOT_VERIFIED",
        "calculation_trace_kind": TYPE,
        "normative_conformity_verified": False,
        "release_allowed": False,
    }
    serialized = _canonical(item)
    return item, serialized, sha256(serialized.encode("utf-8")).hexdigest()


def validar_registro(serialized, digest):
    if sha256(serialized.encode("utf-8")).hexdigest() != digest:
        raise ValueError("Integridade de ensaio de calculo comprometida")
    item = json.loads(serialized)
    if (item.get("calculation_trace_kind") != TYPE or
        set(item.get("algorithm_function_source_sha256", {})) != {
            "selecionar_condutor", "selecionar_disjuntor",
            "calcular_queda_tensao_monofasica"} or
        any(len(v) != 64 for v in item.get("algorithm_function_source_sha256", {}).values()) or
        item.get("release_allowed") is not False or
        item.get("normative_conformity_verified") is not False or
        item.get("source_values_verified") is not False or
        item.get("reported_normative_source_origin") != "CLIENT_DECLARATION_NOT_VERIFIED" or
        item.get("normative_rule_ids_used_verified") != [] or
        item.get("normative_cells_used_verified") != []):
        raise ValueError("Registro de ensaio invalido ou alegacao de homologacao")
    return item
