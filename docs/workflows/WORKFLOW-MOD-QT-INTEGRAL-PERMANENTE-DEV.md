# Workflow MOD-QT Integral e Permanente para @dev

**Status:** Ready for Execution  
**Responsavel principal:** @dev (Dex)  
**Quality gate:** @qa (Quinn)  
**Fechamento remoto/deploy:** @devops (Gage)  
**Data:** 2026-07-30  
**Escopo:** tornar o modulo de queda de tensao visivel, navegavel, testavel e publicavel de forma permanente no sistema SIE.

## 1. Objetivo

Garantir que o MOD-QT (queda de tensao) nao fique apenas implementado no codigo, mas apareca e funcione no sistema real em todos os caminhos esperados:

1. Dominio e servicos continuam operacionais.
2. Rotas UI e API continuam registradas.
3. Navegacao ate o modulo fica disponivel no fluxo do usuario.
4. Rotas profundas funcionam em ambiente local, SPA estatico e SSR/producao.
5. Build usado para deploy contem o modulo.
6. Pacotes de deploy antigos deixam de ser fonte de verdade.
7. Gates automatizados impedem que o modulo suma de novo.

## 2. Diagnostico de origem

Achados ja confirmados:

- A rota de destino existe: `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx`.
- A rota esta registrada em `src/routeTree.gen.ts` e `src/routeTree.spa.ts`.
- O link "Queda de tensão" existe em `src/routes/projetos.$projetoId.tsx`, dentro de `deps-hero-links`.
- O link existe apenas no detalhe do projeto (`/projetos/:projetoId`), nao no cabecalho global.
- `AppShell.tsx` tem apenas link para a home, sem menu global de modulos.
- `dist` contem `queda-tensao`, mas pacotes antigos como `hostinger-spa`, `hostinger-deploy*` e `export` nao contem a rota completa.
- Servir `dist` com `http-server` sem fallback SPA retorna `404` em rotas profundas como `/projetos/demo/queda-tensao`.

Conclusao: o problema nao e ausencia completa do modulo. O problema e permanencia operacional: exposicao, fallback de rota, build/deploy canonico e regressao.

## 3. Pre-condicoes para @dev

@dev so deve iniciar implementacao se houver story `Ready` em `docs/stories/`.

Story recomendada:

```text
docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md
```

Se a story nao existir ou estiver `Draft`, parar e devolver para @sm/@po:

```text
BLOCKED: STORY_REQUIRED
```

## 4. Escopo IN

@dev deve implementar somente itens cobertos pela story:

- tornar a entrada do modulo visivel no fluxo principal;
- consolidar navegacao para `/projetos/$projetoId/queda-tensao`;
- garantir que a rota profunda funcione em servidor SPA estatico com fallback para `index.html`;
- garantir que `npm run build` e `npm run build:spa` gerem artefatos contendo o modulo;
- criar script ou documentacao executavel para servir o build local corretamente;
- adicionar testes de regressao que verifiquem rota, link, build e artefatos;
- atualizar story: checkboxes, Dev Agent Record, File List, Debug Log, Change Log e Status.

## 5. Escopo OUT

@dev nao deve:

- alterar formulas, criterios normativos ou contrato publico de MOD-QT;
- promover valores `[VERIFICAR]` para `CONFIRMADO`;
- alterar `RetornoMODQT`, schemas Zod ou endpoints publicos sem story propria;
- reordenar fluxo de negocio alem do que a story autorizar;
- executar `git push`, PR, merge, tag, release ou deploy;
- tratar diretorios antigos de deploy como fonte canonica sem decisao de @devops.

## 6. Arquivos alvo

Arquivos provaveis para leitura/edicao:

- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.gen.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routeTree.spa.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/AppShell.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/router.spa.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/vite.spa.config.ts`
- `sistema-de-instala-es-el-tricas-sie-main/package.json`
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/`
- `sistema-de-instala-es-el-tricas-sie-main/tests/`
- `docs/stories/story-MOD-QT-3-01-modulo-integral-permanente.md`

@dev deve preservar mudancas nao relacionadas ja presentes na worktree.

## 7. Workflow @dev

### Fase 1 - Preflight

Executar:

```powershell
git status --short
cd sistema-de-instala-es-el-tricas-sie-main
npm run typecheck
npm test -- --runInBand
```

Se `npm test -- --runInBand` nao for suportado pelo Vitest, usar:

```powershell
npm test
```

Registrar baseline na story:

- branch;
- arquivos modificados preexistentes;
- quantidade de testes passando;
- qualquer caveat ambiental, especialmente CRLF/prettier.

### Fase 2 - Confirmar estado atual do MOD-QT

Verificar com `rg`:

```powershell
rg -n "Queda de tens|queda-tensao|deps-hero-links" src tests
rg -n "queda-tensao" src/routeTree.gen.ts src/routeTree.spa.ts
```

