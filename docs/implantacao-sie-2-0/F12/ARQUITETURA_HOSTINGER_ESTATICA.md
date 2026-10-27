# F12 — arquitetura de hospedagem estática existente + API externa opcional

**Decisão atualizada em 26/10/2026.** O titular esclareceu que todos os seus projetos, inclusive o SIE de primeira geração, já funcionaram como **sites de arquivos estáticos hospedados em subdomínios na Hostinger**. O domínio pretendido para o SIE 2.0 é `https://sie2.applicationmanager.com.br/`.

## Decisão técnica final para esta onda de preparação

**Preservar Hostinger como frontend estático; não exigir VPS da Hostinger para isso.** O FastAPI desenvolvido em F00–F11 não pode executar dentro da hospedagem web estática tradicional, mas pode continuar isolado em **outro servidor Python**, caso seja necessário manter os cálculos feitos pelo motor existente.

```text
https://sie2.applicationmanager.com.br/
      │ Hostinger · index.html + consultivo.js + consultivo.css
      │ (sem tokens, sem dados pessoais, sem gravação de projetos)
      │
      └── HTTPS + CORS estrito (somente depois de validado)
               │
               ▼
         API FastAPI `sie_api.f12_consultative:app`
         domínio/serviço separado AINDA NÃO ESCOLHIDO
         somente GET /api/v1/health e POST /api/v1/circuitos/analisar
         sem contas, banco, projetos, artefatos ou aprovação normativa
```

**Não migrar outros sites**, nem remover ou substituir o SIE 1.0 antes de uma decisão de mudança. VPS Hostinger é apenas UMA alternativa possível para o backend; serviço Python de outro provedor também serve, sujeito a análise técnica de risco, custo e contratos.

**Limite funcional explícito:** a interface estática F12 neste momento é um **portal consultivo de demonstração sintética**, NÃO a migração integral dos módulos locais F00–F11. Não transformar fórmulas Python em JavaScript sem equivalência comprovada e QA; nem fingir salvar planta, histórico ou relatórios sem backend.

## Pacote estático de homologação, já automatizado

`python scripts/f12_hostinger_static.py --out /caminho/novo/diretorio-vazio`

Produz um ZIP reproduzível `sie-f12-hostinger-static-preview.zip`, manifesto JSON, SHA-256, HTML/CSS/JS e `.htaccess` com cabeçalhos e tentativa de redirecionamento HTTPS para o domínio informado. **Sem parâmetro --api-origin, não há motor conectado: a simulação fica desabilitada e um aviso aparece na interface.** Isso é intencional, não um defeito.

Após aprovar um backend Python externo, construir novo pacote:

`python scripts/f12_hostinger_static.py --out /outro/diretorio-vazio --api-origin https://DOMINIO-VALIDADO-DA-API`

**DOMINIO-VALIDADO-DA-API é ilustrativo; não é um endereço provisionado.** É preciso validar HTTPS, CORS restrito, headers, monitoramento/rate-limit, custos e o próprio backend antes de configurar. O empacotador recusa HTTP, IP, localhost, credenciais, portas não padrão, fragmentos e querystrings; não publica em nenhum host.

O backend consultivo possui CORS explícito **somente para `https://sie2.applicationmanager.com.br`**. Qualquer origem adicional de homologação precisará ser registrada e testada em configuração separada, jamais `*` (wildcard).

## Caminho de implantação sem afetar sites atuais

1. Conservar `public_html` e DNS do site hoje publicado; fazer backup e inventário de arquivos fora da publicação.
2. Validar o ZIP em ambiente de homologação realmente segregado; conferir `MANIFEST.json`, hashes e política `.htaccess` suportada pelo servidor.
3. Validar carregamento do frontend em navegador real e modo sem API: aviso visível e botão desabilitado.
4. Se o objetivo do primeiro go-live **inclui executar cálculo pela internet**, primeiro contratar/aprovar/provisionar backend Python externo, configurar TLS e bloqueio de armazenamento/rotas, preparar pacote com HTTPS e CORS por origem, executar smoke remoto e teste de abuso.
5. Obter backup/rollback, aprovação de mudança e decisão GO/NO-GO por responsáveis reais. Somente então fazer qualquer upload para o subdomínio existente; registrar pós-deploy.
6. Para expansão futura a usuário logado, acervo e relatórios F10/F11, abrir nova etapa de persistência, IAM, migração e homologação normativa — esses serviços **não estão liberados** pelo portal de demonstração.

