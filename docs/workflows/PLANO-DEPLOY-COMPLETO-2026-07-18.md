# Plano de Deploy Completo — SIE (2026-07-18)

**De:** @dev (Dex)
**Para:** @devops (Gage)
**Origem:** Varredura completa do repositório solicitada pelo usuário
**Escopo:** Sincronizar trabalho pendente no Git + publicar build atual em produção (Hostinger)

---

## 1. Achados da varredura

### 1.1 Topologia do repositório

O diretório raiz é o workspace do framework **Synkra AIOX** (stories, agentes, `.aiox-core/`). A aplicação real que vai para produção **não vive na raiz** — vive em:

```
sistema-de-instala-es-el-tricas-sie-main/
```

Esse diretório está registrado no índice do Git como **gitlink (submodule) órfão** — modo `160000`, commit `9df01a4d...`, mas **não existe `.gitmodules`**. É por isso que `git status` mostra `m sistema-de-instala-es-el-tricas-sie-main` (modificado, sem rastreamento normal de arquivos internos). Isso precisa ser resolvido antes de qualquer push confiável (ver Seção 4, Ação 0).

### 1.2 Stack da aplicação (`sistema-de-instala-es-el-tricas-sie-main/`)

- **Framework:** TanStack Start (React) + Vite. Dois modos de build:
  - **SSR** (`vite.config.ts`, entry `src/start.ts`/`src/server.ts`) — dev local com Node.
  - **SPA estático** (`vite.spa.config.ts`, entry `src/main-spa.tsx`) — **é o que vai para produção** (Hostinger não roda Node).
- **Package manager:** bun (`bun.lock` presente); pnpm também presente (`pnpm-lock.yaml`) — **dois lockfiles coexistindo**, risco de drift de dependências (flag para @qa/@architect, fora do escopo deste deploy).
- **Backend:** Supabase (projeto `hlbksclcandbsyqrsbmx`), acessado via `supabaseBrowser()` (anon key, RLS) no SPA e `supabaseAdmin()` (service role) no SSR.
- **Testes:** Vitest (`npx vitest run`), lint ESLint, typecheck `tsc --noEmit`.
- **CI/CD:** inexistente (`.github/workflows/` não tem pipelines) — todo o deploy é **manual**.

### 1.3 Estado do Git (raiz)

- Branch `master`, 2 commits (`a5631d5` MOD-DC v3.0 QA PASS 637/637, `2d0e432` init AIOX).
- **Working tree sujo** com volume grande de trabalho não commitado:
  - `src/` (raiz) — 3 arquivos novos (`otimizador.ts`, teste, schema) referentes a AUTO-OTI, ainda **não integrados** ao `sistema-de-instala-es-el-tricas-sie-main/src/`.
  - `supabase/migrations/` (raiz) — 2 migrations novas (`20260716_001_dependencia_retornos_downstream`, `20260717_001_dimensionamento_condutores_overrides`). **Já existem equivalentes aplicados** em `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/0009_*` e `0010_*` (mesmo conteúdo lógico, numeração paralela) — checar duplicidade antes de aplicar no Supabase.
  - Múltiplas stories novas em `docs/stories/` (EPIC-MOD-CC-SEC-QT, EPIC-MOD-DC-HYBRID, AUTO-OTI-1.1/1.2, etc.) e `docs/workflows/` — documentação, sem impacto direto em runtime.
  - `.claude/scheduled_tasks.lock` foi **deletado** localmente (D) — confirmar se é intencional antes do commit.
  - `.gitignore` e `AGENTS.md` modificados.
- Memória de sessões anteriores confirma: stories MOD-DC-HYBRID, MOD-CC/SEC/QT e AUTO-OTI 1.1/1.2 estão **Done com QA PASS**, mas **nunca foram commitadas/pushadas** (checkpoint pendente há múltiplas sessões).

### 1.4 Estado de build da aplicação

- `dist/client` e `dist/server` existem localmente (build SSR já gerado, `jul 17 22:11`).
- Pacotes de deploy antigos presentes: `hostinger-deploy/`, `hostinger-deploy-lite/`, `hostinger-deploy-minimal/`, `hostinger-staging/`, `hostinger-spa.zip` — **múltiplos artefatos de tentativas anteriores**, não fica claro qual foi o último efetivamente publicado. Recomenda-se limpar os obsoletos após o deploy validado.
- `README-HOSTINGER.md` documenta um fluxo (`npm start` via `srvx`) que **não é o fluxo atual documentado no CLAUDE.md do app** (que aponta para deploy SPA estático via `.htaccess`, sem Node no servidor). Esse README está desatualizado — não seguir.

