# Guia: Criação de pasta `dist/` SPA funcional

> **Como usar:** "Crie uma pasta dist/ do [conteúdo X], utilizando as instruções existentes no conteúdo do arquivo GUIA-BUILD-SPA-DIST.md"

---

## Contexto e premissas

Este guia aplica-se a projetos que utilizam:
- **TanStack Router** com rotas de API server-side (`createFileRoute` com `server.handlers`)
- **TanStack Start** (SSR) no modo de desenvolvimento, mas que precisam de um **build SPA estático** para hospedagem em servidores sem Node.js (ex: Hostinger, cPanel, S3)
- **Supabase** como banco de dados com RLS
- **Vite** como bundler

O build SSR padrão (`vite build`) gera pastas `dist/client` e `dist/server`. O objetivo deste guia é gerar uma pasta `dist/` **estática e autocontida**, pronta para upload em qualquer servidor HTTP simples.

---

## Passo 1 — Verificar se já existe `vite.spa.config.ts`

Procurar por `vite.spa.config.ts` na raiz do projeto.

**Se não existir**, criar com o conteúdo abaixo:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import tsconfigPaths from "vite-tsconfig-paths";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const rootDir = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      "@": resolve(rootDir, "./src"),
    },
  },
  plugins: [react(), tailwindcss(), tsconfigPaths()],
  define: {
    "process.env": JSON.stringify({}),
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
});
```

> **Atenção:** NÃO usar o plugin `@tanstack/router-plugin` neste config — ele ativa o modo SSR.

---

## Passo 2 — Verificar o `index.html`

O `index.html` na raiz do projeto deve apontar para um entry point SPA, **não** para o entry point SSR (`start.ts`, `server.ts`).

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Nome do App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main-spa.tsx"></script>
  </body>
</html>
```

Se o projeto tiver apenas `main.ts` ou `start.ts` como entry, criar `src/main-spa.tsx`:

```tsx
import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "@tanstack/react-router";
import { getRouter } from "./router.spa";
import "./styles.css";

const router = getRouter();

declare module "@tanstack/react-router" {
  interface Register {
    router: ReturnType<typeof getRouter>;
  }
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
```

---

## Passo 3 — Criar `src/routeTree.spa.ts`

### Por que é necessário

O arquivo `routeTree.gen.ts` gerado automaticamente pelo TanStack Router inclui:
1. Rotas de API (`./routes/api/v1/*`) que importam código server-only (`node:async_hooks`, `AsyncLocalStorage`)
2. Um bloco `declare module '@tanstack/react-start'` com `ssr: true` que ativa o contexto SSR

Ambos causam o erro no browser:
```
Uncaught Error: Module "node:async_hooks" has been externalized for browser compatibility
```

### Como identificar quais rotas são seguras para SPA

- **Incluir:** rotas em `src/routes/*.tsx` que usam apenas `createFileRoute` com componentes React
- **Excluir:** rotas em `src/routes/api/**` que usam `server.handlers`, `createServerFn`, `useServerFn`, ou importam de `@tanstack/react-start`

Verificar com:
```bash
grep -r "react-start\|createServerFn\|useServerFn\|server:" src/routes/ --include="*.ts" --include="*.tsx" -l
```

Cada arquivo encontrado representa uma rota que **não pode** entrar no SPA tree.

### Estrutura do `routeTree.spa.ts`

```ts
// Importar APENAS rotas UI — sem api/v1/* e sem @tanstack/react-start

import { Route as rootRouteImport } from './routes/__root'
import { Route as IndexRouteImport } from './routes/index'
// ... demais rotas UI

const IndexRoute = IndexRouteImport.update({
  id: '/',
  path: '/',
  getParentRoute: () => rootRouteImport,
} as any)

// ... registrar demais rotas UI

const rootRouteChildren = {
  IndexRoute,
  // ... demais rotas UI
}

export const routeTree = rootRouteImport
  ._addFileChildren(rootRouteChildren)
  ._addFileTypes<FileRouteTypes>()

// NÃO incluir: declare module '@tanstack/react-start' { ... }
// NÃO incluir: import from './start.ts'
```

