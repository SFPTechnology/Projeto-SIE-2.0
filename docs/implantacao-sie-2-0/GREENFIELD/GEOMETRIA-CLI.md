# SIE 2.0 — Incremento greenfield GF-001

Este incremento implementa geometria retangular independente do codigo original. Nao implementa iluminacao, TUG, DR, protecao, demanda, conformidade normativa, persistencia ou autenticacao.

## Fonte legada consultada (apenas leitura)
- `SFPTechnology/sistema-de-instala-es-el-tricas-sie/src/domain/calculo/geometria.ts`: area = L*C; perimetro util = 2*(L+C)-exclusao.
- `REFERENCIA-INTEGRAL-SISTEMA.md`: requisitos F-01/F-02, dependencias e revisoes.
- `docs/supabase/0001_init.sql` do legado: estrutura consultada, NAO aplicada no novo banco.

## Executar o CLI
Na raiz do repositorio, com Python 3.11+:
```bash
PYTHONPATH=restructuring/apps/api python -m sie_api.nextgen_geometry_cli --input projeto.json
```

Exemplo de `projeto.json`:
```json
{
  "project_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
  "revision_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
  "rooms": [{"room_id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc", "name": "Sala", "width_m": "3.2", "length_m": "4.1", "excluded_perimeter_m": "1.5"}]
}
```

Saida: area `13.12 m2`, perimetro bruto `14.6 m`, util `13.1 m`, `source_sha256`, vinculo `revision_id`, `rectangular_only` e `NOT_EVALUATED`. Numeros sao strings decimais; nao ha arredondamento implicito. Erros retornam JSON em stderr e codigo 2.

## Testes locais
```bash
PYTHONPATH=restructuring/apps/api python -m pytest restructuring/apps/api/tests/test_nextgen_geometry.py -q
```

Resultado registrado: 22 casos PASS em teste isolado, Python 3.13. Suíte integral e CI do SHA final devem ser conferidos separadamente.

## Bloqueios e próximos gates
1. Validar acesso e inventario de schemas/migrations do projeto Supabase `fozrymsidnaxmuvxxfhh`.
2. Projetar e homologar entidades projeto/revisao/ambiente e RLS, sem reutilizar cegamente o schema do SIE original.
3. Integrar CLI a API autenticada, persistencia revisionada e posteriormente frontend.
4. Validar geometrias irregulares e regras eletricas mediante fonte normativa, separado do motor geométrico.
5. Preservar `main`, F00-F12, SIE original, Hostinger e Supabase de producao. F12 segue HUMAN_REQUIRED/NO-GO.
