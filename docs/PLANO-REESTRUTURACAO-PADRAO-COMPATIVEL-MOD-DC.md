# Plano de reestruturação e correção — Padrão compatível / MOD-DC

**Responsável pela execução:** `@dev`  
**Escopo:** diagnóstico do seletor de padrão compatível e desbloqueio das telas dependentes (Correntes e Dimensionamento de condutores).  
**Projeto afetado:** `proj-54a80990-0c54-433e-991e-b89dd48e5c91`  
**Evidências:** screenshots `Screenshot_200.jpg` e `Screenshot_201.jpg`, código atual e testes do módulo.

## 1. Resultado esperado

Para cargas que exigem 127 V e 220 V, com demanda de 3,367 kVA (caso da evidência), o sistema deve:

1. apresentar `BI-127-220` como opção habilitada;
2. permitir a seleção e persistência do padrão;
3. recalcular o resultado de padrão de entrada;
4. remover o aviso `Padrão de entrada não selecionado` do MOD-DC;
5. liberar o dimensionamento parcial de condutores, desde que os demais parâmetros do MOD-DC estejam válidos.

O sistema não deve alterar as tensões fixas ou as cargas cadastradas.

## 2. Diagnóstico comprovado

### 2.1 A UI não decide compatibilidade

`src/components/app/FornecimentoSelector.tsx` desabilita cada item quando seu ID não está em `resultado.candidatosValidos`. Portanto, todos os itens aparecem como “incompatíveis” quando o domínio retorna `status: "sem-padrao"` ou quando o catálogo recebido pela tela não corresponde ao catálogo vigente.

O botão também fica desabilitado quando não há valor selecionado. Esse comportamento é consequência do resultado do domínio, não a causa primária.

### 2.2 O filtro de compatibilidade é simultaneamente tensão + faixa

`src/domain/calculo/padrao-entrada.ts` aplica:

- demanda entre `potencia_min_kVA` e `potencia_max_kVA`;
- todas as tensões requeridas presentes em `tensoes_ofertadas`.

Para o caso da imagem, `MONO-127`, `MONO-220` e `TRI-220-380` não cobrem simultaneamente `{127, 220}`. O único candidato esperado é `BI-127-220`, desde que esteja com faixa válida.

### 2.3 A configuração persistida é fonte de risco

`padrao_entrada_config.catalogo` é carregado do projeto e pode conter um catálogo antigo. A tela pode continuar recebendo o registro legado se o build corrigido não estiver publicado ou se a leitura não tiver sido executada após a migração.

O sintoma da imagem é compatível com `BI-127-220` persistido com piso antigo de 8 kVA: a demanda de 3,367 kVA fica abaixo do piso e o candidato é removido.

### 2.4 O MOD-DC está bloqueando corretamente

O aviso da segunda imagem (`Padrão de entrada não selecionado`) é uma proteção downstream. O dimensionamento depende de `contratos.saidaA`/padrão de entrada selecionado; sem seleção válida, não há tensão/sistema confiável para dimensionar condutores. Não remover esse bloqueio na UI.

### 2.5 O catálogo atual não é uma fonte normativa definitiva

`src/domain/nbr/catalogo-fornecimento.data.json` declara explicitamente `GENERICO` e `VERIFICAR`. Logo, os limites 0–8, 0–12, 0–25 e 15–75 kVA são parâmetros de aplicação, não comprovação de limites da EDP.

Além disso, o catálogo mistura `BI-127-220` e `TRI-220-380`. A norma técnica da EDP consultada lista, para EDP São Paulo, tensões padronizadas 220/127 V, enquanto 380/220 V aparece indicada para EDP Espírito Santo. A fonte deve ser parametrizada por distribuidora/região antes de ser tratada como catálogo normativo.

## 3. Reestruturação proposta

### Fase P0 — corrigir o caso bloqueante

1. Manter `BI-127-220` com:
   - `sistema: "bi"`;
   - `tensoes_ofertadas: [127, 220]`;
   - `potencia_min_kVA: 0`;
   - `potencia_max_kVA: 25`.
2. Normalizar catálogo persistido legado por ID `BI-127-220`, corrigindo sistema, tensões e faixa.
3. Persistir a configuração normalizada no primeiro `GET`/obtenção do projeto, sem alterar cargas e sem gerar override automático.
4. Rejeitar ou diagnosticar catálogo persistido estruturalmente inválido antes do cálculo; não mascarar erro como “nenhum padrão”.
5. Garantir que a API de leitura devolva o catálogo normalizado que a UI realmente usa.

### Fase P1 — tornar o diagnóstico acionável

1. Expor no retorno do domínio/API:
   - `motivo` (`tensao-nao-ofertada`, `demanda-abaixo-do-piso`, etc.);
   - `potencia_demandada_VA`;
   - `tensoes_requeridas`;
   - candidatos rejeitados e motivo por padrão.
2. Na UI, manter opções desabilitadas, mas mostrar tooltip/descrição objetiva, por exemplo:
   - “não cobre 127 V”;
   - “demanda abaixo do piso de 8 kVA”;
   - “demanda acima do teto de 25 kVA”.
3. Quando nenhum candidato for válido, apresentar o diagnóstico do domínio no bloco de aviso, em vez de somente “selecione um padrão”.
4. Não habilitar opção incompatível apenas para permitir o avanço; a seleção manual deve continuar sujeita ao mesmo cálculo e validação da API.

### Fase P2 — separar catálogo genérico de catálogo de distribuidora

