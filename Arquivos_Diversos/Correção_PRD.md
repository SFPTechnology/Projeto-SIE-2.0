# Itens que devem ser atendidos para a correção do PRD

## 1. Visão e declaração do problema

### 1.1 Problema

O SIE possui uma seção "Diagrama unifilar interativo do projeto" que funciona como visualização operacional no frontend — canvas SVG navegável com inspector lateral, busca, filtros e agrupamento. Essa seção atende à necessidade de inspeção e rastreabilidade dentro do produto web, mas não produz as saídas técnicas que o engenheiro eletricista precisa para aprovar, imprimir, arquivar e submeter o projeto a concessionárias e órgãos de fiscalização.

Especificamente, o produto não gera:

- Diagrama unifilar em formato CAD (DXF) para integração com AutoCAD, BricsCAD ou outros softwares de engenharia utilizados no mercado brasileiro.
- Diagrama unifilar em PDF vetorial com carimbo profissional, legenda ABNT, e qualidade de impressão em escala (A3, A4, A1).
- Diagrama unifilar em SVG técnico com simbologia IEC 60617 normalizada, rastreável e editável em editores vetoriais (Inkscape, Illustrator).

Os botões de exportação SVG, PDF e DXF estão presentes na interface (`UnifilarExportBar`) mas desabilitados, com a mensagem informando que dependem de uma camada Python opcional.

### 1.2 Visão

Construir a seção **"Diagrama Unifilar Completo"** como um pipeline Python que consome o contrato canônico `UnifilarGraph.json` já produzido pela seção existente e gera três saídas vetoriais de qualidade profissional (SVG, DXF, PDF), com simbologia IEC 60617, layout determinístico, carimbo ABNT, e rastreabilidade completa de cada elemento gráfico ao circuito de origem.

O pipeline é uma camada de projeção — não recalcula regras normativas, não inventa valores, e não depende do frontend para operar.

IMPORTANTE CORREÇÃO: Todas as seções do PRD: 3. Escopo; 4. Relação com a seção existente; 5. Arquitetura do pipeline; 6. Contrato de entrada — UnifilarGraph; 7. Catálogo de simbologia IEC 60617; 8. Motor de layout Python; 9. Renderizador SVG técnico; 10. Renderizador DXF CAD; 11. Renderizador PDF vetorial; 12. Carimbo e legenda profissional; 13. CLI de exportação; 14. Endpoint FastAPI; 15. Integração com o frontend; 16. Conformidade normativa; 17. Requisitos não-funcionais; 18. Estratégia de testes; 19. Plano de entrega faseado; 20. Critérios de aceitação por fase
21. Registro de riscos; 22. Dependências técnicas e restrições; e 23. Glossário, devem ser relacionadas com a reestruturação da seção "Diagrama Unifilar Completo", e não devem ser incorporadas a seção "Diagrama unifilar interativo do projeto"

Assim,o PRD deve ser ajustado para atender integralmente essa correção.


























1. Visão e declaração do problema
2. Usuários e personas
3. Escopo
4. Relação com a seção existente
5. Arquitetura do pipeline
6. Contrato de entrada — UnifilarGraph
7. Catálogo de simbologia IEC 60617
8. Motor de layout Python
9. Renderizador SVG técnico
10. Renderizador DXF CAD
11. Renderizador PDF vetorial
12. Carimbo e legenda profissional
13. CLI de exportação
14. Endpoint FastAPI
15. Integração com o frontend
16. Conformidade normativa
17. Requisitos não-funcionais
18. Estratégia de testes
19. Plano de entrega faseado
20. Critérios de aceitação por fase
21. Registro de riscos
22. Dependências técnicas e restrições
23. Glossário