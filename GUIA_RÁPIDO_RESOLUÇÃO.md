# ⚡ Guia Rápido: Resolver Problema de Projetos Invisíveis

**Tempo estimado:** 2-3 minutos

---

## 🎯 O Que Foi Corrigido

O arquivo `.env` com as credenciais do Supabase foi movido para o diretório correto:

```
❌ Antes:  Projeto_SIE/.env
✅ Agora:  Projeto_SIE/sistema-de-instala-es-el-tricas-sie-main/.env
```

---

## 📋 Checklist - Siga esses passos

### Passo 1: Parar o Servidor (se estiver rodando)

```bash
# No terminal/prompt, pressione:
Ctrl + C
```

**Status esperado:** Prompt volta ao normal

---

### Passo 2: Limpar Node Modules e Cache (Recomendado)

```bash
cd sistema-de-instala-es-el-tricas-sie-main

# Limpar cache npm
npm cache clean --force

# Remover node_modules (opcional, mas recomendado)
rm -rf node_modules  # no Mac/Linux
# ou
rmdir /s node_modules  # no Windows
```

---

### Passo 3: Instalar Dependências

```bash
cd sistema-de-instala-es-el-tricas-sie-main
npm install
```

**Tempo:** ~2-3 minutos

**Status esperado:** 
```
added XXXX packages in Xs
```

---

### Passo 4: Iniciar o Servidor

```bash
npm run dev
```

**Status esperado:**
```
  VITE v8.0.16  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

---

### Passo 5: Abrir no Navegador

1. Abra: **http://localhost:5173**
2. Pressione: **Ctrl + Shift + Del** (limpar cache)
3. Selecione tudo e clique "Limpar"
4. Volte ao navegador
5. Pressione: **Ctrl + R** (recarregar)

---

## 🎉 Resultado Esperado

Você deve ver:

```
Projetos

Projeto 1
11 dependência(s) · criado em 19/06/2026, 16:02

[→]
```

### ✅ Validações

- [ ] "Projeto 1" aparece na lista
- [ ] Tem 11 dependências
- [ ] Data correta: 19/06/2026
- [ ] Clicável e funcional
- [ ] Sem erros no console (F12)

---

## 🔧 Se Ainda Não Funcionar

### Debug 1: Verificar Arquivo .env

```bash
cat sistema-de-instala-es-el-tricas-sie-main/.env | grep SUPABASE
```

**Esperado:**
```
APP_SUPABASE_URL=https://hlbksclcandbsyqrsbmx.supabase.co
APP_SUPABASE_SERVICE_ROLE_KEY=
```

### Debug 2: Verificar Console do Navegador

1. Abra: **F12** ou **Ctrl + Shift + I**
2. Aba: **Console**
3. Procure por erros vermelhos
4. Se houver erros, copie e relate

### Debug 3: Verificar Logs do Servidor

Verifique o terminal onde `npm run dev` está rodando:
- Procure por "Supabase"
- Procure por erros em vermelho
- Copie as mensagens de erro

---

## 📞 Se Precisar de Ajuda

**Informações para reportar:**

1. **Status do servidor:** Rodando? Qual port?
2. **Console do navegador:** Tem erros?
3. **Logs do servidor:** Que mensagens aparecem?
4. **Screenshot:** Do que você vê no navegador

---

## 📊 Estrutura de Dados (Supabase)

### Projeto Visível Agora

```json
{
  "id": "proj-1",
  "nome": "Projeto 1",
  "criado_em": "2026-06-19T16:02:28.857+00:00",
  "dependenciaIds": [
    "dep-1781807783475",
    "dep-1781807827642",
    "dep-1781808008186",
    "dep-1781808149544",
    "dep-1781808373935",
    "dep-1781808426942",
    "dep-1781808562385",
    "dep-1781809514324",
    "dep-fix-check-...",
    "dep-test-now",
    "Quintal"
  ]
}
```

---

## 🚨 Nota Importante

⚠️ **"Projeto Teste 1" vai desaparecer após reiniciar o servidor**

Razão: Era armazenado apenas em memória volátil

Solução: Recrear após sincronização (será persistido no Supabase)

---

## 🎓 O Que Aprendemos

| Problema | Causa | Solução |
|----------|-------|---------|
| Supabase não conectava | .env no lugar errado | Mover arquivo .env |
| Sistema usava memória | Env não carregado | Arquivo copiado |
| Projetos invisíveis | Repo type errado | Supabase agora ativo |

---

**Próximo passo:** Execute os passos acima e verifique se "Projeto 1" aparece! 🚀
