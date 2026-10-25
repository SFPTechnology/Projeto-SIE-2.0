# F11 — candidato, reprodução e comissionamento

## Candidato congelado para auditoria inicial

- Repositório: `SFPTechnology/Projeto-SIE-2.0`.
- Base exata: `540f2c8e7e61a1efb6bf71abcedc8768d7086914`, tree `e1190eae49478ddf34cd372a71056c113a858270`, branch `feat/f09-concessionarias-especializadas`.
- Incremento F11: branch `feat/f11-qa-integrado`; o SHA final será registrado após testes e CI. Alterações posteriores exigem revalidação.
- F10 código: `9623b4ad0a1710edf36ca05423f078b16b9442f0`, 1181 testes API registrados e três CI de código no estado; a base documental `540f2c8` possui três runs próprios concluídos com sucesso (API `40142136768`, AIOX `40142136778`, Chromium `40142136788`).
- Pacote Python: `restructuring/apps/api/pyproject.toml`, `sie-api 0.1.0`, Python >=3.11; faixas FastAPI >=0.110,<1, Pydantic >=2,<3, Uvicorn >=0.27,<1, ReportLab >=4,<5; pytest/httpx/pypdf/playwright opcionais. Estas faixas não congelam versões transitivas: capturar ambiente resolvido no CI para reprodução binária.
- JS: `package.json` na raiz e `.aiox-core/package-lock.json` para dependências do framework; CI instala com `npm ci --prefix .aiox-core` em `.github/workflows/sie-orchestrator-quality.yml`.
- Dados versionados: `restructuring/apps/api/sie_api/data/*.json`; entradas de cenário e resultados esperados nos testes versionados. Não usar dados de produção.
- Persistência: esquema SQLite em `storage.py`, registros e migração reversível em `data_lifecycle.py`; procedimentos de restauração devem ser ensaiados em banco temporário, nunca em produção.
- Evidência F10: `docs/implantacao-sie-2-0/F10/` e `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`. Aprovação de software não implica homologação normativa ou profissional.

## Inspeção e ensaios de campo — checklist aplicável a projeto real

Preencher por profissional habilitado, com identificação do projeto, revisão, local, data, instrumentos e certificados de calibração, condições de ensaio, resultados e assinatura. **Estado inicial de todos os itens: NÃO EXECUTADO.** Este repositório não contém laudo de campo.

| Item | Registro requerido | Situação |
|---|---|---|
| Confronto as built e documentação | Planta, circuitos, identificação e desvios da revisão | NÃO EXECUTADO |
| Inspeção visual | Condutores, proteção, identificação, acessibilidade, aterramento e invólucros conforme escopo real | NÃO EXECUTADO |
| Continuidade e isolamento | Método, instrumento, condições, valores e critérios aplicáveis verificados pelo responsável | NÃO EXECUTADO |
| Polaridade e funcionamento | Circuitos medidos, resultados e não conformidades | NÃO EXECUTADO |
| Proteções e seccionamento | Ensaios cabíveis, ajustes, atuação e coordenação com documentação validada | NÃO EXECUTADO |
| Aterramento e equipotencialização | Topologia, medições e interpretação responsável | NÃO EXECUTADO |
| Entrega e aceite | Correções, retestes, responsável técnico e aprovação documentada | NÃO EXECUTADO |

Resultados computacionais da F11 só cobrem os cenários reproduzidos. Qualquer declaração de conformidade NBR 5410, NBR 5419, NR-10 ou concessionária depende de fonte aplicável, verificação profissional e evidências do projeto e da instalação.
