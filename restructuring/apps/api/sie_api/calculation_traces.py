"""Ensaio de cálculo com proveniência REAL dos algoritmos, sem afirmar norma."""
from decimal import Decimal
from hashlib import sha256
from inspect import getsource
import json
from .domain.engines import (selecionar_condutor, selecionar_disjuntor,
                             calcular_queda_tensao_monofasica)
from uuid import uuid4
from .application import analisar_circuito

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
    # Captura a linha do input REALMENTE usada no calculo; nao uma celula ABNT.
    secao = Decimal(str(resultado["condutor"]["secao_mm2"]))
    linhas_efetivas = [
        {"indice_entrada": n, "secao_mm2": row["secao_mm2"],
         "capacidade_a": row["capacidade_a"]}
        for n, row in enumerate(entrada["tabela_condutores"])
        if Decimal(str(row["secao_mm2"])) == secao
    ]
    if len(linhas_efetivas) != 1:
        raise ValueError("Linha efetiva de condutor nao identificada de modo unico")
    expected_capacity = Decimal(str(linhas_efetivas[0]["capacidade_a"])) * Decimal(
        str(entrada["fator_correcao"]))
    if Decimal(str(resultado["condutor"]["capacidade_decisao_a"])) != expected_capacity:
        raise ValueError("Iz efetivamente utilizada diverge da linha e fator recebidos")
    applied_values = {
        "selected_input_row": linhas_efetivas[0],
        "input_row_sha256": sha256(_canonical(linhas_efetivas[0]).encode("utf-8")).hexdigest(),
        "source_parameter_kinds": {
            "conductor_base_iz": "CLIENT_DECLARED",
            "correction_factor": "CLIENT_DECLARED",
            "resistance_ohm_km": "CLIENT_DECLARED",
        },
        "correction_factor": entrada["fator_correcao"],
        "resistance_ohm_km": entrada["resistencia_ohm_km"],
        "capacity_for_breaker_decision_a": resultado["condutor"]["capacidade_decisao_a"],
        "source_classification": "CLIENT_SUPPLIED_UNVERIFIED_NOT_NORMATIVE_CELL",
    }
    item = {
        "trace_schema_version": 2,
        "orchestration_source": {
            "id": "sie_api.application.analisar_circuito:v2",
            "function_source_sha256": sha256(getsource(analisar_circuito).encode("utf-8")).hexdigest(),
        },
        "values_actually_used_by_algorithm": applied_values,
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
        not isinstance(item.get("values_actually_used_by_algorithm"), dict) or
        item["values_actually_used_by_algorithm"].get("source_classification") !=
        "CLIENT_SUPPLIED_UNVERIFIED_NOT_NORMATIVE_CELL" or
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
    # Optional provenance preserves pre-existing v1/v2 traces without backfill.
    orchestration = item.get("orchestration_source")
    if orchestration is not None and (
        not isinstance(orchestration, dict) or
        orchestration.get("id") != "sie_api.application.analisar_circuito:v2" or
        not isinstance(orchestration.get("function_source_sha256"), str) or
        len(orchestration["function_source_sha256"]) != 64 or
        any(c not in "0123456789abcdef" for c in orchestration["function_source_sha256"])
    ):
        raise ValueError("Proveniencia da orquestracao de calculo invalida")
    # Version 1 remains readable for historical local traces. Stronger v2
    # rejects internal inconsistencies even if someone recalculates the digest.
    version = item.get("trace_schema_version", 1)
    if version not in (1, 2):
        raise ValueError("Versao do formato de ensaio nao suportada")
    if version == 2:
        used = item["values_actually_used_by_algorithm"]
        line = used.get("selected_input_row")
        if not isinstance(line, dict):
            raise ValueError("Linha de entrada realmente consumida ausente")
        expected_hash = sha256(_canonical(line).encode("utf-8")).hexdigest()
        if used.get("input_row_sha256") != expected_hash:
            raise ValueError("Hash da linha realmente consumida nao confere")
        origins = used.get("source_parameter_kinds")
        if origins != {
            "conductor_base_iz": "CLIENT_DECLARED",
            "correction_factor": "CLIENT_DECLARED",
            "resistance_ohm_km": "CLIENT_DECLARED",
        }:
            raise ValueError("Fonte de parametros alterada sem homologacao")
        try:
            raw_row = item["entrada"]["tabela_condutores"][line["indice_entrada"]]
            matching = (Decimal(str(raw_row["secao_mm2"])) == Decimal(str(line["secao_mm2"]))
                        and Decimal(str(raw_row["capacidade_a"])) == Decimal(str(line["capacidade_a"])))
            expected_iz = Decimal(str(raw_row["capacidade_a"])) * Decimal(str(item["entrada"]["fator_correcao"]))
            actual_iz = Decimal(str(item["resultado"]["condutor"]["capacidade_decisao_a"]))
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ValueError("Linha/fator de entrada invalido no historico") from exc
        if not matching or expected_iz != actual_iz:
            raise ValueError("Trilha de parametros nao corresponde ao calculo efetivo")
    return item
