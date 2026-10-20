"""Ensaio de cálculo com proveniência REAL dos algoritmos, sem afirmar norma."""
from decimal import Decimal
from hashlib import sha256
from inspect import getsource
import json
from .domain.engines import (selecionar_condutor, selecionar_disjuntor,
                             calcular_queda_tensao_monofasica)
from uuid import uuid4
from .application import analisar_circuito
from . import cell_bindings, protection_checks

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
    binding = resultado.get("vinculo_celulas")
    if binding is not None:
        applied_values["selected_registered_capacity_cell_id"] = next(
            c["id"] for c in binding["celulas"] if c["tabela"] == "36"
            and Decimal(c["linha"]) == secao)
        applied_values["source_classification"] = "SERVER_REGISTERED_LIMITED_ACCEPTANCE_NOT_MOTOR_APPROVAL"
        applied_values["source_parameter_kinds"].update({
            "conductor_base_iz": "SERVER_REGISTERED_LIMITED_ACCEPTANCE",
            "correction_factor": "SERVER_REGISTERED_LIMITED_ACCEPTANCE",
        })
    item = {
        "trace_schema_version": 3 if binding is not None else 2,
        "limited_cell_binding": binding,
        "additional_implementation_sources": {
            "cell_bindings": sha256(getsource(cell_bindings).encode()).hexdigest(),
            "protection_checks": sha256(getsource(protection_checks).encode()).hexdigest(),
        },
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
    bound = item.get("trace_schema_version") == 3
    classification = ("SERVER_REGISTERED_LIMITED_ACCEPTANCE_NOT_MOTOR_APPROVAL" if bound
                      else "CLIENT_SUPPLIED_UNVERIFIED_NOT_NORMATIVE_CELL")
    if (item.get("calculation_trace_kind") != TYPE or
        not isinstance(item.get("values_actually_used_by_algorithm"), dict) or
        item["values_actually_used_by_algorithm"].get("source_classification") !=
        classification or
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
    if version not in (1, 2, 3):
        raise ValueError("Versao do formato de ensaio nao suportada")
    if version in (2, 3):
        used = item["values_actually_used_by_algorithm"]
        line = used.get("selected_input_row")
        if not isinstance(line, dict):
            raise ValueError("Linha de entrada realmente consumida ausente")
        expected_hash = sha256(_canonical(line).encode("utf-8")).hexdigest()
        if used.get("input_row_sha256") != expected_hash:
            raise ValueError("Hash da linha realmente consumida nao confere")
        origins = used.get("source_parameter_kinds")
        expected_origins = {
            "conductor_base_iz": "CLIENT_DECLARED",
            "correction_factor": "CLIENT_DECLARED",
            "resistance_ohm_km": "CLIENT_DECLARED",
        }
        if bound:
            expected_origins.update({"conductor_base_iz": "SERVER_REGISTERED_LIMITED_ACCEPTANCE",
                                     "correction_factor": "SERVER_REGISTERED_LIMITED_ACCEPTANCE"})
        if origins != expected_origins:
            raise ValueError("Fonte de parametros alterada sem homologacao")
        try:
            raw_row = item["entrada"]["tabela_condutores"][line["indice_entrada"]]
            matching = (Decimal(str(raw_row["secao_mm2"])) == Decimal(str(line["secao_mm2"]))
                        and Decimal(str(raw_row["capacidade_a"])) == Decimal(str(line["capacidade_a"])))
            expected_iz = Decimal(str(raw_row["capacidade_a"])) * Decimal(str(item["entrada"]["fator_correcao"]))
            actual_iz = Decimal(str(item["resultado"]["condutor"]["capacidade_decisao_a"]))
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ValueError("Linha/fator de entrada invalido no historico") from exc
        if (not matching or expected_iz != actual_iz or
                Decimal(str(item["resultado"]["condutor"]["secao_mm2"])) != Decimal(str(line["secao_mm2"]))):
            raise ValueError("Trilha de parametros nao corresponde ao calculo efetivo")
    if bound:
        _, expected_binding = cell_bindings.resolver_vinculo(item["entrada"])
        if (expected_binding is None or item.get("limited_cell_binding") != expected_binding or
                item["resultado"].get("vinculo_celulas") != expected_binding):
            raise ValueError("Vínculo de células do ensaio inconsistente")
        selected_id = next(c["id"] for c in expected_binding["celulas"]
                           if c["tabela"] == "36" and Decimal(c["linha"]) ==
                           Decimal(str(item["resultado"]["condutor"]["secao_mm2"])))
        if item["values_actually_used_by_algorithm"].get("selected_registered_capacity_cell_id") != selected_id:
            raise ValueError("ID da célula selecionada inconsistente")
    elif item.get("limited_cell_binding") is not None or item.get("entrada", {}).get("vinculo_celulas") is not None:
        raise ValueError("Vínculo exige formato de ensaio versionado")
    implementations = item.get("additional_implementation_sources")
    if implementations is not None:
        if (set(implementations) != {"cell_bindings", "protection_checks"} or
                any(not isinstance(h, str) or len(h) != 64 or
                    any(c not in "0123456789abcdef" for c in h) for h in implementations.values())):
            raise ValueError("Proveniência dos verificadores inválida")
        r = item["resultado"]
        expected_protection = protection_checks.verificar_sobrecarga(
            Decimal(str(item["entrada"]["corrente_a"])), Decimal(str(r["disjuntor"]["corrente_a"])),
            Decimal(str(r["condutor"]["capacidade_decisao_a"])), item["entrada"].get("protecao_sobrecarga"))
        if r.get("protecao_sobrecarga") != expected_protection:
            raise ValueError("Verificação de sobrecarga do ensaio inconsistente")
    if implementations is None and (
            bound or item.get("entrada", {}).get("protecao_sobrecarga") is not None or
            "protecao_sobrecarga" in item.get("resultado", {})):
        raise ValueError("Ensaio com células/proteção exige proveniência dos verificadores")
    return item
