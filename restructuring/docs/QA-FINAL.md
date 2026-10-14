# QA final — núcleo integrado SIE 2.0

## Critérios de aceite executáveis

| Critério | Verificação | Resultado esperado |
|---|---|---|
| Entrada inválida | teste unitário/API | resposta 422 e mensagem explicável |
| Corrente inválida | teste unitário | rejeição de zero, negativo, NaN e infinito |
| Condutor | teste unitário | menor seção suficiente é escolhida |
| Proteção | teste unitário | somente `Ib ≤ In ≤ Iz` é aceito |
| Queda de tensão | teste unitário | fórmula e percentual são retornados |
| Gate | teste unitário/API | sem evidência completa, não libera uso normativo |
| UI | revisão manual | formulário, resultado, aviso e responsividade são visíveis |

## Execução

```powershell
cd restructuring\apps\api
python -m pytest -q
```

## Decisão de qualidade

O módulo pode ser classificado como **pronto para teste local controlado** quando todos os testes passarem e a interface se comunicar com a API. Ele não pode ser classificado como motor normativo completo até que catálogos/fatores sejam versionados, fontes sejam auditadas e os cenários de referência estejam aprovados.

## Segurança e gate — regressões adicionais

- Requisições que declaram `dados_validados=true` e `testes_independentes=true` devem continuar com `PENDENTE` e `liberado_para_uso_normativo=false`.
- Enquadramento EDP retorna apenas candidato e nunca libera o padrão automaticamente.
- CORS permite apenas a UI local conhecida; não é mecanismo de autenticação.
- Frontend escapa campos textuais exibidos a partir da resposta, impedindo inserção direta de HTML arbitrário.
- Aprovação normativa futura depende de credenciais, referência auditada, evidência imutável e assinatura/autoridade verificável no servidor.
