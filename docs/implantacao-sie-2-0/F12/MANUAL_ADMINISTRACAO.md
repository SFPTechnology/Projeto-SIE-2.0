# SIE 2.0 — manual de administração F12 (preparação, não produção)

## 1. Separar ambientes
O sistema validado até F11 funciona como API local e UI em navegador; a API local é intencionalmente single-owner por token, restrita a loopback/dev-test. **Não publicar essa configuração na Internet**. Para operar externamente exigem-se identidade autenticada, autorização por projeto, isolamento, HTTPS, gestão de segredos, logging redigido, backup e gestão de acesso previamente implementados e aprovados.

## 2. Diagnóstico sem modificar dados
No checkout F12, em terminal do diretório raiz:
```powershell
git rev-parse HEAD
git status --short
python scripts/f12_release_gate.py --check
```
O resultado `PREPARATION_VERIFIED_ONLY` não significa GO. `--require-production` retorna bloqueio intencional. Verificar três workflows API/AIOX/Chromium e o workflow F12 no SHA do checkout. Não incluir tokens nos logs anexados.

## 3. Subir software apenas no ambiente local de teste
Usar o procedimento do `restructuring/README.md` e do `restructuring/docs/MANUAL-OPERACIONAL.md` versionados no mesmo SHA. Preparar venv Python >=3.11, instalar `restructuring/apps/api` no venv, configurar DB e token de teste; usar somente `127.0.0.1`. Abrir a interface F10 e confirmar projeto de exemplo, artefato `PUBLISHED`, verificação de hash e `STALE` quando alterado. Caso algum controle falhe, interromper a sessão de teste.

## 4. Backup e recuperação offline
Parar escritores. No diretório `restructuring/apps/api`, em cópia descartável:
```powershell
python -m sie_api.local_bundle_backup_f11 backup --db CAMINHO_DB_TESTE --bundle DESTINO_BACKUP_NOVO
python -m sie_api.local_bundle_backup_f11 restore --bundle DESTINO_BACKUP_NOVO --db NOVO_DB_TESTE --roots NOVA_PASTA_RAIZES
```
Guardar o JSON de mapeamento de raízes; atualizar configuração do serviço restaurado, inclusive `SIE_F10_ARTIFACT_ROOT`; conferir todos os hashes e abrir um documento real do acervo de teste. Não reutilizar destinos existentes nem copiar bases reais para demonstradores. **Atenção:** o comando só é aplicável a SQLite local com raízes registradas. Nenhuma recuperação de Supabase/produção foi validada.

## 5. Segurança e operação
Configurar mínimo privilégio por serviço; secrets fora de código, manifests e CI logs. Rotação e expiração de credenciais conforme política aprovada. Mascarar tokens, PII, payloads de clientes e caminhos sensíveis dos logs de incidente. Aprovar política de backup criptografado, retenção, acesso e descarte. Separar responsáveis DevOps, DBA, QA, engenharia e change manager.

## 6. Falha e suporte
Em erro 401/403: verificar configuração de token local sem divulgar valor. Em erro 5xx: capturar timestamp, SHA, rota e correlation ID sanitizado; conferir logs e integridade de SQLite. Em manifesto/hash divergente, bloquear download e seguir `PLANO_IMPLANTACAO_ROLLBACK.md`. Se alterações gerarem `STALE`, recalcular e conferir proveniência, nunca reaproveitar documento obsoleto.

## 7. Rotina de atualização
Ler `CHECKLIST_GO_NO_GO.md` antes de qualquer publicação. Rever fontes de concessionária e ABNT com responsável habilitado e reter snapshots históricos. Não atualizar silenciosamente catálogos aplicados a projetos finalizados. Abrir ticket de incidente com versão, ambiente, reprodução e impacto; manter trilha de aprovação.