Saida esperada:

- rota UI presente;
- rota API de resumo/lote presente;
- link presente no hub do projeto;
- testes existentes de queda de tensao presentes.

Se algum item basico estiver ausente, @dev deve tratar como regressao dentro da story.

### Fase 3 - Exposicao permanente no produto

Implementar a solucao definida pela story. A recomendacao tecnica e:

1. Manter o link atual no hub do projeto.
2. Garantir que ele seja `Link` do TanStack Router:

```tsx
<Link
  to="/projetos/$projetoId/queda-tensao"
  params={{ projetoId }}
  className="deps-hero-link"
>
  Queda de tensão
</Link>
```

3. Se a story exigir acesso global, criar um componente pequeno e reutilizavel para navegacao de modulos do projeto, evitando duplicar strings de rota.
4. Nao adicionar link global sem `projetoId`; se nao houver projeto ativo, o link global deve permanecer indisponivel ou apontar para selecao de projeto.
5. Se houver menu lateral/topbar por projeto, a entrada "Queda de tensão" deve aparecer junto dos demais modulos.

Regra de produto: MOD-QT e um modulo dependente de projeto. Ele nao deve aparecer como acao executavel fora do contexto de um projeto selecionado.

### Fase 4 - Rota profunda e fallback SPA

Corrigir o problema de `404` em servidor estatico para rotas profundas.

@dev deve escolher uma abordagem simples e rastreavel:

1. Criar script local de preview SPA com fallback para `index.html`; ou
2. Ajustar documentacao/script de deploy SPA para usar servidor com fallback; ou
3. Gerar artefato Hostinger com `.htaccess`/rewrite correto se essa for a estrategia vigente do projeto.

Requisitos:

- `/` responde `200`.
- `/projetos/<id>` responde `200` no modo SPA.
- `/projetos/<id>/queda-tensao` responde `200` no modo SPA.
- assets em `/assets/*.js` e `/assets/*.css` continuam respondendo `200`.

Nao basta o bundle conter `queda-tensao`; a rota profunda precisa abrir quando o usuario recarrega a pagina ou cola a URL.

### Fase 5 - Build canonico e artefatos permanentes

@dev deve definir, na story, qual build e canonico para cada uso:

- Desenvolvimento local: `npm run dev` ou fallback documentado se TanStack Start travar.
- Producao SSR: `npm run build` + `npm run start`.
- Producao SPA/Hostinger: `npm run build:spa` + artefato com fallback.

Se diretorios antigos de deploy (`hostinger-spa*`, `hostinger-deploy*`, `export`) estiverem obsoletos:

- nao editar todos indiscriminadamente;
- documentar na story que eles nao sao canonicos;
- se a story exigir, criar um unico script de geracao canonica, por exemplo `npm run build:hostinger`, que limpa e gera apenas o artefato oficial.

Critério permanente:

```text
rg "queda-tensao" <artefato-canonico>
rg "Queda de tens" <artefato-canonico>
```

Ambos devem encontrar resultado no artefato final usado para deploy.

### Fase 6 - Testes obrigatorios

Criar ou atualizar testes sem instalar infraestrutura nova desnecessaria.

Testes minimos:

1. Teste de fonte do hub:
   - `src/routes/projetos.$projetoId.tsx` contem "Queda de tensão";
   - contem `to="/projetos/$projetoId/queda-tensao"`;
   - ordem entre links permanece correta.

2. Teste de route tree:
   - `src/routeTree.gen.ts` contem `/projetos/$projetoId/queda-tensao`;
   - `src/routeTree.spa.ts` contem `/projetos/$projetoId/queda-tensao`.

3. Teste de artefato:
   - apos build canonico, bundle contem `queda-tensao`;
   - bundle contem label "Queda de tensão" ou representacao minificada equivalente.

4. Teste de fallback SPA:
   - servidor local de preview canonico responde `200` para `/projetos/demo/queda-tensao`;
   - `index.html` e assets respondem corretamente.

5. Testes existentes de MOD-QT:
   - nao reduzir cobertura;
   - nao alterar snapshots VRT sem comando explicito e registro no File List.

Se o projeto continuar sem jsdom/happy-dom/testing-library, usar os padroes existentes:

- `readFileSync` para assercao de fonte;
- `renderToStaticMarkup` apenas para componentes puros exportados;
- testes de processo/build com Node/Vitest quando necessario.

### Fase 7 - Validacoes completas

Rodar no subprojeto:

```powershell
cd sistema-de-instala-es-el-tricas-sie-main
npm run lint
npm run typecheck
npm test
npm run build
npm run build:spa
```

Depois validar artefato:

```powershell
rg "queda-tensao" dist
rg "Queda de tens" dist
```

Se houver artefato Hostinger canonico, validar tambem:

