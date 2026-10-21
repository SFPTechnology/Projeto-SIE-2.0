# F02 — Contratos implementados dos motores e do modelo
Data: 20/10/2026. Versão: SIE_INSTALLATION_V1 / SIE_SNAPSHOT_V1 / SIE_CALCULATION_RECORD_V1.

## Interfaces executáveis

| Interface | Operação | Contrato |
|---|---|---|
| POST /api/v1/modelo/validar | Validar agregado | Installation; identidade/revisão, sem cálculo |
| POST /api/v1/modelo/snapshots | Capturar revisão por valor | Installation → InstallationSnapshot com JSON canônico e SHA-256 |
| POST /api/v1/modelo/ensaiar-legado | Adaptar circuito ao motor atual | LegacyAnalysisRequest → CalculationRecord |
| POST /api/v1/modelo/invalidacao | Avaliar dependências atuais | InvalidationRequest → VALID/PENDING/INVALID/STALE |
| POST /api/v1/modelo/referencias/validar | Confrontar referência de documento/cálculo | Mesmo projeto, revisão e hash |
| PUT /api/v1/local/projetos/{project_id}/modelo | Persistir snapshot | Token local obrigatório; próxima revisão esperada; conflito409 |

OpenAPI executável: `OPENAPI_F02.json`. Schema tipado: `MODELO_INSTALACAO_SCHEMA.json`. As rotas públicas do modelo são stateless: não gravam dados ou autenticam a origem dos documentos. A persistência usa o armazenamento local já existente, seu token e suas revisões imutáveis.

## CLI primeiro

`python -m sie_api.cli modelo --arquivo entrada.json --operacao validar|snapshot|ensaiar-legado|invalidacao|referencia`

Cada operação recebe o mesmo DTO da respectiva rota HTTP e usa o serviço diretamente, sem navegador ou servidor. O subcomando modelo não exige banco para operações stateless. A persistência pode reutilizar a CLI salvar com dados locais ou a rota PUT autenticada.

## Grandezas e erros

Magnitudes são texto decimal com unidade explícita, não float binário. Tensão inclui base FN/FF; P/W, Q/var e S/VA têm tipos diferentes. Conversão deve ocorrer explicitamente antes do contrato. Entradas com booleanos no lugar de fases, unidades erradas, não finitos, excesso de precisão computacional ou referências incoerentes são recusadas. Limite de recurso:1000 dígitos e expoente absoluto1000 por magnitude; não é limite normativo.

HTTP422 para violações; HTTP401/503 para armazenamento não autorizado/desabilitado; HTTP409 para conflito de revisão. Erros de domínio do adaptador têm código LEGACY_MODEL_INCOMPATIBLE, referências REVISION_REFERENCE_MISMATCH e gravação SNAPSHOT_REFERENCE_INVALID/REVISION_CONFLICT. Erros de validação incluem localização/tipo/mensagem sem repetir dados brutos. CLI retorna2 para dados inválidos.

## Fronteira de compatibilidade

O adaptador aceita um percurso monofásico homogêneo, compara exatamente corrente, tensão, soma de comprimentos, seção selecionada e corrente nominal do dispositivo quando declarada. Soma decimal usa precisão local suficiente sem arredondar decisões. O motor original e suas respostas são preservados. Não altera o circuito para acomodar o resultado.

Recusa circuito trifásico, percursos múltiplos/ramificados, condições distintas, impedância canônica declarada e parâmetros complementares/vínculo F01 sem mapeamento explícito. Esses cenários continuam representáveis no modelo; o adaptador não finge que o motor resistivo os processa. As rotas F01 originais permanecem disponíveis, inclusive verificações complementares. Capacidades/fator/resistência de entrada são declarações não verificadas: o adaptador não confirma correspondência normativa da tabela a material/isolação ou instalação.

## Proveniência e significado de VALID

CalculationRecord armazena snapshot/revisão/circuito, hash da entrada e resultado JSON/hash. Identidade do algoritmo inclui corpos/módulos executados e valores reais do catálogo de disjuntores, além da versão do adaptador. Alterações nesses dados invalidam a correspondência. Resultados não-objeto, incompletos, com grandezas inválidas ou flags de aprovação são rejeitados.

VALID significa apenas integridade e correspondência de dependências computacionais declaradas. A rota de invalidação recebe um registro do cliente e não autentica sua origem por assinatura. Não concede aprovação normativa; `normative_conformity_verified=false`. A revisão F02 avalia modelagem e compatibilidade de software.
