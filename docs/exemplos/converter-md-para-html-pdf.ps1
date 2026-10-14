# ============================================================================
# Script de Conversão: Markdown → HTML → PDF
# ============================================================================
#
# Objetivo: Converter arquivo Markdown para HTML com estilo profissional
#           e depois exportar para PDF com suporte a A4
#
# Baseado em: docs/avaliacao-pqa-500/guia-conversao-md-html-pdf.md
# Uso: .\converter-md-para-html-pdf.ps1 -InputFile "tutorial.md" -OutputDir "docs/"
#
# ============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [Parameter(Mandatory=$false)]
    [string]$OutputDir = "./",

    [Parameter(Mandatory=$false)]
    [switch]$GeneratePDF = $false,

    [Parameter(Mandatory=$false)]
    [string]$ChromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
)

# ============================================================================
# Funções
# ============================================================================

function Test-FileEncoding {
    param([string]$FilePath)

    $bytes = [System.IO.File]::ReadAllBytes($FilePath)

    # Testar UTF-8 BOM
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        return "UTF-8-BOM"
    }

    # Testar UTF-8 sem BOM
    try {
        $text = [System.Text.Encoding]::UTF8.GetString($bytes)
        $reencoded = [System.Text.Encoding]::UTF8.GetBytes($text)
        if (@(Compare-Object $bytes $reencoded -SyncWindow 0).Length -eq 0) {
            return "UTF-8"
        }
    } catch {}

    return "Unknown"
}

