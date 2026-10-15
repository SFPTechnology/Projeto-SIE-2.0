# SIE 2.0 — Marco 002: segurança, rastreabilidade e persistência local

## Situação
Incremento de desenvolvimento na branch de reestruturação, isolado da main. **Não corresponde a aprovação normativa nem a liberação profissional do software.**

## Implementação entregue

| Identificação | Entrega | Critério objetivo |
|---|---|---|
| SEG-01 | Gate conservador | Dados e testes autodeclarados pelo cliente nunca aprovam um cálculo |
| SEG-02 | Enquadramento EDP apenas consultivo | O retorno pode ter candidato para estudo, mas `liberado_para_padrao_entrada=false` |
| SEG-03 | Restrição CORS da API | Apenas interface local das portas previstas; não substitui autenticação |
| SEG-04 | Escape de HTML na interface | Valores externos são escapados antes de compor cartões |
| DAT-01 | SQLite local versionado | Revisão otimista, transação, rollback em conflito, trilha de eventos |
| DAT-02 | Limite do armazenamento | Projeto individual de no máximo 1 MiB de JSON |
| QA-01 | Testes de regressão | Incluem fraude por flags, fronteira CORS, valores não finitos e versões |
| QA-02 | CI | Testes pytest + análise de sintaxe do JavaScript via node --check |
| DOC-01 | Manual HTML para iniciantes | Guia navegável, campos, conceitos e limites |

## Decisões e critérios

- A função de seleção de condutores usa tabela informada pelo cliente; portanto o resultado é preliminar e não representa tabela normativa aprovada.
- O catálogo EDP já possui trilha documental interna em `Arquivos_Diversos/QA_CONFERENCIA_CERTFID_TABELAS_EDP.md`, mas o enquadramento automático por corrente não verifica todas as condições e não autoriza a execução.
- `EvidenciaNormativa.dados_validados` e `testes_independentes` continuam no modelo por compatibilidade com testes e clientes legados, mas são ignorados como autoridade de liberação.
- A persistência SQLite está exposta **somente em API local opcional**, bloqueada por padrão e exigindo `SIE_LOCAL_API_TOKEN` e `SIE_LOCAL_DB_PATH`. Essa proteção não substitui autenticação por usuário em produção.
- CORS limita a origem de páginas no navegador, mas não autentica requisições e não protege uma API publicada na internet.

## Próximos gates e bloqueios

| ID | Necessidade | Evidência para aceitar |
|---|---|---|
| SEC-05 | Autenticação e autorização no backend | Perfis, testes de acesso negado e auditoria da identidade |
| NOR-01 | Registro confiável de normas e tabelas | PDF/fonte oficial, edição, revisão, unidade, hash, recorte e conferência |
| NOR-02 | Aprovação independente por perfil autorizado | Assinatura/identidade auditável, vínculo a versão do motor, logs imutáveis |
| ENG-01 | Cálculos completos NBR 5410 | Casos de referência, limites, dimensões e tabelas versionadas |
| ENG-02 | Proteção completa | Sobrecarga, curto-circuito, DR, coordenação, seletividade e seccionamento |
| EDP-01 | Elegibilidade EDP além da corrente | Todas as condições exigidas, inclusive cargas de motores e modalidades |
| DAT-03 | Migração do armazenamento local para PostgreSQL | Migrações reversíveis, controle de acesso e backups |
| UX-02 | UI integrada com projetos e banco | Jornada ponta a ponta testada |
| DOC-02 | Desenhos, memoriais e quantitativos | Consistência com dados autoritativos e cálculo |
| QA-03 | Auditoria profissional de liberação | Testes normativos independentes, segurança, E2E e relatório |

## Política de publicação
Permanece proibido classificar o motor como normativamente aprovado. A branch `main` não deverá ser alterada antes da avaliação do PR, e o software existente não deve ser substituído automaticamente.

## Como verificar
No GitHub: PR #1, aba **Checks**. No Windows, siga `restructuring/README.md` e execute `python -m pytest -q` em `restructuring/apps/api`. Os testes de API/armazenamento e o comando `node --check restructuring/apps/web/app.js` estão incorporados à integração contínua.

## Extensão matemática não normativa

Adicionada a função `calcular_queda_tensao_trifasica_resistiva` como primitiva isolada do domínio, com hipóteses explícitas de equilíbrio de fases, `cos(phi)=1` e reatância nula. Testes cobrem valor numérico, proporcionalidade com comprimento e rejeição de parâmetros não finitos. Essa função não é exposta como aprovação nem substitui o motor de queda de tensão conforme a NBR 5410.
