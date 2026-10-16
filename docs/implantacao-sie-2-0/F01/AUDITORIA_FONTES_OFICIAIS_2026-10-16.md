# F01 — Verificação de fontes oficiais externas em 16/10/2026

**Critério:** registrar apenas o que foi obtido de **fontes oficiais** e de texto efetivamente acessível. A presença de URL/cópia, identidade editorial e hash **não equivale** à homologação da transcrição numérica nem ao segundo conferente. F00 mantida como baseline intocada.

## 1. ABNT NBR 5410 — edição identificada, células não conferidas

**Emissor e catálogo primário:** Associação Brasileira de Normas Técnicas; https://www.abntcatalogo.com.br/default.aspx?O=1.

**Identificação oficial consultada:** **ABNT NBR 5410:2004 Versão Corrigida:2008**, Instalações elétricas de baixa tensão. A transcrição `Arquivos_Diversos/NBR_5410_original/NBR-5410.md` referencia esta edição, mas é **derivada e não comprova exemplar oficial ABNT autorizado**.

**Lacuna impeditiva:** acesso a documento licenciado/autorizado e inspeção técnica original das tabelas 36–46 com método/material/seção/isolação/carregados e notas; Rca/XL sob as condições reais de operação. Nenhum valor ABNT foi homologado ou publicado nesta verificação. O software continua recusando aprovação normativa.

## 2. ABNT NBR 5419 — metadados SPDA

O catálogo oficial https://www.abntcatalogo.com.br/default.aspx?O=1 lista as partes **1, 2, 3 e 4 de 2026, Versão Corrigida:2026**. A versão já consta em `sie_api/data/normative_registry.json`, com `verified_data=false`. Nenhuma parte de SPDA foi reinterpretada como fonte de ampacidade, Rca ou XL; aplicabilidade dependerá do módulo/projeto.

## 3. EDP São Paulo — fonte oficial da V09 encontrada diretamente

- **Página pública de normas EDP:** https://www.edp.com.br/normas-e-padroes-tecnicos/; resultado indexado da categoria "unidade consumidora individual EDP São Paulo" informa **código PT.DT.PDN.00068, versão 9, data de publicação 15/04/2026**.
- **Documento primário divulgado no próprio domínio EDP, URL direta identificada:** https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf. Resultado indexado identifica título, código `PT.DT.PDN.00068`, versão `09`, campo **"VIGÊNCIA — INÍCIO 14/04/2026"**, 91 páginas.
- **Cópia binária existente no repositório:** `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9.pdf`; registro F00 do SHA local `b14f414001d9831f91bbef84f022c5164f367431cc6a209e5fb34b4e48f20810`. A origem oficial foi **LOCALIZADA**; **NÃO foi possível baixar o binário via acesso atual** para comparar a cópia do GitHub byte a byte ou inspecionar visualmente Anexo A e notas. O servidor oferece o PDF como `application/octet-stream`, não admitido pelo leitor web desta execução. Resultado indexado e cópia transcrita **não são conferência física de célula**.
- **Distinção importante:** publicação pública 15/04/2026 ≠ campo de início de vigência 14/04/2026 exibido na fonte oficial indexada. A versão de código não deve inferir vigência da mera data de publicação; aplicar a vigência somente após inspeção do campo original.
- **Estado por célula:** U2, D2/D4/D6/D7/D9/D10 e T2/T4/T6/T7/T9/T10 permanecem **candidatos históricos não homologados**. Linha/coluna/notas, demanda/modalidade e condutores exigem duas conferências independentes da fonte primária e checagem do território.

## 4. NR-10 — fonte primária obtida, verificada e código corrigido

**Documento oficial aberto e inspecionado visualmente nas páginas 1 e 3:** Portaria MTE nº 737, de 29/05/2026, DOU 01/06/2026, publicada no site do Ministério do Trabalho e Emprego:  
https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/sst-portarias/2026-1/portaria-mte-no-737-nova-nr-10.pdf

**Constatações primárias pontuais:**
- Art. 5º: a Portaria entra em vigor um ano após sua publicação, portanto **01/06/2027**.
- Art. 3º: prazo adicional de **um ano depois da entrada em vigor**, **somente** para a alínea `e` do subitem **10.6.4** da nova NR-10 **nas instalações elétricas existentes na data da vigência**. Assim, o marco específico é **01/06/2028**, não uma prorrogação global da NR-10 anterior.
- Há retificação publicada no DOU 24/06/2026 referente ao item 10.8.4 (alíneas de treinamento) visível no PDF oficial.
- Seção 10.4 trata de segurança em projetos, exigindo atenção a componentes, aterramento, memorial, atualização e responsabilidade do profissional legalmente habilitado; a redação de 2027 não se aplica automaticamente aos projetos datados de 2026.

**Mudança implementada:** `sie_api/domain/normative.py` passou a tratar a exceção estreita `10.6.4(e)` conforme data e condição declarada de instalação existente em 01/06/2027, sem propagar a transição ao conjunto da norma. API recebe campo opcional `existing_installation_on_2027_06_01` apenas para TRIAGEM, sem converter autodeclaração em prova. `test_normative_f01.py` valida limites de datas e status sempre bloqueados sem homologação externa. **O código implementa a lógica e não substitui a inspeção de todo o conteúdo regulatório nem assinatura profissional.**

## 5. Quadro de verificação e independência

| Fonte | Documento editorial original localizado | Texto primário aberto e conferido nesta sessão | Valores/células numéricas duplamente conferidos | Signoff técnico independente |
|---|---|---|---|---|
| ABNT NBR 5410 | Catálogo / edição somente | **Não** | 0 | Não |
| ABNT NBR 5419 | Catálogo / edições somente | **Não** | 0 | Não |
| EDP PT.DT.PDN.00068 V09 | **Sim**, URL no próprio domínio | **Não** — PDF binário não acessível no leitor | 0 | Não |
| MTE Portaria 737/2026 (NR-10) | **Sim**, PDF oficial | **Sim**, artigos 3º e 5º e seção 10.4 | Não aplicável para Iz/Rca/XL | Não |

**G01 continua PARTIAL**, pois metadados confirmados não cobrem todas as fontes, direitos e aplicabilidades. **G02/G03 seguem BLOCKED.** Verificação da Portaria MTE não foi realizada por dois revisores independentes; esta inspeção do mesmo executor não satisfaz G06.

## 6. Única próxima comprovação objetiva

Obter cópia autorizada do original ABNT NBR 5410 edição aplicável e efetuar leitura independente; obter/abrir o PDF EDP diretamente do link oficial com leitores independentes e comparar páginas/valores com o arquivo local; para cada linha efetivamente consumida produzir expectativa externa, notas, condição, revisor A/B, data e hash de evidência. Então executar QA3 em três sessões autenticadas realmente isoladas, corrigir achados, checar todos os 10 critérios e 6 gates no SHA final. **Não reiniciar F00 nem iniciar F02.**
