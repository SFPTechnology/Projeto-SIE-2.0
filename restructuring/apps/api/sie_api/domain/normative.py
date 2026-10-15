"""Catálogo de candidatos normativos; nenhum valor de tabela é aprovado aqui.

Um match de contexto não atesta conformidade nem autoriza cálculo normativo.
Apenas dados publicados e validados por processo confiável poderiam mudar este gate.
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class NormativeRecord:
    id: str
    document: str
    edition: str
    subject: str
    typologies: tuple[str, ...] = ("residencial", "comercial", "predial")
    uf: Optional[str] = None
    distributor: Optional[str] = None
    effective_from: Optional[date] = None
    effective_until: Optional[date] = None
    verified_data: bool = False

# Metadados editoriais identificados, não transcrições ou tabelas certificadas.
# NR-10: transição da Portaria MTE 737/2026; conferir exceções de instalações existentes.
RECORDS = (
    NormativeRecord("ABNT-NBR-5410", "ABNT NBR 5410", "2004 corrigida 2008",
                    "Instalações de baixa tensão; escopo técnico a conferir"),
    *(NormativeRecord(f"ABNT-NBR-5419-{i}", f"ABNT NBR 5419-{i}",
                      "2026 corrigida 2026", "SPDA; depende de análise técnica de risco")
      for i in range(1, 5)),
    NormativeRecord("NR-10-ATE-2027", "NR-10", "Redação anterior à Portaria MTE 737/2026",
                    "Segurança de serviços e instalações",
                    effective_until=date(2027, 5, 31)),
    NormativeRecord("NR-10-A-PARTIR-2027", "NR-10", "Portaria MTE 737/2026",
                    "Segurança de serviços e instalações",
                    effective_from=date(2027, 6, 1)),
    NormativeRecord("EDP-SP-PTDT00068-V09", "EDP PT.DT.PDN.00068", "v09 candidata",
                    "Padrão de entrada; concessão exata por confirmar",
                    uf="SP", distributor="EDP_SP"),
)

@dataclass(frozen=True)
class Context:
    typology: str
    uf: str
    voltage_v: float
    reference_date: date
    distributor: Optional[str] = None
    material: Optional[str] = None
    installation_method: Optional[str] = None
    use: Optional[str] = None

def inspect_record(record: NormativeRecord, ctx: Context) -> dict:
    """Somente metadados confiáveis do servidor; nunca flags de aprovação do cliente."""
    reasons = []
    if ctx.typology not in record.typologies:
        return _decision(record, "NAO_APLICAVEL", ["TIPOLOGIA_FORA_DO_RECORTE"])
    if record.uf is not None and ctx.uf != record.uf:
        return _decision(record, "NAO_APLICAVEL", ["UF_FORA_DO_RECORTE"])
    if record.effective_from and ctx.reference_date < record.effective_from:
        return _decision(record, "NAO_APLICAVEL", ["ANTES_DA_VIGENCIA"])
    if record.effective_until and ctx.reference_date > record.effective_until:
        # NR-10 2026 prevê regra transitória para instalações existentes.
        # Não presumir que o regime anterior deixou de importar para todos os casos.
        if record.id == "NR-10-ATE-2027":
            return _decision(record, "PENDENTE", ["TRANSICAO_INSTALACOES_EXISTENTES_A_CONFERIR"])
        return _decision(record, "NAO_APLICAVEL", ["APOS_A_VIGENCIA"])
    if record.distributor is not None and ctx.distributor is None:
        return _decision(record, "PENDENTE", ["DISTRIBUIDORA_NAO_INFORMADA"])
    if record.distributor is not None and ctx.distributor != record.distributor:
        return _decision(record, "NAO_APLICAVEL", ["DISTRIBUIDORA_DIFERENTE"])
    if not record.verified_data:
        reasons.append("FONTE_E_REGRAS_NAO_HOMOLOGADAS")
    if record.distributor:
        reasons.append("AREA_CONCESSAO_NAO_VERIFICADA")
    if record.document.startswith("ABNT NBR 5419"):
        reasons.append("AVALIACAO_SPDA_PENDENTE")
    if record.document == "NR-10":
        reasons.append("TRANSICAO_E_EXCECOES_A_VERIFICAR")
    return _decision(record, "BLOQUEADO", reasons)

def _decision(record: NormativeRecord, status: str, reasons: list[str]) -> dict:
    return {"rule_id": record.id, "document": record.document, "edition": record.edition,
            "status": status, "reasons": reasons,
            "normative_approved": False, "verified_data": False}