## Critérios auditáveis
- O ZIP estático **não contém Python, bancos, secrets ou autenticação local**.
- Duas execuções com mesmo `--api-origin` geram ZIPs e hashes byte-a-byte idênticos.
- A ausência de API impede fazer chamada para motor inexistente e expõe motivo de bloqueio.
- `POST /api/v1/circuitos/analisar`, quando conectado ao FastAPI separado, retorna `liberado_para_uso_normativo=false`; demais rotas bloqueadas.
- Em ambiente aprovado, TLS, CORS, proxy/ingress, observabilidade, disponibilidade e recuperação devem ser comprovados, não presumidos.
- **Qualquer entrega de arquivos no site atual é uma mudança real e exige autorização formal específica**; este pacote de CI é apenas QA, não deploy.

## Evidências CI de implementação (código SHA `67ef9d4cadebaec67163d9bfcce46859897b1144`)
- API `40265032187`: **1234 passed**; Chromium `40265032249`: **37 passed**; AIOX `40265032253`: **success**.
- F12 Safety `40265032192`: **8 testes gate, 19 recuperação, 6 segurança consultiva, 5 inspeção Hostinger, 13 pacote estático**; todos success.
- Pacote estático SEM API: **5 arquivos**, checksum SHA-256 `70a685c58a49bf80c4b542dd7c588fccab4263de851da246334c59f16faf2512`, dois ZIPs iguais e `production_authorized=false`.
- Evidências públicas do código/CI não comprovam o tipo de plano, conteúdo do subdomínio, acesso hPanel, sucesso de upload, API externa, segurança do host, nem mudança aprovada.

**Estado da fase:** `F12 HUMAN_REQUIRED / NO-GO para produção`. A arquitetura de infraestrutura foi definida; falta backend se cálculo online for obrigatório, homologação segregada e autorização de implantação.

## Complemento técnico — isolamento de staging e diagnóstico de dois hosts (2026-10-26 (America/Sao_Paulo))

1. **Gerar preview estático em staging isolado**, após confirmar o subdomínio que foi realmente criado na Hostinger:
```bash
python scripts/f12_hostinger_static.py --out /pasta-qa-vazia \
  --site-origin https://SUBDOMINIO_REAL.applicationmanager.com.br \
  --api-origin https://API_PYTHON_REAL
```
Esses dois hosts são **marcadores**; o comando não prova que DNS/TLS/serviços existam e não deve ser executado apontando para `public_html` existente.
2. O `.htaccess` do ZIP agora redireciona ao **mesmo host de staging** indicado por `--site-origin`, e o manifesto inclui `site_origin`. CLI rejeita HTTP, host externo, senha, caminho e porta não padronizada.
3. A instância FastAPI de homologação exige `SIE_F12_STAGING_ORIGIN=https://SUBDOMINIO_REAL.applicationmanager.com.br`. Essa configuração autoriza exclusivamente staging, não o site de produção. Sem variável configurada, o FastAPI autoriza apenas `https://sie2.applicationmanager.com.br`.
4. Requisições JSON POST recebem limite efetivo de corpo (inclusive transfer-encoding chunked). **Proxy/WAF também precisa** ter limites de tamanho, taxa e recursos; middleware não substitui controle de ingresso.
5. Novo diagnóstico `scripts/f12_split_preflight.py`: `python scripts/f12_split_preflight.py` não usa rede. `--live --site-origin ... --api-origin ...` faz GET verificado por TLS **em dois hosts distintos**. É insuficiente para comprovar CORS preflight, execução POST, rate-limit, autenticação/admin, alertas ou autorização final. Não executar no CI com `--live`.
6. O checker antigo `f12_hostinger_preflight.py` pressupunha frontend e API na **mesma origem**, sendo inadequado como aceitação da topologia estática + API externa. Preservado somente como histórico/teste legado de uma implantação same-origin.