---

## Passo 4 — Criar `src/router.spa.tsx`

```tsx
import { QueryClient } from "@tanstack/react-query";
import { createRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.spa";

export const getRouter = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        staleTime: 30_000,
      },
    },
  });

  return createRouter({
    routeTree,
    context: { queryClient },
    scrollRestoration: true,
    defaultPreloadStaleTime: 0,
  });
};
```

---

## Passo 5 — Verificar variáveis de ambiente

No SPA, variáveis de ambiente são **baked no bundle em build time**. Apenas variáveis prefixadas com `VITE_` são expostas ao browser.

Verificar se existe `.env.local` com as variáveis necessárias:

```env
# Exemplo para Supabase
VITE_SUPABASE_URL=https://<project-id>.supabase.co
VITE_SUPABASE_ANON_KEY=<anon-key-publica>
```

> **Crítico:** usar sempre a **anon key** (publishable), nunca a service_role key. A anon key é segura para ficar no bundle do browser.

> **Onde encontrar:** Supabase Dashboard → Project Settings → API → "anon public"

O código do projeto deve usar `import.meta.env.VITE_*` (não `process.env.*`) para acessar essas variáveis no cliente:

```ts
const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_ANON_KEY;
```

---

## Passo 6 — Executar o build

```bash
npx vite build --config vite.spa.config.ts
```

**Saída esperada** (sem erros):
```
✓ N modules transformed.
dist/index.html
dist/assets/index-XXXXXXXX.js
dist/assets/index-XXXXXXXX.css
✓ built in Xs
```

**Se aparecer erro `node:async_hooks`:** alguma rota com código server-only ainda está no `routeTree.spa.ts`. Voltar ao Passo 3 e remover a rota problemática.

**Confirmar que as credenciais foram embutidas corretamente:**
```bash
grep -o 'VITE_SUPABASE_ANON_KEY_VALOR_REAL\|sb_publishable_[^"]*' dist/assets/index-*.js
```
Se aparecer o placeholder em vez da key real, o `.env.local` não estava salvo antes do build.

---

## Passo 7 — Configurar RLS do Supabase para acesso via anon key

No modo SSR, o app geralmente usa a `service_role` key (que bypassa o RLS). No SPA, a `anon key` fica sujeita ao RLS. Se as tabelas não tiverem políticas para a role `anon`, as queries retornam `[]` vazio sem erro.

**Teste rápido** para verificar se o RLS está bloqueando:
```bash
curl "https://<project>.supabase.co/rest/v1/<tabela>?select=id&limit=1" \
  -H "apikey: <anon-key>" \
  -H "Authorization: Bearer <anon-key>"
```
- Retorno `[]` vazio quando há dados → RLS bloqueando
- Retorno `[{"id":"..."}]` → OK

**SQL para liberar acesso anon** (executar no Supabase SQL Editor):

```sql
-- Repetir para cada tabela que o app acessa (incluindo tabelas filhas com FK)
CREATE POLICY "anon_all_<tabela>" ON <tabela>
  FOR ALL TO anon USING (true) WITH CHECK (true);
```

Identificar todas as tabelas consultando os repositórios do projeto:
```bash
grep -r "from(" src/infra/supabase/ --include="*.ts" -h | grep -o '"[a-z_]*"' | sort -u
```

As políticas aplicam imediatamente — não é necessário rebuild do SPA.

---

## Passo 8 — Criar o ZIP para deploy

### Verificar conteúdo do `dist/`

```
dist/
├── index.html
└── assets/
    ├── index-XXXXXXXX.js
    ├── index-XXXXXXXX.css
    └── styles-XXXXXXXX.css  (pode haver mais de um)
```

### Criar ZIP com forward slashes (crítico no Windows)

