# F12 — manifesto do candidato (não é release de produção)

**Candidato de preparação:** `F12-prepare-only-2026-10-25`. **Estado:** preparação técnica, NO-GO de produção.

| Atributo | Valor / rastreabilidade |
|---|---|
| Repositório | `SFPTechnology/Projeto-SIE-2.0` |
| SHA da origem F11 | `11643cf3ad7da2e6182183c6071148f924bfe741` |
| Branch F11 | `feat/f11-qa-integrado` |
| Branch F12 | `feat/f12-liberacao-controlada` (candidato de desenvolvimento; verificar HEAD e CI antes de qualquer uso) |
| API Python | `sie-api 0.1.0`, Python >=3.11, ambiente CI Python 3.12 |
| Bibliotecas diretas API | FastAPI >=0.110,<1; Pydantic >=2,<3; Uvicorn >=0.27,<1; ReportLab >=4,<5 |
| Testes opcionais | pytest >=8,<10; httpx >=0.27,<1; pypdf >=5,<7; Playwright >=1.55,<2 |
| Frontend | `restructuring/apps/web/` no SHA base; sem binário ou versão estável de produção homologados |
| CLI e motor | `restructuring/apps/api/sie_api/`; fluxo integrado consultivo F09→F10, sem habilitar cálculo normativo profissional |
| Persistência local | SQLite e exportações F05/F10 (raízes separadas); backup/restore offline em `local_bundle_backup_f11.py` |
| Bases de regras | versões/fontes registradas nos snapshots F01/F06–F09; nenhum ajuste de regras em F12 |
| Migrações observadas | migração SQLite versionada F03 (`data_lifecycle.py`), e migrations Supabase legadas; produção Supabase não inspecionada |
| Ambientes | DEV/TEST local experimentais; domínio, secrets, identidade de PROD e janela: **NÃO VALIDADO** |

## Evidência dos gates F11 — observação remota

No SHA exato de partida `11643cf3ad7da2e6182183c6071148f924bfe741`, três workflows `completed/success`:
- API: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/40183189791
- AIOX: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/40183189740
- Chromium: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/40183189754

Esta confirmação supre a condição documental de F11 para prosseguir **na preparação F12**, não a aprovação de produção. Baseline declarada: API 1.202 testes e 36 Chromium no commit de código F11; conferir quantidades no log do SHA documental antes de reproduzi-las como resultado próprio da F12.

## Composição do candidato e versionamento
- Fonte está vinculada ao SHA Git exato; conferir `git rev-parse HEAD`, `git status` e divergência com a base.
- Não há tag/release binária ou assinatura criptográfica de produção na F12.
- Inventário de código: `pyproject.toml`, `package.json`, `.aiox-core/package-lock.json`, `restructuring/apps/web/`, `sie_api/`, `supabase/migrations/`, `docs/implantacao-sie-2-0/`.
- O CI captura o ambiente Python resolvido da F11, mas faixas transitivas ainda não equivalem a lockfile Python reproduzível.
- Manifesto legível por máquina: `MANIFESTO_RELEASE.json`. Validador offline: `python scripts/f12_release_gate.py --check`; sucesso significa apenas consistência do preparo, jamais autorização de produção.
- Para um pacote verificável futuro: checkout da SHA final; ambiente limpo e lock registrado; `python -m build` se habilitado; `sha256sum` (Linux) / `Get-FileHash -Algorithm SHA256` (Windows); registrar hash, tamanho, dependências, SBOM, assinatura de responsável e resultado smoke; não anexar segredos.

## Compatibilidade e restrições
Não há contrato provado de multiusuário, RLS, autenticação externa, base de produção ou HTTPS operacional. O token local não substitui identidade empresarial. Artefatos F10 são imutáveis por revisão/hash; não reinterpretar snapshots passados ao atualizar normas. Regras elétricas e as-built dependem de validação profissional. Não existe liberação de SPDA/FV/VE/ambientes especiais pela F12.

**Próximo gate:** comprovar ambiente e permissões de produção; ensaio de backup/migração/restore em homologação isolada; build e checksums; smoke, alertas, evidências de QA; autorização formal de mudança e pós-deploy. Até lá: **NO-GO**.
