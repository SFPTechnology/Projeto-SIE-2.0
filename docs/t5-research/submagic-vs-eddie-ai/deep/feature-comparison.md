# Deep Feature Comparison — Submagic vs Eddie AI

Comparação categoria-por-categoria com análise comportamental.

## 1. Workflow paradigm

### Submagic — Linear creator workflow
```
Upload → Transcribe → Auto-edit (captions + B-roll + zoom + music) → Polish → Publish
                                  ↑ tudo automático
```
Timeframe: 2-5 min do upload ao MP4 publicável.
Quem dirige: **AI primeiro, humano refina**.

### Eddie AI — Assistant-augmented pro workflow
```
Upload (folders A-roll + B-roll) → Logging overnight → Chat with transcript → Generate rough cut → Export XML → Edit final no NLE
                                    ↑ AI prepara, humano direciona
```
Timeframe: horas (logging) → minutos (chat refinement) → horas (NLE finishing).
Quem dirige: **Humano, AI assiste**.

**Implicação:** Ferramentas pertencem a ciclos de produção diferentes. SM é "fast & cheap & shippable". ED é "hours saved on tedious pre-edit".

---

## 2. Como cada um trata "Match imagem com fala" (request original do Alan)

### Submagic — Magic AI B-roll
Mecanismo (inferido da documentação):
1. Whisper-class ASR transcreve áudio
2. AI lê transcript completo
3. Para cada N segundos (densidade configurável), seleciona "key moment"
4. Match contra Storyblocks library (proprietary index) ou "My videos" upload via keyword/concept matching
5. Auto-insert no timeline com layout pré-selecionado (cover/split/PIP)

Forças:
- Inserção automática direta no preview
- Layout split-50-50 e split-35-65 nativos (literal "divide a tela")
- Edição manual rápida (highlight transcript → add B-roll)

Fraquezas:
- Match parece keyword-based mais que semantic real
- Para library pessoal, retrieval menos sofisticado que Eddie
- Não tem visual recognition no upload — você precisa nomear bem os arquivos

### Eddie AI — B-Roll Finder + Logging
Mecanismo (documentado):
1. Whisper-class ASR transcreve A-roll
2. Visual recognition (multimodal model) tagga cada clip de B-roll com objetos, cenas, ações
3. Background speech detection extrai contexto adicional do áudio dos B-rolls
4. Embeddings semânticos do transcript (texto) + B-roll (visual)
5. User pede via chat ("office chaos") OU sistema match automático contra fala
6. Eddie sugere placement com timestamps; user aprova; export XML

Forças:
- Semantic search VERDADEIRO (não keyword) — "office chaos" pega planos sem essa tag
- Tagging automático elimina necessidade de organizar manualmente
- Funciona em biblioteca grande (Pro+ aceita 500 B-roll files)
- Background speech catches detail que visual-only perde

Fraquezas:
- Não monta o vídeo final — só sugere placement
- Reviews independentes notam: "B-roll placement wasn't amazing. The choices didn't always match what I would have done."
- Curva de UX maior (chat-prompt requer aprender prompts efetivos)

**Veredicto técnico:** Eddie tem o pipeline mais sofisticado para SEMANTIC matching. Submagic tem o pipeline mais sofisticado para SHIPPING vídeo final.

---

## 3. Output e finalização

| Aspecto | Submagic | Eddie AI |
|---|---|---|
| Tipo de output | MP4/MOV renderizado | XML / FCPXML / EDL |
| Resolução máxima | 4K 60fps (Business) | Whatever o NLE rendera |
| Codecs | H.264, H.265 | Metadata; codec final é do NLE |
| Aspectos | 9:16, 1:1, 16:9, custom | Qualquer (definido no NLE) |
| Cor | Pipeline simplificado | Delegado ao NLE (color grading do Resolve etc) |
| Áudio mix | Pipeline simplificado | Delegado ao NLE |
| Effects/transitions | Curated library | Delegado ao NLE |

---

## 4. Pricing por valor entregue

### Submagic — direct value, low friction
- $24/mês (Pro) entrega: transcrição + B-roll + captions premium + render 4K para social
- ROI claro: se você posta 10 shorts/mês, paga-se em horas economizadas
- Free tier suficiente para testar em 1 dia

### Eddie AI — pro tooling, premium pricing
- $21/mês (Plus) é entry-level mas limitado (5 exports/mês)
- $167/mês (Pro) é onde virtude profissional aparece (multicam, BRAW)
- $333/mês (Pro+) só faz sentido para teams pequenos
- Pulo de 8x entre Plus e Pro é barreira psicológica

**Insight:** SM tem pricing de ferramenta, ED tem pricing de software pro-grade. SM democratiza, ED segmenta.

---

## 5. Where each shines (use cases)

### Submagic shines
- TikTok/Reels/Shorts daily output
- Repurposing podcast → 10 shorts numa tarde
- Brand consistency em alta cadência (Brand Kit)
- Solo creator sem equipe técnica
- Mobile-shot content (upload via QR code)
- Multi-idioma (auto-translate 100+)
- Templates virais prontos

### Eddie AI shines
- Documentário 60-90 min com horas de bruto
- Podcast multi-cam (3-6 câmeras) longform
- Corporate video com brand exigente
- Filmmakers que terminam no Premiere/Resolve/FCP
- Quem tem biblioteca pessoal grande (50h+ de B-roll)
- Workflows overnight (Night Shift)
- Editores assistentes que querem aliviar logging

---

## 6. Anti-patterns (quando NÃO usar)

### Não use Submagic para:
- Documentário longform (não suporta multicam, não exporta XML)
- Conteúdo cinematográfico premium (color science fica no básico)
- Workflow que precisa de Avid/AAF
- Quando você precisa de controle granular do timeline

### Não use Eddie AI para:
- Quem só quer postar shorts hoje à noite (overhead de aprender)
- Workflow que termina no celular (não há mobile)
- Solo creator com orçamento <$30/mês (pricing real começa em $167)
- Quem não tem NLE (Eddie sem Premiere/Resolve/FCP é metade do produto)

---

## 7. Maturity & momentum

### Submagic
- Categoria saturada (Submagic, Captions, Opus, Vizard, Kapwing competem ferozmente)
- 2026: AI Avatar generator, Eye Contact AI, Magic Clips → ainda inovando
- Aposta em consolidação: "all-in-one short-form platform"

### Eddie AI
- Categoria emergente (poucos competidores diretos — Adobe Productions Auto-edit, Twelve Labs, FastPix são adjacentes)
- 2026: Multi-language, smarter B-roll detection → diferencial técnico
- Aposta em depth: "AI assistant editor for pros"

**Trajetória:** SM compete em volume e UX. ED compete em profissionalismo e accuracy.
