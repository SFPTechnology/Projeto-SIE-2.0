# F12 — manutenção normativa, versões históricas e documentação as-built

**Escopo:** política de governança para implantação futura; sem homologação de normas nesta fase.

## Ciclo de revisão
- Inventariar por regra: organismo emissor, identificador, edição, data de vigência, trecho/tabela, escopo, hash da evidência, revisão que aprovou, impacto em cálculos/instalações e data de próxima revisão.
- Monitorar publicações oficiais da ABNT, requisitos aplicáveis NR-10 e padrões da concessionária conforme região/serviço, com periodicidade aprovada pelo responsável e evento extraordinário quando mudança normativa for identificada. **Periodicidade ainda não aprovada; não inventar calendário legal fixo.**
- Ao detectar revisão, abrir mudança versionada; comparar grandezas e limites, comprovar fontes primárias e casos independentes, obter parecer de engenheiro eletricista responsável, validar casos de regressão e publicar edição nova **sem reescrever os históricos**.
- Associar todo documento e `CalculationRun` ao snapshot de regras, hash, revisão, premissas e template usado. Mudanças relevantes originam nova revisão; documentos antigos recebem `STALE` se a lógica de dependências assim exigir, preservando evidência histórica.
- Depreciar regra com aviso de substituição, versão final e justificativa; impedir uso novo de regra revogada fora de exceção formal aprovada, nunca atualizar silently um projeto antigo.

## Política as-built para instalação real
Apenas após obra/inspeção real: registrar local, responsável técnico, data, revisão da planta, circuitos, mudanças de trajeto/cargas/disjuntores/condutores, medições, instrumentos, laudos, fotos pertinentes, não conformidades e aceites. Associar cada diferença a item de projeto e revisão, com auditoria; exigir validação profissional e documentação pertinente conforme caso. **Nenhum as-built real foi produzido.**

## Limites e próximos gates
F06–F08 têm recortes de regras/catálogos estudados e F09/F10 integram dados consultivos. F12 não aprova eletrodutos, curto-circuito, seleção, SPDA, fotovoltaicos, recarga de veículos ou instalações especiais além do que já estava validado. Qualquer declaração de NBR 5410/5419, NR-10 e padrões de concessionária depende de fontes confiáveis, aplicabilidade e evidência assinada por profissional responsável.
