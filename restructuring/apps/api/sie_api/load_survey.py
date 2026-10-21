"""F04 preliminary survey: no normative defaults or circuit model replacement."""
from decimal import Decimal, localcontext
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator

class Record(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True, allow_inf_nan=False)
    id: UUID
    nome: str = Field(min_length=1, max_length=160)
    arquivado: bool = False

class Building(Record):
    pass

class Floor(Record):
    edificacao_id: UUID

class Room(Record):
    pavimento_id: UUID
    tipo: str = Field(min_length=1, max_length=80)
    uso: str = Field(default='', max_length=200)
    condicao: Literal['seco', 'molhado', 'outro'] = 'seco'
    area_m2: Decimal | None = Field(default=None, gt=0, le=10000000)
    perimetro_m: Decimal | None = Field(default=None, gt=0, le=1000000)

class Load(Record):
    ambiente_id: UUID
    classe: Literal['ILUMINACAO', 'TUG', 'TUE']
    quantidade: int = Field(default=1, ge=1, le=100000, strict=True)
    p_w: Decimal | None = Field(default=None, ge=0, le=1000000000)
    q_var: Decimal | None = Field(default=None, ge=0, le=1000000000)
    s_va: Decimal | None = Field(default=None, ge=0, le=1000000000)
    potencia_placa_w: Decimal | None = Field(default=None, ge=0, le=1000000000)
    potencia_atribuida_va: Decimal | None = Field(default=None, ge=0, le=1000000000)
    origem: Literal['declarado', 'estimado'] = 'declarado'
    fonte_regra: str = Field(default='', max_length=500)
    tensao_v: Decimal | None = Field(default=None, gt=0, le=100000)
    fases: Literal[1, 2, 3] | None = None
    corrente_placa_a: Decimal | None = Field(default=None, ge=0, le=1000000)
    fator_potencia: Decimal | None = Field(default=None, gt=0, le=1)
    regime: str = Field(default='', max_length=160)
    circuito_preliminar: str = Field(default='', max_length=160)
    dedicado: bool | None = None
    posicao: str = Field(default='', max_length=160)
    comandos: str = Field(default='', max_length=160)
    categoria: str = Field(default='', max_length=100)
    tags: list[str] = Field(default_factory=list, max_length=30)