function Convert-MarkdownToHtml {
    param(
        [string]$MarkdownFile,
        [string]$OutputHtmlFile,
        [string]$Title = "Documento Convertido"
    )

    Write-Host "📖 Lendo arquivo Markdown: $MarkdownFile" -ForegroundColor Cyan

    # Validar encoding
    $encoding = Test-FileEncoding $MarkdownFile
    Write-Host "   Encoding detectado: $encoding" -ForegroundColor Yellow

    # Ler arquivo com UTF-8 explícito
    $markdown = [System.IO.File]::ReadAllText($MarkdownFile, [System.Text.Encoding]::UTF8)

    # Validar acentos
    if ($markdown -match '[áéíóúãõç]') {
        Write-Host "   ✓ Acentuação detectada (português)" -ForegroundColor Green
    }

    # Iniciar HTML
    $html = @"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$Title</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { font-size: 16px; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.6;
      color: #2c3e50;
      background-color: white;
    }
    .container { max-width: 210mm; margin: 0 auto; padding: 40px; }
    h1 { font-size: 2.2em; color: #003366; margin: 40px 0 20px 0; border-bottom: 3px solid #ffc107; }
    h2 { font-size: 1.8em; color: #004499; margin: 35px 0 15px 0; border-bottom: 2px solid #e0e0e0; }
    h3 { font-size: 1.4em; color: #005cc5; margin: 25px 0 15px 0; }
    h4 { font-size: 1.1em; color: #2c3e50; margin: 20px 0 12px 0; }
    p { margin-bottom: 15px; line-height: 1.7; }
    ul, ol { margin-left: 30px; margin-bottom: 15px; }
    li { margin-bottom: 8px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 25px; }
    th { background-color: #004499; color: white; padding: 12px; text-align: left; border: 1px solid #003366; }
    td { padding: 10px 12px; border: 1px solid #d0d0d0; }
    tr:nth-child(even) { background-color: #f5f5f5; }
    code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: "Courier New", monospace; }
    pre { background-color: #f8f8f8; border: 1px solid #ddd; padding: 15px; overflow-x: auto; margin-bottom: 20px; }
    @media print {
      body { background-color: white; }
      @page { size: A4; margin: 20mm; }
    }
  </style>
</head>
<body>
  <div class="container">
"@

    # Converter Markdown para HTML (simplificado)
    $html += Convert-MarkdownContent $markdown

    # Fechar HTML
    $html += @"
  </div>
</body>
</html>
"@

    # Salvar com encoding UTF-8 sem BOM
    $utf8NoBOM = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($OutputHtmlFile, $html, $utf8NoBOM)

    Write-Host "✓ HTML gerado: $OutputHtmlFile" -ForegroundColor Green
}

function Convert-MarkdownContent {
    param([string]$Markdown)

    $html = ""
    $lines = $markdown -split "`n"
    $inCodeBlock = $false
    $inTable = $false

    foreach ($line in $lines) {
        # Blocos de código
        if ($line -match '^\s*```') {
            if ($inCodeBlock) {
                $html += "</pre>`n"
                $inCodeBlock = $false
            } else {
                $html += "<pre><code>`n"
                $inCodeBlock = $true
            }
            continue
        }

        if ($inCodeBlock) {
            $html += [System.Web.HttpUtility]::HtmlEncode($line) + "`n"
            continue
        }

        # Títulos
        if ($line -match '^# (.+)$') {
            $html += "<h1>$($matches[1])</h1>`n"
            continue
        }
        if ($line -match '^## (.+)$') {
            $html += "<h2>$($matches[1])</h2>`n"
            continue
        }
        if ($line -match '^### (.+)$') {
            $html += "<h3>$($matches[1])</h3>`n"
            continue
        }
        if ($line -match '^#### (.+)$') {
            $html += "<h4>$($matches[1])</h4>`n"
            continue
        }

        # Tabelas
        if ($line -match '^\|.*\|$') {
            if (-not $inTable) {
                $html += "<table>`n"
                $inTable = $true
            }

            $cells = $line -split '\|' | Where-Object { $_ -ne "" }
            if ($line -match '---') {
                $html += "<thead>`n<tr>`n"
            }

            $html += "<tr>`n"
            foreach ($cell in $cells) {
                $cell = $cell.Trim()
                if ($line -match '---') {
                    $html += "<th>$cell</th>`n"
                } else {
                    $html += "<td>$cell</td>`n"
                }
            }
            $html += "</tr>`n"
            continue
        } elseif ($inTable -and $line.Trim() -ne "") {
            $html += "</table>`n"
            $inTable = $false
        }

        # Negrito e itálico
        $line = $line -replace '\*\*(.+?)\*\*', '<strong>$1</strong>'
        $line = $line -replace '\*(.+?)\*', '<em>$1</em>'
        $line = $line -replace '`(.+?)`', '<code>$1</code>'

        # Listas
        if ($line -match '^\- (.+)$') {
            $html += "<ul>`n<li>$($matches[1])</li>`n</ul>`n"
            continue
        }

        # Parágrafos
        if ($line.Trim() -ne "") {
            $html += "<p>$line</p>`n"
        }
    }

    return $html
}

function Export-HtmlToPdf {
    param(
        [string]$HtmlFile,
        [string]$PdfFile,
        [string]$ChromePath
    )

    if (-not (Test-Path $ChromePath)) {
        Write-Host "❌ Chrome não encontrado em: $ChromePath" -ForegroundColor Red
        Write-Host "   Use -ChromePath para especificar o caminho correto" -ForegroundColor Yellow
        return $false
    }

    Write-Host "📄 Convertendo para PDF: $PdfFile" -ForegroundColor Cyan

    $HtmlFullPath = (Resolve-Path $HtmlFile).Path
    $PdfFullPath = (Resolve-Path $([System.IO.Path]::GetDirectoryName($PdfFile))).Path + "\" + (Split-Path $PdfFile -Leaf)

    & $ChromePath `
        --headless `
        --disable-gpu `
        --print-to-pdf="$PdfFullPath" `
        --print-to-pdf-no-header `
        --margin-top=20 `
        --margin-bottom=20 `
        --margin-left=20 `
        --margin-right=20 `
        "file:///$HtmlFullPath"

    if (Test-Path $PdfFullPath) {
        Write-Host "✓ PDF gerado com sucesso: $PdfFullPath" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ Erro ao gerar PDF" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# Execução
# ============================================================================

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Conversor: Markdown → HTML → PDF                         ║" -ForegroundColor Cyan
Write-Host "║  Baseado em: Guia de Conversão MD-HTML-PDF               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Validar arquivo de entrada
if (-not (Test-Path $InputFile)) {
    Write-Host "❌ Arquivo não encontrado: $InputFile" -ForegroundColor Red
    exit 1
}

# Extrair nome base
$basename = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)
$htmlFile = Join-Path $OutputDir "$basename.html"
$pdfFile = Join-Path $OutputDir "$basename.pdf"

# Converter para HTML
Convert-MarkdownToHtml -MarkdownFile $InputFile -OutputHtmlFile $htmlFile -Title $basename

# Exportar para PDF (se solicitado)
if ($GeneratePDF) {
    $success = Export-HtmlToPdf -HtmlFile $htmlFile -PdfFile $pdfFile -ChromePath $ChromePath

    if ($success) {
        Write-Host ""
        Write-Host "✅ Conversão concluída com sucesso!" -ForegroundColor Green
        Write-Host "   HTML: $htmlFile" -ForegroundColor Cyan
        Write-Host "   PDF:  $pdfFile" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "⚠️  HTML gerado com sucesso, mas PDF falhou" -ForegroundColor Yellow
        Write-Host "   Você pode gerar o PDF manualmente:" -ForegroundColor Yellow
        Write-Host "   1. Abra o arquivo HTML em um navegador" -ForegroundColor Yellow
        Write-Host "   2. Pressione Ctrl+P (ou Cmd+P no Mac)" -ForegroundColor Yellow
        Write-Host "   3. Selecione 'Salvar como PDF'" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "✅ HTML gerado com sucesso!" -ForegroundColor Green
    Write-Host "   Arquivo: $htmlFile" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Para gerar PDF:" -ForegroundColor Cyan
    Write-Host "  .\converter-md-para-html-pdf.ps1 -InputFile '$InputFile' -GeneratePDF" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Checklist de validação:" -ForegroundColor Cyan
Write-Host "   ☐ Acentuação correta (á, é, í, ó, ú, ã, õ, ç)" -ForegroundColor Gray
Write-Host "   ☐ Tabelas mantiveram a formatação" -ForegroundColor Gray
Write-Host "   ☐ Títulos com hierarquia preservada" -ForegroundColor Gray
Write-Host "   ☐ Código destacado e preservado" -ForegroundColor Gray
Write-Host "   ☐ PDF com margens adequadas para A4" -ForegroundColor Gray
