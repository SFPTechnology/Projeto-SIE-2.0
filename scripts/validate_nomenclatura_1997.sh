#!/bin/bash
# Script: Validação de nomenclatura 1997 (AC-DC-25)
# Story: DC-1
#
# Rejeita referências à numeração de tabelas da edição 1997 da NBR 5410.
# Padrões proibidos: Tab. 28|31–34|35–42|37|43 como agrupamento
#
# Código, dados e UI devem referir exclusivamente numeração 2004:
# Tab. 30, 33, 36–48, 58

set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
PATTERNS_PROIBIDOS=(
  "Tab\. 28"
  "Tab\. 31"
  "Tab\. 32"
  "Tab\. 33" # NOTA: Tab. 33 é 2004, mas se encontrado no contexto "antiga" marca
  "Tab\. 34"
  "Tab\. 35"
  "Tab\. 42.*agrupamento" # Especificamente "Tab. 42 como agrupamento" é 1997
  "Tab\. 43"
  "Tabela 31"
  "Tabela 32"
  "Tabela 35"
  "Tabela 42"
  "Tabela 43"
)

echo "🔍 Validando nomenclatura de tabelas (AC-DC-25)..."
echo "   Procurando padrões de numeração 1997 em código, dados e UI..."
echo ""

ENCONTRADOS=0

for pattern in "${PATTERNS_PROIBIDOS[@]}"; do
  if grep -r --include="*.ts" --include="*.tsx" --include="*.js" --include="*.sql" --include="*.md" \
    "$pattern" "$REPO_ROOT/src" "$REPO_ROOT/tests" "$REPO_ROOT/supabase" "$REPO_ROOT/docs" 2>/dev/null | \
    grep -v "numeração de tabelas da edição 1997" | \
    grep -v "edição 1997" | \
    grep -v "#comentário"; then

    echo "❌ ENCONTRADA referência PROIBIDA: $pattern"
    ENCONTRADOS=$((ENCONTRADOS + 1))
  fi
done

echo ""
if [ $ENCONTRADOS -eq 0 ]; then
  echo "✅ PASS: Zero referências a numeração 1997 detectadas"
  exit 0
else
  echo "❌ FAIL: $ENCONTRADOS referência(s) a numeração 1997 encontrada(s)"
  echo "   Numeração obrigatória: Tab. 30, 33, 36–48, 58 (edição 2004)"
  exit 1
fi