1. Introduzir identificação explícita de fonte: distribuidora, UF/região, versão e referência documental.
2. Manter o catálogo genérico apenas como fallback de demonstração/teste, claramente rotulado.
3. Criar catálogo EDP São Paulo separado, baseado na norma de fornecimento vigente da EDP e em tabela de limites de atendimento por sistema/faixa.
4. Não afirmar que a NBR 5410 define os limites comerciais de ligação. A NBR 5410 deve ser usada para requisitos da instalação de baixa tensão; tensões e faixas de atendimento devem vir da distribuidora/concessionária.
5. Versionar a fonte e registrar data de verificação. Se a referência estiver ausente ou expirada, bloquear publicação do catálogo normativo e emitir diagnóstico de configuração.

### Fase P3 — contrato estável com Correntes/MOD-DC

1. Fazer Correntes e Dimensionamento consumirem somente o contrato canônico derivado do padrão selecionado.
2. Se não houver padrão selecionado, manter o bloqueio e indicar a dependência upstream.
3. Após seleção bem-sucedida, invalidar/recarregar queries de padrão de entrada, correntes e dimensionamento.
4. Testar navegação direta para MOD-DC com e sem seleção, evitando estado stale no cache do React Query.

## 4. Alterações técnicas para `@dev`

### Código

- `src/domain/nbr/catalogo-fornecimento.ts`
  - centralizar normalização/migração;
  - validar assinatura, tensões, faixa e referência;
  - manter função pura e idempotente.
- `src/domain/servicos/servico-padrao-entrada.ts`
  - normalizar antes de calcular;
  - persistir apenas quando houve mudança;
  - não sobrescrever override manual válido.
- `src/domain/calculo/padrao-entrada.ts`
  - preservar filtro de tensão + faixa;
  - adicionar rejeições explicáveis por padrão.
- `src/components/app/FornecimentoSelector.tsx`
  - renderizar motivo de incompatibilidade;
  - preservar desabilitação de opções realmente inválidas.
- Rotas/API de padrão de entrada
  - validar e devolver catálogo normalizado;
  - não confiar apenas no schema de escrita para dados legados já persistidos.

### Dados e persistência

1. Ler o registro do projeto afetado antes de qualquer alteração.
2. Fazer backup/export do `padrao_entrada_config`.
3. Aplicar migração somente ao item `BI-127-220` e somente aos campos definidos neste plano.
4. Reconsultar o registro e confirmar `catalogo`, `resultado` e auditoria.
5. Não executar update amplo em todos os projetos sem script idempotente e relatório de alterações.

## 5. Matriz de aceitação do catálogo atual

| Padrão | Tensões declaradas | Faixa atual | Caso 127/220 | Ação |
|---|---:|---:|---|---|
| MONO-127 | 127 | 0–8 kVA | Rejeitar: não cobre 220 V | Manter somente para cargas 127 V |
| MONO-220 | 220 | 0–12 kVA | Rejeitar: não cobre 127 V | Manter somente para cargas 220 V |
| BI-127-220 | 127/220 | 0–25 kVA | **Candidato válido** para 3,367 kVA | Corrigir/migrar e validar na fonte EDP |
| TRI-220-380 | 220/380 | 15–75 kVA | Rejeitar: não cobre 127 V e piso excede demanda | Separar por distribuidora/região |

Essa matriz é uma avaliação lógica do catálogo atual. Ela não substitui a confirmação dos limites de ligação da EDP.

## 6. Testes obrigatórios

### Domínio

- cargas `{127, 220}`, demanda `3,367 kVA` → `status: ok`, candidato `BI-127-220`;
- BI legado com piso 8 kVA → normaliza para 0 kVA;
- BI com sistema/tensões inconsistentes → normaliza por ID;
- cada padrão rejeitado retorna motivo específico;
- demanda abaixo do piso real → nenhum candidato, diagnóstico correto;
- demanda acima do teto → diagnóstico de teto;
- tensões não ofertadas → diagnóstico de tensão.

### API/persistência

- `GET` de projeto legado retorna catálogo normalizado;
- primeiro `GET` persiste a migração uma única vez;
- `PUT` rejeita catálogo estruturalmente inválido;
- override inválido continua rejeitado;
- projeto customizado sem BI não recebe BI artificialmente.

### UI/E2E

- BI habilitado no seletor para o caso da imagem;
- seleção e salvamento removem o aviso de pendência;
- MOD-DC deixa de mostrar “Padrão de entrada não selecionado” após seleção;
- sem seleção, MOD-DC permanece bloqueado com mensagem clara;
- recarga de página preserva seleção e resultado.

## 7. Critérios de conclusão

`@dev` pode marcar a implementação pronta somente quando:

- o caso da imagem estiver reproduzido e resolvido por teste automatizado;
- catálogo legado estiver normalizado e persistido;
- catálogo customizado não tiver regressão;
- `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` passarem;
- story e File List estiverem atualizados;
- a publicação do build for encaminhada ao `@devops`;
- a confirmação normativa EDP/região estiver registrada separadamente da regra NBR 5410.

## Referências técnicas

- [Norma técnica EDP — distribuição em baixa tensão PT.DT.PDN.00059](https://www.edp.com.br/media/klki3ub5/norma-tecnica-baixa-tensao-00059-v5.pdf), especialmente Tabela 001 de tensões nominais padronizadas.
- [Resumo de escopo da ABNT NBR 5410](https://loja.br.abb.com/blog/post/nbr-5410): requisitos de instalações elétricas de baixa tensão; não é a fonte dos limites comerciais de atendimento da concessionária.