### 1.5 Variáveis de ambiente necessárias

| Variável | Onde | Observação |
|---|---|---|
| `VITE_SUPABASE_URL` | `.env.local` (build SPA) | Baked no bundle — precisa existir **antes** do `vite build --config vite.spa.config.ts` |
| `VITE_SUPABASE_ANON_KEY` | `.env.local` (build SPA) | Idem — confirmada presente localmente |
| `APP_SUPABASE_URL` / `APP_SUPABASE_ANON_KEY` / `APP_SUPABASE_SERVICE_ROLE_KEY` | ambiente servidor (só se optar por SSR) | Presentes no `.env` da raiz do workspace — **não usar esse `.env` para o app**, ele é do AIOX, não do SIE |

Confirmar `.env.local` dentro de `sistema-de-instala-es-el-tricas-sie-main/` antes de buildar (já existe, mas revalidar chaves).

---

## 2. Decisão de arquitetura de deploy

**Modo alvo: SPA estático no Hostinger** (conforme documentado em `sistema-de-instala-es-el-tricas-sie-main/CLAUDE.md`, seção "Deploy SPA no Hostinger"). Não usar o fluxo `hostinger-deploy/README-HOSTINGER.md` (SSR com `srvx`) — está desalinhado com o app atual e Hostinger compartilhado não roda processo Node persistente.

Subdomínio de produção: `sie.applicationmanager.com.br` → `public_html/sie/`.

---

## 3. Pré-condições (bloqueantes)

1. **Resolver o gitlink órfão** de `sistema-de-instala-es-el-tricas-sie-main` (Ação 0) — sem isso, `git add`/`git push` na raiz não vai capturar o conteúdo real do app.
2. Confirmar com o usuário se as **migrations duplicadas** (`supabase/migrations/2026071*` na raiz vs `docs/supabase/0009-0010` no app) já foram aplicadas no Supabase — **não reaplicar** sem checar (risco de erro "already exists" ou, pior, migração divergente).
3. Confirmar se `.claude/scheduled_tasks.lock` deletado é intencional.
4. Rodar suíte de testes/lint/typecheck do app **antes** do build de produção (ver Ação 3).

---

## 4. Plano de execução (para @devops)

### Ação 0 — Corrigir o gitlink órfão do app

```bash
git rm --cached sistema-de-instala-es-el-tricas-sie-main
git add sistema-de-instala-es-el-tricas-sie-main/
```

Isso converte o app de "submodule fantasma" para arquivos normais rastreados no repo principal (confirmar com o usuário que essa é a intenção — a alternativa é formalizar como submodule real com `.gitmodules` + remote próprio, mas não há evidência de repo remoto separado para o app).

### Ação 1 — Consolidar o trabalho pendente na raiz

```bash
git add docs/stories/ docs/workflows/ docs/qa/ docs/roadmap/ .claude/agent-memory/ .ai/
git add .gitignore AGENTS.md
git status   # revisar D .claude/scheduled_tasks.lock antes de decidir add ou restore
git add src/ supabase/migrations/   # AUTO-OTI otimizador + migrations novas
```

Commits separados por natureza (não um monólito):
- `feat: consolida stories MOD-CC/SEC/QT, MOD-DC-HYBRID e AUTO-OTI (QA PASS)`
- `feat: integra app SIE ao repositório principal (resolve gitlink órfão)`

### Ação 2 — Validar migrations no Supabase antes de aplicar

```bash
# Verificar quais migrations já foram aplicadas ao projeto hlbksclcandbsyqrsbmx
supabase migration list --project-ref hlbksclcandbsyqrsbmx
```

Aplicar apenas as que faltam (prováveis candidatas: `0009_dependencia_retornos_downstream.sql`, `0010_dimensionamento_condutores_overrides.sql` — usar os arquivos de `docs/supabase/`, não os duplicados da raiz).

### Ação 3 — Validar o build antes de publicar

