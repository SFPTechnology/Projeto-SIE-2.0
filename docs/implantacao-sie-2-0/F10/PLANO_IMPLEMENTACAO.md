# F10 — Plano de implementação executável

**Branch de trabalho:** feat/f09-concessionarias-especializadas  
**Limites:** preservar main; sem merge, deploy, migração de produção ou homologação normativa. As extensões F09 já excluídas permanecem fora do escopo.

## Estado inicial confirmado

- O handoff F09 registra a integração essencial como concluída e libera desenvolvimento F10.
- O código F10 existente é uma camada inicial em restructuring/apps/api/sie_api/representation_f10.py, ainda sem editor/importador de planta, armazenamento imutável, PDF ou integração de interface.
- A última suíte API observada no SHA 4f1e27971339c4cae702a3f8353be5162675f70b teve 1.039 aprovações e uma falha em test_svg_escapes_untrusted_labels. A falha está no cenário que muda o ID do quadro sem atualizar as referências dos circuitos; a validação do grafo interrompe corretamente.
- O AIOX passou nesse SHA. A execução de navegador registrada ainda não havia concluído na consulta inicial. O SHA atual da branch é a588224d30877d63d25349160e2168546bce5f5b; a API de checks não apresentou execuções associadas a esse SHA na inspeção.

## Sequência de trabalho

1. **Consertar e confirmar a base de testes**
   - Ajustar o teste de escape SVG para usar rótulo hostil em circuito mantendo ID do quadro e referências válidas.
   - Rodar o teste focal, a suíte API e os três workflows remotos no SHA resultante.
   - Não alterar expectativas funcionais para obter resultado verde.

2. **Consolidar o contrato de artefato**
   - Ampliar o contrato para project_id, revision_id, calculation_run_id, versão da regra e template em todos os artefatos.
   - Garantir que snapshot inválido, referência inexistente, valor não finito ou revisão divergente bloqueiem geração/exportação.
   - Preservar estados de estudo/pendência; nunca inferir aprovação normativa.

3. **Representação gráfica derivada do modelo**
   - Usar IDs do domínio e topologia existente para desenhar unifilar por quadro e legenda rastreável.
   - Implementar geometria de planta somente sobre estruturas/unidades existentes; não inventar escala ou comprimentos. Se o repositório não oferecer contrato geométrico, registrar a dependência e restringir a entrega ao unifilar.

4. **Quadro, quantitativos e relatório**
   - Produzir quadro de circuitos com carga/fase/dispositivo/condutor da mesma revisão e execução.
   - Derivar quantitativos somente de itens e comprimentos efetivamente registrados; estimativas devem ser identificadas separadamente.
   - Gerar saída documental do escopo suportado com IDs, premissas, pendências, status, fontes e referências. PDF só após verificar dependências já suportadas; caso contrário, documentar formato não implementado.

5. **Exportação e validador cruzado**
   - Implementar formatos sustentados pelo projeto e testes de round-trip em seus campos/IDs.
   - Comparar revisão, cálculo, topologia, cargas, fases, proteção e condutor entre quadro/diagrama/relatório; divergência bloqueia pacote.

6. **Prévia, acessibilidade e QA**
   - Exercitar SVG/HTML em viewport pequeno e desktop, foco/semântica, escape de conteúdo e impressão, conforme UI disponível.
   - Produzir pareceres separados QA-01 (arquitetura/testes), QA-02 (escopo de engenharia; sem homologação humana) e QA-03 (integração/segurança/UX).
   - Corrigir achados impeditivos e repetir os testes afetados.

7. **Fechamento**
   - Atualizar relatório F10 e a fonte de estado canônica com SHAs, comandos, resultados e arquivos.
   - Marcar DONE somente se critérios essenciais e três revisões aplicáveis estiverem comprovados. Caso contrário, manter IMPLEMENTED/VALIDATING/BLOCKED com pendências concretas.

## Evidências mínimas de conclusão

- API e regressões relevantes passam no SHA final.
- Três workflows remotos de API, AIOX e Chromium concluídos com sucesso no mesmo SHA.
- Artefatos da mesma revisão têm identidade e dados coerentes; diferenças são bloqueadoras.
- Exportação suportada é reproduzível; QA visual/acessibilidade foi executado quando houver interface.
- QA-01/02/03 e relatório F10 citam provas reais; não há declaração de conformidade profissional/normativa sem parecer e fonte apropriados.