```powershell
rg "queda-tensao" <diretorio-hostinger-canonico>
rg "Queda de tens" <diretorio-hostinger-canonico>
```

### Fase 8 - Teste local no navegador

@dev deve iniciar o servidor adequado e registrar URL:

SSR:

```powershell
npm run build
$env:PORT="4181"
npm run start
```

SPA com fallback:

```powershell
npm run build:spa
npm run preview:spa
```

Validar manualmente ou por browser tool:

1. Abrir `/`.
2. Criar ou selecionar um projeto.
3. Entrar em `/projetos/:projetoId`.
4. Confirmar link "Queda de tensão" visivel.
5. Clicar no link.
6. Confirmar tela MOD-QT carregada.
7. Recarregar a pagina em `/projetos/:projetoId/queda-tensao`.
8. Confirmar que nao volta 404.

### Fase 9 - Story updates

@dev pode atualizar apenas as secoes permitidas:

- Tasks / Subtasks checkboxes;
- Dev Agent Record;
- Debug Log References;
- Completion Notes List;
- File List;
- Change Log;
- Status.

Status final esperado:

```text
Ready -> InProgress -> InReview
```

@dev nao deve marcar `Done`; isso e autoridade de @qa.

## 8. Acceptance Criteria recomendados para a story

### AC1 - Modulo aparece no fluxo do projeto

Given um projeto existente  
When o usuario abre `/projetos/:projetoId`  
Then a acao "Queda de tensão" aparece junto dos demais modulos do projeto  
And aponta para `/projetos/:projetoId/queda-tensao`.

### AC2 - Rota do modulo carrega por navegacao

Given o usuario esta no detalhe do projeto  
When clica em "Queda de tensão"  
Then a tela do MOD-QT e renderizada sem erro.

### AC3 - Rota profunda carrega por refresh

Given o build SPA/producao esta sendo servido  
When o usuario acessa diretamente `/projetos/:projetoId/queda-tensao`  
Then o servidor entrega a aplicacao e o router renderiza a rota correta  
And nao retorna `404`.

### AC4 - Artefato de deploy contem MOD-QT

Given o build canonico de deploy foi gerado  
When o artefato e inspecionado  
Then `queda-tensao` esta presente no bundle final  
And o label "Queda de tensão" ou equivalente esta presente.

### AC5 - Builds antigos nao mascaram o modulo

Given existem diretorios antigos de deploy  
When o workflow finaliza  
Then a story declara qual diretorio/script e canonico  
And qualquer artefato obsoleto fica documentado como nao fonte de verdade ou e substituido pelo artefato canonico autorizado.

### AC6 - Gates tecnicos passam

Given a implementacao final  
When @dev roda os gates  
Then `npm run lint`, `npm run typecheck`, `npm test`, `npm run build` e `npm run build:spa` passam ou qualquer caveat ambiental fica comprovado e aceito pela story/QA.

## 9. Definition of Done para @dev

- [ ] Story `MOD-QT-3-01` esta `InReview`.
- [ ] Link/entrada de MOD-QT visivel no fluxo autorizado.
- [ ] Rota `/projetos/:projetoId/queda-tensao` registrada em SSR e SPA.
- [ ] Rota profunda responde sem 404 no modo de preview/deploy definido.
- [ ] Build canonico contem `queda-tensao`.
- [ ] Artefato de deploy canonico definido.
- [ ] Testes de regressao adicionados.
- [ ] `npm run lint` executado.
- [ ] `npm run typecheck` executado.
- [ ] `npm test` executado.
- [ ] `npm run build` executado.
- [ ] `npm run build:spa` executado.
- [ ] File List da story atualizado.
- [ ] Nenhuma alteracao fora de escopo foi feita.
- [ ] Handoff para @qa criado.

## 10. Handoff para @qa

Ao finalizar, @dev deve registrar:

```yaml
from_agent: "@dev"
to_agent: "@qa"
story: "MOD-QT-3-01"
last_command: "*develop-yolo"
status: "InReview"
evidence:
  - lint
  - typecheck
  - test
  - build
  - build_spa
  - route_deep_link_200
  - artifact_contains_queda_tensao
```

## 11. Handoff para @devops

Somente apos QA `PASS` ou `CONCERNS` aceito:

```text
@devops *pre-push
```

@devops deve:

- rodar gates de pre-push;
- confirmar artefato canonico de deploy;
- preparar push/PR;
- executar push/PR/deploy apenas mediante pedido explicito do usuario.

## 12. Comando recomendado para iniciar

```text
@dev
*develop-yolo story-MOD-QT-3-01-modulo-integral-permanente
```

Se a story ainda nao existir:

```text
@sm
Criar story MOD-QT-3-01 a partir de docs/workflows/WORKFLOW-MOD-QT-INTEGRAL-PERMANENTE-DEV.md
```