No Windows, `Compress-Archive` do PowerShell gera ZIPs com barras invertidas (`assets\arquivo`), que servidores Linux interpretam como parte do nome do arquivo em vez de diretório. Usar o método .NET:

```powershell
Add-Type -Assembly "System.IO.Compression"
Add-Type -Assembly "System.IO.Compression.FileSystem"

$dist = "C:\caminho\para\dist"
$zip  = "C:\caminho\para\deploy.zip"

if (Test-Path $zip) { Remove-Item $zip -Force }

$stream  = [System.IO.File]::Open($zip, 'Create')
$archive = New-Object System.IO.Compression.ZipArchive($stream, 'Create')

# Mapear cada arquivo com forward slash como entry name
$files = @(
  @{ src = "$dist\index.html"; entry = "index.html" }
)
# Adicionar todos os assets dinamicamente
Get-ChildItem "$dist\assets" | ForEach-Object {
  $files += @{ src = $_.FullName; entry = "assets/$($_.Name)" }
}

foreach ($f in $files) {
  $entry = $archive.CreateEntry($f.entry, 'Optimal')
  $dst   = $entry.Open()
  $src   = [System.IO.File]::OpenRead($f.src)
  $src.CopyTo($dst)
  $src.Close(); $dst.Close()
}
$archive.Dispose(); $stream.Dispose()
"ZIP criado: $zip ($([math]::Round((Get-Item $zip).Length/1MB,1)) MB)"
```

---

## Passo 9 — Deploy no Hostinger (ou servidor equivalente)

### Identificar a pasta correta no servidor

Subdomínios no Hostinger geralmente têm pasta própria:
- Domínio principal → `public_html/`
- Subdomínio `app.dominio.com` → `public_html/app/`
- Subdomínio `sie.dominio.com` → `public_html/sie/`

### Procedimento de upload

1. **File Manager** → entrar na pasta do domínio/subdomínio
2. **Deletar** todos os arquivos existentes (evitar mistura de builds antigos e novos)
3. **Upload** do `deploy.zip`
4. **Extract** o ZIP na pasta atual (não em subpasta)
5. **Deletar** o ZIP após extração
6. Verificar que a estrutura final é:
   ```
   <pasta-do-domínio>/
   ├── index.html
   └── assets/
       ├── index-XXXXXXXX.js
       └── index-XXXXXXXX.css
   ```

### Configurar roteamento SPA (`.htaccess`)

Para que rotas como `/projetos/123` não retornem 404, criar `.htaccess` na pasta do domínio:

```apache
Options -MultiViews
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ index.html [QSA,L]
```

### Verificar após upload

```bash
# Verificar que o JS correto está sendo servido
curl -sI https://seu-dominio.com/assets/index-XXXXXXXX.js | head -2
# Esperado: HTTP/1.1 200 OK

# Verificar que o index.html referencia o JS correto
curl -s https://seu-dominio.com/ | grep "script"
```

---

## Checklist final

- [ ] `vite.spa.config.ts` existe sem o plugin TanStack Router
- [ ] `index.html` aponta para `src/main-spa.tsx`
- [ ] `src/routeTree.spa.ts` existe sem rotas de API e sem bloco `@tanstack/react-start`
- [ ] `src/router.spa.tsx` importa de `routeTree.spa`
- [ ] `.env.local` tem `VITE_SUPABASE_URL` e `VITE_SUPABASE_ANON_KEY` preenchidas (não placeholders)
- [ ] Build executado: `npx vite build --config vite.spa.config.ts`
- [ ] Anon key confirmada no bundle (não placeholder)
- [ ] Políticas RLS criadas para todas as tabelas acessadas pelo app
- [ ] ZIP criado com forward slashes (método .NET ZipArchive)
- [ ] Arquivos antigos deletados do servidor antes do upload
- [ ] Estrutura `index.html` + `assets/` na pasta correta do servidor
- [ ] `.htaccess` configurado para SPA routing
- [ ] Testado em aba anônima (sem cache do browser)
