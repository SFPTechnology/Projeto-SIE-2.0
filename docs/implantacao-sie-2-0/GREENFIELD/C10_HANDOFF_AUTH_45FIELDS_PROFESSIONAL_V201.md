# C10 — Encaminhamento dos três bloqueios: Auth, 45 campos, parecer elétrico

**Emissão:** 28/10/2026. **Escopo:** SIE 2.0 / PR #11 / Bloco C / DEVELOPMENT.
**Ações no Supabase:** nenhuma escrita em origem, destino ou ambiente remoto.

## Agentes especializados mobilizados
| Agente | Função | Entrega |
|---|---|---|
| A-IDENT / IAM + Supabase | Verificar sujeito JWT confiável, existência real em Auth, escopo de 5 IDs | `v201_c_auth_owner_binding.py`, testes negativos; **AUTH_NOT_CREATED** |
| A-LEGACY / Engenheiro de Dados | Auditar os 45 campos sem regra, sem perder valores originais | `C02_REVISAO_SEMANTICA_45_CAMPOS_V201.csv` e `v201_c_field_review.py` |
| A-ELEC / Engenheiro Eletricista | Avaliar 11 famílias de ensaios e premissas com referências comprováveis | `C04_C05_DOSSIE_ACEITE_PROFISSIONAL_V201.json`, aguardando revisor habilitado |
| A-NORM / Normas e Concessionária | Conferir fontes licenciadas, versões, aplicação e P03/P06/Rca/XL | Registro de requisitos e parâmetros não aprovados |
| A-SEG / Segurança | Evitar aprovação por JSON editável, UUID fictício, escopo parcial | Testes fail-closed |
| A-QA / DevOps independente | Executar API, PG17, browser e qualidade no mesmo SHA | Evidências de CI; checkpoint final exige read-back |

## Frente A — titularidade e identidade Auth
O responsável declarou que os cinco projetos são seus e deseja migrar todos. A atribuição está registrada, mas o destino `fozrymsidnaxmuvxxfhh` tinha **zero usuários em auth.users** em consulta SELECT. Nenhuma chave UUID sintética confere identidade.

**Única etapa pessoal indispensável para esta frente:** criar ou confirmar uma conta real de usuário na plataforma **SIE 2.0**, usando o fluxo legítimo Supabase Auth e um email ao qual o titular tenha acesso, confirmar o cadastro e autenticar-se. Pode-se iniciar pela interface de Auth do próprio Supabase (Authentication > Users); NÃO criar linhas diretamente por INSERT em `auth.users`. Um login como administrador do Dashboard não comprova uma sessão da aplicação.

**Read-back técnico obrigatório, somente mediante solicitação futura:** conferir registro `auth.users.id` não nulo, confirmação do endereço conforme política de Auth e JWT validado pelo backend da aplicação; registrar vínculo 5/5 desse UID com os IDs legados e comprovação independente de titularidade. Não registrar email, senha ou JWT no repositório.

**Bloqueio atual:** `USER_ACCOUNT_NOT_PRESENT`, `OWNER_BINDING_UNAPPLIED`. A ferramenta `check_real_auth_user` aceita conexão de leitura injetada e sujeito JWT validado pelo backend; a consulta isolada não concede aprovação final.

## Frente B — auditoria semântica dos 45 campos
Foram elaboradas 45 decisões **de tratamento proposto** por nome exato de origem:
- **22 campos** pertencem a tabelas sem registros no read-back. Há contrato de arquivo condicional, mas o surgimento de novas linhas exige nova revisão.
- **15 campos** devem ficar preservados como dados originais, sem inferência/normalização elétrica; vínculo, resultado ou tempo histórico são preservados e não se tornam Auth/norma.
- **7 campos** contêm fatores de potência, overrides, resultados de condutores, disjuntores ou queda de tensão e necessitam revisão elétrica verificável.
- **1 campo** (`dependencias.nome_personalizado`) tem proposta de apresentação no nome do ambiente e requer validação de modelo e UX, mantendo o nome literal do legado.

**Conclusão:** 45/45 revisados/classificados para preservação governada. **Não significa** 45/45 transformações canônicas autorizadas; nenhuma decisão pode sobrescrever fontes ou criar aprovação técnica. Confirmar a disposição dos 7 campos elétricos e o uso do nome no aceite técnico/funcional.

## Frente C — pacote de aceite profissional
O dossiê contém 11 casos E01–E11:
1. Iluminação/TUG e condições de áreas;
2. TUE, FP e topologia 1/3 fases;
3. Demanda, divisão e balanceamento;
4. Condutores/correções/instalação;
5. Queda de tensão com Rca/XL;
6. Proteção contra sobrecarga/curto/I2;
7. DR e DPS;
8. Aterramento/PE/neutro;
9. Concessionária EDP e padrão de entrada;
10. Histórico de fatores/resultados legados;
11. Negativos, hashes, versão normativa e reprodução.

**Aceite necessário de um profissional habilitado:** validar a edição/licença da norma, parâmetros e limites, exemplos golden, condições de aplicação, falhas negativas, restrições dos módulos. Emitir documento de aprovação ou reprovação com identificação do revisor, registro profissional aplicável, escopo, data, documentos/snapshots revisados e assinatura cuja autenticidade possa ser conferida. Verificar necessidade de ART/registro de responsabilidade conforme natureza concreta da atividade; não inventar número de registro, responsabilidade nem assinatura.

Nenhuma inteligência artificial, teste automatizado ou campo `APPROVED` editável substitui o parecer. Testes `test_c04_professional_review_gate_v201.py` rejeitam signoff fictício e omissão de casos.

## Gates de saída
| Critério | Situação após execução |
|---|---|
| Seleção do proprietário sobre os cinco projetos | DECLARED |
| Conta Auth legítima no destino | NOT_CREATED |
| Vínculo real de Auth→5 IDs | BLOCKED |
| 45 campos classificados e com rota de preservação | DEVELOPMENT_REVIEWED |
| 7 campos elétricos homologados | PENDING_PROFESSIONAL |
| Aceite profissional dos 11 ensaios e normas | PENDING_EXTERNAL_SIGNOFF |
| DDL/ETL remoto e homologação E02–E06 | NOT_AUTHORIZED |
| **GC integral** | **BLOCKED** |

Somente liberar escrita remota após autorização específica e backups; não realizar merge, deploy ou alterações em `main`, F12 ou SIE original.
