# Inventory — banana-slides

## Identidade

- **Repo:** `Anionex/banana-slides`
- **Clone local:** `../bench/banana-slides`
- **Licença:** AGPL-3.0
- **Prioridade:** P1
- **Papel na stack:** benchmark de UX prompt-to-edit, edição regional, estilo e vídeo.

## Evidência Lida

- `../bench/banana-slides/README_EN.md`

## Capacidades Fortes

| Capacidade | Observação |
|---|---|
| Prompt-to-edit | Forte foco em edição por linguagem natural. |
| Edição local/regional | Otimização de página ou região específica. |
| Style references | Usa referências visuais e templates. |
| Export PPTX/PDF | Exporta apresentações e trabalha em direção a editabilidade. |
| Vídeo com voz/subtítulos | FFmpeg e pipeline de explicação em vídeo. |

## Limitações

- AGPL-3.0: alto risco para copiar código em produto privado.
- Forte dependência de modelos/serviços específicos em partes do fluxo.
- A maturidade de export editável ainda deve ser validada localmente.

## O Que Absorver

1. UX patterns de prompt-to-edit.
2. Modelo mental de edição por região/slide.
3. Preview + confirmação antes de aplicar alteração.
4. Fluxo de vídeo apenas como referência P2.

## O Que Não Copiar Diretamente

- Código AGPL sem decisão jurídica explícita.
- Dependências de provider que não encaixem no BYOK/local.
- Fluxo de vídeo no MVP.

## Critério de Aceite para Inspiração

- Criar wireflow próprio e independente.
- Documentar quais padrões são ideia de produto, não código derivado.
- Confirmar licença antes de qualquer reutilização direta.
