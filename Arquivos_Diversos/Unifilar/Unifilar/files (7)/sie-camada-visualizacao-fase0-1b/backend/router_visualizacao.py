"""
SIE — Endpoint da Camada de Visualização (PRD Seção 2.2).

GET /api/v1/projetos/{id}/visualizacao
→ JSON com o contrato de circuito canônico, consumido por:
  - Camada A (Fable 5): fetch JSON, renderiza dashboards/stories.
  - Camada B (SVG próprio): props dos componentes React.

Nenhuma camada armazena dados — o backend é a fonte única de verdade.
O payload é determinístico (sem timestamps, ordenação estável) para
suportar o RNF-03 (mesma entrada → mesmo SVG byte-identical).
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from .adaptador_1x1 import adaptar_projeto
from .contrato_circuito import CircuitoCanonico, PontoCarga

router = APIRouter(prefix="/api/v1/projetos", tags=["visualizacao"])


class PayloadVisualizacao(BaseModel):
    model_config = ConfigDict(frozen=True)

    projeto_id: str
    origem: str = Field(
        description="'adaptador-1:1' (árvore provisória, R-04) ou 'divisao-circuitos'"
    )
    provisorio: bool = Field(
        description="True => todo artefato visual DEVE exibir a nota 'Árvore provisória'"
    )
    total_circuitos: int
    circuitos: list[CircuitoCanonico]


# Repositório de pontos: injete aqui o acesso real (SQLAlchemy) do SIE.
# A assinatura esperada é: carregar_pontos(projeto_id) -> list[PontoCarga]
_carregar_pontos = None  # type: ignore[assignment]


def registrar_repositorio(fn) -> None:
    """Ponto de integração: o app principal registra o loader real de pontos."""
    global _carregar_pontos
    _carregar_pontos = fn


@router.get("/{projeto_id}/visualizacao", response_model=PayloadVisualizacao)
def obter_visualizacao(projeto_id: str) -> PayloadVisualizacao:
    if _carregar_pontos is None:
        raise HTTPException(503, "Repositório de pontos não registrado no router de visualização.")
    pontos: list[PontoCarga] = _carregar_pontos(projeto_id)
    if not pontos:
        raise HTTPException(404, f"Projeto '{projeto_id}' sem pontos de carga cadastrados.")
    circuitos = adaptar_projeto(pontos)
    return PayloadVisualizacao(
        projeto_id=projeto_id,
        origem="adaptador-1:1",
        provisorio=True,
        total_circuitos=len(circuitos),
        circuitos=circuitos,
    )