class Survey(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    schema_version: Literal['F04-1'] = 'F04-1'
    projeto_id: UUID
    nome: str = Field(min_length=1, max_length=160)
    cliente: str = Field(default='', max_length=200)
    endereco: str = Field(default='', max_length=500)
    tipologia: str = Field(default='', max_length=160)
    edificacoes: list[Building] = Field(default_factory=list, max_length=1000)
    pavimentos: list[Floor] = Field(default_factory=list, max_length=10000)
    ambientes: list[Room] = Field(default_factory=list, max_length=10000)
    cargas: list[Load] = Field(default_factory=list, max_length=20000)

    @model_validator(mode='after')
    def links(self):
        groups = [self.edificacoes, self.pavimentos, self.ambientes, self.cargas]
        ids = [item.id for group in groups for item in group]
        if len(ids) != len(set(ids)):
            raise ValueError('Identificadores duplicados')
        for children, parents, field in [(self.pavimentos, self.edificacoes, 'edificacao_id'),
                                          (self.ambientes, self.pavimentos, 'pavimento_id'),
                                          (self.cargas, self.ambientes, 'ambiente_id')]:
            lookup = {x.id: x for x in parents}
            for child in children:
                parent = lookup.get(getattr(child, field))
                if parent is None or (parent.arquivado and not child.arquivado):
                    raise ValueError('Vínculo ausente ou filho ativo de item arquivado')
        return self


def summarize(survey: Survey):
    active = [c for c in survey.cargas if not c.arquivado]
    issues = []
    for c in active:
        missing = [f for f in ['tensao_v', 'fases'] if getattr(c, f) is None]
        if all(getattr(c, f) is None for f in ['p_w', 's_va']):
            missing.append('potencia P ou S')
        if c.classe == 'TUE':
            missing += [f for f in ['regime', 'dedicado'] if getattr(c, f) in (None, '')]
        if missing:
            issues.append({'id': str(c.id), 'codigo': 'DADOS_INCOMPLETOS', 'campos': missing})
        if c.s_va is not None and ((c.p_w is not None and c.p_w > c.s_va) or
           (c.q_var is not None and c.q_var > c.s_va) or
           (c.p_w is not None and c.q_var is not None and
            abs(c.s_va*c.s_va - c.p_w*c.p_w - c.q_var*c.q_var) > max(Decimal('0.01'), c.s_va*c.s_va*Decimal('0.01')))):
            issues.append({'id': str(c.id), 'codigo': 'POTENCIAS_INCONSISTENTES'})
        if c.p_w is not None and c.s_va is not None and c.s_va > 0 and c.fator_potencia is not None and abs(c.p_w / c.s_va - c.fator_potencia) > Decimal('0.01'):
            issues.append({'id': str(c.id), 'codigo': 'FATOR_POTENCIA_INCONSISTENTE'})
    names = set()
    for c in active:
        key = (c.ambiente_id, c.nome.casefold())
        if key in names:
            issues.append({'id': str(c.id), 'codigo': 'POSSIVEL_DUPLICIDADE'})
        names.add(key)
    def exact_total(loads, field):
        with localcontext() as ctx:
            ctx.prec = max(80, max((len(getattr(c, field).as_tuple().digits) + abs(getattr(c, field).as_tuple().exponent) for c in loads), default=0) + 20)
            return str(sum((getattr(c, field)*c.quantidade for c in loads), Decimal(0)))
    def totals(loads):
        result = {}
        for field, unit in [('p_w','W'), ('q_var','var'), ('s_va','VA')]:
            known = [c for c in loads if getattr(c, field) is not None]
            result[field] = {'valor': exact_total(known, field),
                             'unidade': unit, 'cargas_sem_dado': len(loads)-len(known)}
        return result
    floor_for = {r.id: r.pavimento_id for r in survey.ambientes}
    return {'contrato': 'EP03-EP04-F04-1', 'total': totals(active),
            'por_ambiente': {str(r.id): totals([c for c in active if c.ambiente_id == r.id]) for r in survey.ambientes if not r.arquivado},
            'por_pavimento': {str(f.id): totals([c for c in active if floor_for[c.ambiente_id] == f.id]) for f in survey.pavimentos if not f.arquivado},
            'nomes_ambientes': {str(r.id): r.nome for r in survey.ambientes},
            'nomes_pavimentos': {str(f.id): f.nome for f in survey.pavimentos},
            'pendencias': issues, 'regras_minimas': 'PENDENTE_FONTE_VALIDADA',
            'conformidade_normativa': False, 'fator_demanda_aplicado': False}


def persist(repo, project_id, survey, expected):
    if str(survey.projeto_id) != str(project_id):
        raise ValueError('Levantamento pertence a outro projeto')
    previous = repo.carregar(str(project_id))
    data = {} if previous is None else dict(previous['dados'])
    old = data.get('levantamento', {})
    for group in ['edificacoes', 'pavimentos', 'ambientes', 'cargas']:
        previous_items = old.get(group, []) if isinstance(old, dict) else []
        if isinstance(previous_items, list):
            old_ids = {str(x['id']) for x in previous_items if isinstance(x, dict) and 'id' in x}
            if not old_ids.issubset({str(x.id) for x in getattr(survey, group)}):
                raise ValueError('Exclusão silenciosa recusada; arquive explicitamente o item')
    data['levantamento'] = survey.model_dump(mode='json')
    data['levantamento_resultados_invalidos'] = True
    revision = repo.salvar(str(project_id), survey.nome, data, expected)
    return {'id': str(project_id), 'revisao': revision, 'resumo': summarize(survey)}
