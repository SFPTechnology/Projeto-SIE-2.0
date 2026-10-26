# Story SIE-F12 — Release controlado, sem implantação

- Fase: F12 / EP24, EP26, EP27, EP35 condicional
- Base obrigatória: `feat/f11-qa-integrado` no commit `11643cf3ad7da2e6182183c6071148f924bfe741`.
- Especificação: `F12_EXECUTAR.md` fornecido pelo titular em 25/10/2026.
- Estado: **EM EXECUÇÃO — preparação do candidato e controles, sem autorização de produção**.
- Escopo autorizado: branch isolada, código de validação sem efeitos colaterais, documentação, testes com dados descartáveis; sem merge, tag, publicação de release, deploy, acesso a secrets ou mudança de bases reais.

## Critérios de aceitação rastreáveis
- [x] 12.01 Manifesto de candidato ligado à base F11 e inventário auditável de versões e limites.
- [ ] 12.02 Checklist documentado de identidade, segredo, permissões e ambientes; nenhuma credencial exposta.
- [ ] 12.03 Ensaio verificável de migração reversível e recuperação total em cópia isolada.
- [ ] 12.04 Métricas, alertas e procedimentos de incidente testados em ambiente representativo.
- [ ] 12.05 Notas, manual, inventário e checksums de pacote reproduzível conferidos.
- [ ] 12.06 Smoke/E2E/restore e acesso negativo em pré-produção aprovada.
- [ ] 12.07 Registro de autorização formal de mudança com responsável, custos, janela e rollback.
- [ ] 12.08 Deploy controlado rastreado após GO, nunca nesta execução.
- [ ] 12.09 Monitoramento pós-deploy e suporte exercitados.
- [ ] 12.10 Política de revisão normativa e as-built documentada e aprovada.
- [ ] QA-01, QA-02, QA-03 revisam separadamente e assinam escopo/evidências; profissional da engenharia permanece necessário para liberação técnica.

## Restrições invariantes
- `main` e produção inalteradas; F11 DONE significa **QA do software local**, não go-live.
- Software consultivo F09→F10 não implica conformidade NBR 5410/5419/NR-10 ou concessionárias.
- O token local e SQLite de único proprietário **não são identidade ou segregação de produção**.
- Todos os gates sem prova permanecem `PENDENTE` ou `HUMAN_REQUIRED`; nenhum teste recebe expectativa enfraquecida para ficar verde.

## File list
- `docs/stories/story-SIE-F12-LIBERACAO-CONTROLADA.md` (esta story).
- `docs/implantacao-sie-2-0/F12/` (manifesto, riscos, playbooks, QA e relatórios).
- `scripts/f12_release_gate.py` e testes (controle local sem deploy).
- `.github/workflows/sie-f12-release-safety.yml` (validação segregada, se elegível).

## Definição de DONE
F12 DONE apenas após todos os gates comprovados em ambiente e SHA próprios, autorização humana aplicável, implantação e pós-deploy saudáveis; até lá, execução parcial e bloqueio de produção.
## Checkpoint QA3 da preparação — 25/10/2026
- CI no SHA `436edb321ec52a0ee8b7971a698641306692de2a`: API 1209, 36 Chromium, F12 Safety 7+19 e AIOX success.
- QA-01: preparação APROVADA, produção BLOQUEADA; QA-02: homologação normativa PENDENTE; QA-03: recuperação local APROVADA, produção BLOQUEADA.
- Documentos: manifesto JSON/MD, notas, checklist, rollback, manuais, operação, política normativa, mudança, pós-implantação, QA3 e relatório.
- Esta story é de preparação, não atestado de implementação 12.07–12.09.

## Incremento de execução técnica W1–W4 — story de alteração
- [ ] A02: staging HTTPS de loopback com certificado descartável e teste de persistência local negada com `SIE_ENV=production`.
- [ ] A03: replay de migração, recovery F05/F10 e recusa de corrupção no CI.
- [ ] A04: pacote tar.gz determinístico SHA-256 de fontes rastreadas, dois builds byte-a-byte idênticos e manifesto de todos os arquivos.
- [ ] A05: verificar pacote, checksums e smoke HTTPS; manter testes API/Chromium/AIOX.
- [ ] A06: estabelecer relatório sanitizado; monitoramento de ambiente público permanece fora do escopo comprovado.
- [ ] A07/A08: anexar matriz de aprovações obrigatórias e NO-GO quando não houver laudo e decisão de mudança.
- Códigos novos: `scripts/f12_bundle.py`, `scripts/f12_staging_smoke.py`; CI `sie-f12-release-safety.yml`; política do gate `f12_release_gate.py`.
- Produção, `main` e motores elétricos ficam inalterados.