Dentro de `sistema-de-instala-es-el-tricas-sie-main/`:

```bash
bun install          # ou pnpm install — escolher UM e documentar (ver Seção 5)
bun run typecheck     # tsc --noEmit
bun run lint          # eslint .
bun run test          # vitest run
```

Só prosseguir se os 3 passarem limpo.

### Ação 4 — Build de produção (SPA)

```bash
# confirmar .env.local com VITE_SUPABASE_ANON_KEY preenchida
bun run build:spa    # vite build --config vite.spa.config.ts
grep -o 'sb_publishable_[^"]*' dist/assets/index-*.js   # confirmar chave baked corretamente
```

### Ação 5 — Empacotar para Hostinger

Usar o script PowerShell documentado em `CLAUDE.md` (gera ZIP com forward-slashes — `Compress-Archive` nativo do PowerShell quebra no Linux):

```powershell
Add-Type -Assembly "System.IO.Compression"
Add-Type -Assembly "System.IO.Compression.FileSystem"
$dist = ".\dist"; $zip = ".\hostinger-spa.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
$stream  = [System.IO.File]::Open($zip, 'Create')
$archive = New-Object System.IO.Compression.ZipArchive($stream, 'Create')
$files = @(@{ src = "$dist\index.html"; entry = "index.html" })
Get-ChildItem "$dist\assets" | ForEach-Object {
  $files += @{ src = $_.FullName; entry = "assets/$($_.Name)" }
}
foreach ($f in $files) {
  $entry = $archive.CreateEntry($f.entry, 'Optimal')
  $d = $entry.Open(); $s = [System.IO.File]::OpenRead($f.src)
  $s.CopyTo($d); $s.Close(); $d.Close()
}
$archive.Dispose(); $stream.Dispose()
```

### Ação 6 — Publicar no Hostinger

1. File Manager Hostinger → `public_html/sie/` → **apagar todos os arquivos existentes**.
2. Upload de `hostinger-spa.zip` → extrair no mesmo diretório.
3. Confirmar/recriar `public_html/sie/.htaccess`:

```apache
Options -MultiViews
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ index.html [QSA,L]
```

### Ação 7 — Smoke test pós-deploy

- Abrir `https://sie.applicationmanager.com.br/` — carrega lista de projetos.
- Navegar para `/projetos/:id` diretamente pela URL (valida `.htaccess`/SPA routing).
- Criar/editar uma dependência de teste, confirmar persistência no Supabase (valida RLS + anon key).
- Checar console do browser por erros de RLS (`[]` silencioso = policy faltando — ver policies documentadas no CLAUDE.md do app).

### Ação 8 — Push e limpeza

```bash
git push origin master   # @devops exclusivo
```

- Remover artefatos de deploy obsoletos (`hostinger-deploy-lite/`, `hostinger-deploy-minimal/`, `hostinger-staging/`, zips antigos) **após confirmar** que o deploy atual está estável — não antes.
- Atualizar/depreciar `hostinger-deploy/README-HOSTINGER.md` para não confundir futuras execuções (aponta fluxo SSR incorreto).

---

## 5. Itens para decisão do usuário (não bloqueiam deploy, mas precisam resposta)

1. **bun vs pnpm** — dois lockfiles no app. Qual é a fonte de verdade?
2. **Gitlink órfão** — formalizar como submodule real (repo remoto próprio) ou absorver como diretório normal no monorepo AIOX?
3. **Migrations duplicadas** (raiz `supabase/migrations/` vs app `docs/supabase/`) — consolidar em um único local?
4. **`.claude/scheduled_tasks.lock` deletado** — intencional?

---

## 6. Resumo executivo

| Item | Status |
|---|---|
| Trabalho de dev (stories QA PASS) | Pronto, não commitado |
| Testes/lint/typecheck | Não executados nesta varredura — rodar na Ação 3 |
| Build de produção | `dist/` existe mas desatualizado (17/jul) — rebuildar |
| CI/CD | Inexistente — deploy 100% manual |
| Bloqueante crítico | Gitlink órfão do diretório do app |
| Migrations pendentes | 2 (verificar se já aplicadas antes de reaplicar) |

**Ação imediata recomendada para @devops:** iniciar pela Ação 0 (gitlink) e Ação 1 (commits), depois seguir sequencialmente até a Ação 8.
