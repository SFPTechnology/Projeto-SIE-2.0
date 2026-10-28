# A02 — catálogo canônico de migrations (V2.0.1)

## Layout autorizado
- **Somente** `restructuring/supabase/migrations/`: migrations greenfield aplicáveis.
- `restructuring/supabase/greenfield/manifest.json`: inventário auditável da GF02 aplicada, identificador remoto e Git blob.
- `restructuring/supabase/greenfield/check_catalog.py`: valida arquivos locais e rejeita alterações na GF02 sem origem registrada.
- `supabase/migrations/` (raiz): **legado; nunca incluir, copiar ou executar** neste projeto.

## Execução sem serviço adicional
A partir da raiz da branch de desenvolvimento:

```bash
python restructuring/supabase/greenfield/check_catalog.py --json
python -m pytest restructuring/apps/api/tests/test_a02_greenfield_catalog_v201.py -q
```

A ferramenta não acessa Supabase nem cria banco. Os erros de hash, migration não registrada, versão duplicada, ref inesperado e tentativa de sinalizar DDL autorizada causam exit code 1. Não executar `supabase db push` na raiz.

## Adição futura de migration
1. Registrar story, revisão de schema e impacto de RLS/segurança.
2. Preparar candidato SQL em `docs/implantacao-sie-2-0/GREENFIELD` sem considerá-lo aplicado.
3. Quando a CLI apropriada estiver disponível, verificar `supabase --help` e `supabase migration new --help`, gerar arquivo versionado em workspace greenfield e atualizar manifesto.
4. Executar validação estática; SQL real somente em destino exato, com autorização específica de DDL, pré-condições, proteção de backup/rollback e leitura de retorno.
5. O manifesto de migrations **aplicadas** só aumenta após verificação do histórico remoto; candidatos pendentes ficam fora de `applied_migrations` até então.

A01/A02 estão relacionadas a desenvolvimento, não a implantação. Não confundir testes de contrato com rebuild/restore ou performance.
