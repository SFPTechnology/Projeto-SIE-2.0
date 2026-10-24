"""Deterministic paginated PDF of the verified engineering record (F10)."""
from __future__ import annotations

from html import escape
from io import BytesIO
from pathlib import Path
import json


def render_engineering_pdf(memorial, schedule, quantities, equipment) -> bytes:
    import reportlab
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak, LongTable, TableStyle
    from reportlab.platypus.tableofcontents import TableOfContents

    font_path = Path(reportlab.__file__).parent / 'fonts' / 'Vera.ttf'
    if 'F10Vera' not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont('F10Vera', str(font_path)))
    styles = getSampleStyleSheet()
    for name in ('Normal', 'Title', 'Heading1', 'Heading2'):
        styles[name].fontName = 'F10Vera'
    styles['Normal'].fontSize = 8
    styles['Normal'].leading = 12
    styles.add(ParagraphStyle(name='CellF10', fontName='F10Vera', fontSize=7, leading=10, wordWrap='CJK'))
    buffer = BytesIO()

    class Document(BaseDocTemplate):
        def afterFlowable(self, flowable):
            if isinstance(flowable, Paragraph) and flowable.style.name == 'Heading1':
                self.notify('TOCEntry', (0, flowable.getPlainText(), self.page))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('F10Vera', 7)
        canvas.setFillColor(colors.HexColor('#475569'))
        canvas.drawString(40, 25, 'SIE 2.0 | estudo não homologado')
        canvas.drawRightString(A4[0] - 40, 25, f'Página {doc.page}')
        canvas.restoreState()

    doc = Document(buffer, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=42, bottomMargin=42,
                   title='Memorial técnico rastreável - SIE 2.0', author='SIE 2.0', invariant=1)
    doc.addPageTemplates(PageTemplate(id='main', frames=[Frame(40, 42, A4[0]-80, A4[1]-84, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=footer))
    story = []
    def p(text, style='Normal'):
        return Paragraph(escape(str(text)), styles[style])
    def heading(text):
        story.extend([Spacer(1, 10), p(text, 'Heading1')])
    def table(headers, rows, widths):
        data = [[p(value, 'CellF10') for value in headers]]
        data += [[p(value, 'CellF10') for value in row] for row in rows]
        t = LongTable(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e2e8f0')),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#94a3b8')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]))
        story.append(t)

    story += [Spacer(1, 70), p('SIE 2.0', 'Title'), Spacer(1, 20), p('Memorial técnico rastreável', 'Title'), Spacer(1, 22),
              p('Quadro de cargas, quantitativos e resultados da execução persistida.'), Spacer(1, 12),
              p('Estudo computacional. Não constitui homologação normativa, profissional ou de concessionária.'), Spacer(1, 20)]
    for key, value in memorial['contract'].items():
        story.append(p(f'{key}: {value}'))
    story += [PageBreak(), p('Sumário', 'Title')]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle(name='TOCF10', fontName='F10Vera', fontSize=10, leading=16)]
    story += [toc, PageBreak()]
    heading('1. Identificação e fontes')
    for calculation in memorial.get('calculations', [memorial]):
        if 'calculation_circuit_id' in calculation:
            story.append(p('Circuito: ' + calculation['calculation_circuit_id']))
        if 'calculation_run_id' in calculation:
            story.append(p('Execução: ' + calculation['calculation_run_id']))
        table(['Campo', 'Referência autoritativa'], [(k, calculation[k]) for k in ('algorithm_version','execution_sha256','input_sha256','result_sha256')], [125,390])
        story.append(Spacer(1, 6))
    heading('2. Entradas persistidas')
    table(['Origem JSON', 'Valor usado pelo motor'], [(r['source_path'], json.dumps(r['value'],ensure_ascii=False)) for r in memorial['input_facts']], [230,285])
    heading('3. Resultados, intermediários e fórmulas')
    story.append(p('Transcrição dos campos retornados pelo motor identificado; não há reconstrução de fórmulas ausentes.'))
    table(['Origem JSON', 'Valor retornado'], [(r['source_path'], json.dumps(r['value'],ensure_ascii=False)) for r in memorial['result_facts']], [230,285])
    heading('4. Quadro de cargas')
    fields = ('circuit_id','panel_id','load_va','phase','breaker_id','conductor_id')
    table(['Circuito','Quadro','Carga VA','Fase','Disjuntor','Condutor'], [[r[k] for k in fields] for r in schedule['rows']], [100,85,50,40,120,120])
    # Same authoritative values as the schedule JSON/CSV/HTML, never recalculate.
    engineering_fields = ('design_current_a', 'voltage_v', 'section_mm2', 'breaker_current_a')
    if any(any(key in row for key in engineering_fields) for row in schedule['rows']):
        story.append(Spacer(1, 8))
        table(['Circuito', 'Corrente A', 'Tensão V', 'Seção mm²', 'Disjuntor A'],
              [[row['circuit_id'], *[row.get(key, 'Não disponível') for key in engineering_fields]] for row in schedule['rows']],
              [195,80,80,80,80])
    heading('5. Quantitativos e proveniência')
    table(['Trecho/circuito', 'Comprimento m / estado', 'Origem'], [(r['segment_id']+' / '+r['circuit_id'],str(r['length_m'])+' / '+r['status'],r['origin']) for r in quantities], [200,130,185])
    heading('6. Equipamentos cadastrados')
    table(['Item', 'Tipo', 'Quantidade', 'Origem'], [(r['item_id'],r['kind'],f"{r['quantity']} {r['unit']}",r['source_path']) for r in equipment], [140,80,60,235])
    heading('7. Limitações e pendências')
    for item in memorial['limitations']:
        story += [p(item), Spacer(1, 6)]
    doc.multiBuild(story)
    return buffer.getvalue()
