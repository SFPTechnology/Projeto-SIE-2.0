import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const rootDir = resolve(scriptDir, "..");
const sourcePath = resolve(rootDir, "docs", "competitor-analysis.md");
const outputPath = resolve(rootDir, "docs", "competitor-analysis-interativo.html");

const markdown = readFileSync(sourcePath, "utf8");
const sourceJson = JSON.stringify(markdown).replaceAll("<", "\\u003c");
const sha256 = createHash("sha256").update(markdown).digest("hex");
const lineCount = markdown.split(/\r?\n/).length;
const wordCount = markdown.trim().split(/\s+/).filter(Boolean).length;
const sectionCount = (markdown.match(/^##\s+/gm) ?? []).length;

const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="Consulta interativa da análise competitiva das seções unifilares do SIE.">
  <title>Análise Competitiva | SIE</title>
  <style>
    :root {
      color-scheme: light;
      --reader-scale: 1;
      --font-ui: Inter, "Segoe UI", Arial, sans-serif;
      --font-doc: Arial, Helvetica, sans-serif;
      --font-code: "Cascadia Code", "IBM Plex Mono", Consolas, monospace;
      --bg: #edf2f4;
      --surface: #ffffff;
      --surface-subtle: #f5f7f8;
      --surface-raised: #ffffff;
      --text: #172023;
      --text-muted: #59676c;
      --border: #cdd7da;
      --border-strong: #9cadaf;
      --accent: #006b5f;
      --accent-strong: #004f47;
      --accent-soft: #d9f0eb;
      --signal: #d7a500;
      --signal-soft: #fff4c2;
      --danger: #b4232d;
      --danger-soft: #fde7e9;
      --info: #1d5f91;
      --info-soft: #e3f0fa;
      --focus: #005fcc;
      --code-bg: #11191b;
      --code-text: #e7f3f1;
      --shadow: 0 12px 34px rgba(29, 45, 48, 0.12);
      --header-h: 68px;
      --sidebar-w: 304px;
      --content-w: 900px;
      --radius: 6px;
    }

    [data-theme="dark"] {
      color-scheme: dark;
      --bg: #151a1a;
      --surface: #202626;
      --surface-subtle: #282f2e;
      --surface-raised: #242b2a;
      --text: #f2f6f5;
      --text-muted: #b5c0bd;
      --border: #465250;
      --border-strong: #687875;
      --accent: #70d8c2;
      --accent-strong: #9ce6d6;
      --accent-soft: #173c35;
      --signal: #f2c94c;
      --signal-soft: #493d12;
      --danger: #ff8389;
      --danger-soft: #4c2427;
      --info: #78b9e6;
      --info-soft: #1f3c50;
      --focus: #9dccff;
      --code-bg: #0c1112;
      --code-text: #e7f3f1;
      --shadow: 0 14px 38px rgba(0, 0, 0, 0.28);
    }

    * {
      box-sizing: border-box;
    }

    html {
      scroll-behavior: smooth;
      scroll-padding-top: calc(var(--header-h) + 24px);
    }

    body {
      margin: 0;
      min-width: 320px;
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-ui);
      line-height: 1.55;
      letter-spacing: 0;
    }

    body.is-locked {
      overflow: hidden;
    }

    button,
    input {
      font: inherit;
      letter-spacing: 0;
    }

    button {
      color: inherit;
    }

    a {
      color: var(--accent-strong);
      text-underline-offset: 0.18em;
      text-decoration-thickness: 1px;
    }

    [data-theme="dark"] a {
      color: var(--accent);
    }

    :focus-visible {
      outline: 3px solid var(--focus);
      outline-offset: 3px;
    }

    .skip-link {
      position: fixed;
      top: 8px;
      left: 8px;
      z-index: 1000;
      padding: 10px 14px;
      background: var(--surface);
      color: var(--text);
      border: 1px solid var(--focus);
      transform: translateY(-160%);
    }

    .skip-link:focus {
      transform: translateY(0);
    }

    .reading-progress {
      position: fixed;
      inset: 0 auto auto 0;
      z-index: 120;
      width: 0;
      height: 3px;
      background: var(--accent);
      transition: width 80ms linear;
    }

    .app-header {
      position: fixed;
      inset: 0 0 auto 0;
      z-index: 100;
      min-height: var(--header-h);
      display: grid;
      grid-template-columns: minmax(260px, 1fr) auto auto;
      align-items: center;
      gap: 18px;
      padding: 10px 18px;
      border-bottom: 1px solid var(--border);
      background: color-mix(in srgb, var(--surface) 94%, transparent);
      backdrop-filter: blur(14px);
    }

    .brand {
      min-width: 0;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-mark {
      width: 40px;
      height: 40px;
      flex: 0 0 40px;
      display: grid;
      place-items: center;
      border: 1px solid var(--accent);
      background: var(--accent-soft);
      color: var(--accent-strong);
      font-size: 13px;
      font-weight: 800;
    }

    .brand-copy {
      min-width: 0;
    }

    .brand-kicker {
      margin: 0;
      color: var(--accent);
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
    }

    .brand-title {
      margin: 2px 0 0;
      overflow: hidden;
      color: var(--text);
      font-size: 15px;
      font-weight: 700;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .mode-switcher {
      display: inline-grid;
      grid-template-columns: repeat(3, 1fr);
      padding: 3px;
      border: 1px solid var(--border);
      background: var(--surface-subtle);
    }

    .mode-button {
      min-height: 36px;
      padding: 6px 12px;
      border: 0;
      border-radius: 3px;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 12px;
      font-weight: 700;
    }

    .mode-button[aria-pressed="true"] {
      background: var(--surface);
      color: var(--accent-strong);
      box-shadow: 0 1px 4px rgba(24, 38, 40, 0.12);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .icon-button {
      width: 38px;
      height: 38px;
      display: inline-grid;
      place-items: center;
      border: 1px solid transparent;
      border-radius: 4px;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 18px;
    }

    .icon-button:hover {
      border-color: var(--border);
      background: var(--surface-subtle);
      color: var(--text);
    }

    .menu-button {
      display: none;
    }

    .app-shell {
      min-height: 100vh;
      padding-top: var(--header-h);
    }

    .sidebar {
      position: fixed;
      inset: var(--header-h) auto 0 0;
      z-index: 80;
      width: var(--sidebar-w);
      overflow: hidden;
      border-right: 1px solid var(--border);
      background: var(--surface);
    }

    .sidebar-inner {
      height: 100%;
      display: grid;
      grid-template-rows: auto auto 1fr auto;
      gap: 14px;
      padding: 18px 14px 14px;
    }

    .document-facts {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1px;
      border: 1px solid var(--border);
      background: var(--border);
    }

    .fact {
      min-width: 0;
      padding: 10px 6px;
      background: var(--surface-subtle);
      text-align: center;
    }

    .fact strong {
      display: block;
      color: var(--text);
      font-size: 15px;
    }

    .fact span {
      display: block;
      margin-top: 2px;
      color: var(--text-muted);
      font-size: 9px;
      text-transform: uppercase;
    }

    .search-wrap {
      position: relative;
    }

    .search-wrap label {
      display: block;
      margin-bottom: 6px;
      color: var(--text-muted);
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
    }

    .search-input {
      width: 100%;
      height: 40px;
      padding: 0 38px 0 12px;
      border: 1px solid var(--border-strong);
      border-radius: 4px;
      background: var(--surface);
      color: var(--text);
    }

    .search-count {
      position: absolute;
      right: 10px;
      bottom: 11px;
      color: var(--text-muted);
      font-size: 10px;
    }

    .toc {
      min-height: 0;
      overflow: auto;
      padding-right: 4px;
      scrollbar-width: thin;
    }

    .toc-heading {
      margin: 0 0 8px 6px;
      color: var(--text-muted);
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
    }

    .toc-list {
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .toc-link {
      display: block;
      margin: 1px 0;
      padding: 7px 9px;
      border-left: 3px solid transparent;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 12px;
      line-height: 1.3;
    }

    .toc-link:hover {
      background: var(--surface-subtle);
      color: var(--text);
    }

    .toc-link.is-active {
      border-left-color: var(--accent);
      background: var(--accent-soft);
      color: var(--accent-strong);
      font-weight: 700;
    }

    .sidebar-footer {
      padding: 10px;
      border-top: 1px solid var(--border);
      color: var(--text-muted);
      font-family: var(--font-code);
      font-size: 9px;
      line-height: 1.5;
      word-break: break-all;
    }

    .main {
      min-width: 0;
      margin-left: var(--sidebar-w);
      padding: 32px clamp(20px, 4vw, 64px) 80px;
    }

    .reader-toolbar {
      width: min(100%, var(--content-w));
      min-height: 48px;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      margin: 0 auto 14px;
      padding: 6px 8px 6px 14px;
      border: 1px solid var(--border);
      background: var(--surface);
    }

    .reader-status {
      min-width: 0;
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--text-muted);
      font-size: 11px;
    }

    .integrity-dot {
      width: 8px;
      height: 8px;
      flex: 0 0 8px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-soft);
    }

    .reader-actions {
      display: flex;
      align-items: center;
      gap: 2px;
    }

    .document-paper {
      width: min(100%, var(--content-w));
      min-height: 80vh;
      margin: 0 auto;
      padding: clamp(32px, 6vw, 72px);
      border: 1px solid var(--border);
      background: var(--surface-raised);
      box-shadow: var(--shadow);
    }

    .rendered-view {
      min-width: 0;
      max-width: 100%;
      font-family: var(--font-doc);
      font-size: calc(16px * var(--reader-scale));
      line-height: 1.72;
      overflow-wrap: break-word;
    }

    .rendered-view > h1 {
      max-width: 760px;
      margin: 0 0 26px;
      color: var(--text);
      font-size: clamp(30px, 5vw, 54px);
      line-height: 1.04;
    }

    .rendered-view h2,
    .rendered-view h3,
    .rendered-view h4,
    .rendered-view h5,
    .rendered-view h6 {
      position: relative;
      color: var(--text);
      line-height: 1.2;
    }

    .rendered-view h2 {
      margin: 64px 0 22px;
      padding: 0 0 12px;
      border-bottom: 2px solid var(--accent);
      font-size: calc(28px * var(--reader-scale));
    }

    .rendered-view h2::before {
      content: "";
      position: absolute;
      left: 0;
      bottom: -2px;
      width: 72px;
      height: 5px;
      background: var(--signal);
    }

    .rendered-view h3 {
      margin: 40px 0 14px;
      font-size: calc(21px * var(--reader-scale));
    }

    .rendered-view h4 {
      margin: 28px 0 10px;
      color: var(--accent-strong);
      font-size: calc(17px * var(--reader-scale));
    }

    .rendered-view p {
      margin: 0 0 1em;
    }

    .rendered-view ul,
    .rendered-view ol {
      margin: 0.5em 0 1.25em;
      padding-left: 1.55em;
    }

    .rendered-view li {
      margin: 0.32em 0;
      padding-left: 0.18em;
    }

    .rendered-view li::marker {
      color: var(--accent);
      font-weight: 700;
    }

    .rendered-view blockquote {
      margin: 22px 0 30px;
      padding: 18px 20px;
      border-left: 5px solid var(--accent);
      background: var(--accent-soft);
      color: var(--text);
    }

    .rendered-view blockquote p:last-child {
      margin-bottom: 0;
    }

    .rendered-view hr {
      margin: 52px 0;
      border: 0;
      border-top: 1px solid var(--border-strong);
    }

    .rendered-view strong {
      color: var(--text);
    }

    .rendered-view code:not(pre code) {
      padding: 0.12em 0.34em;
      border: 1px solid var(--border);
      border-radius: 3px;
      background: var(--surface-subtle);
      color: var(--danger);
      font-family: var(--font-code);
      font-size: 0.88em;
    }

    .code-block {
      position: relative;
      margin: 24px 0 30px;
      border: 1px solid #344244;
      border-radius: var(--radius);
      background: var(--code-bg);
      color: var(--code-text);
      overflow: hidden;
    }

    .code-label {
      min-height: 34px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 5px 8px 5px 14px;
      border-bottom: 1px solid #344244;
      color: #a8bab7;
      font-family: var(--font-ui);
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
    }

    .code-block pre {
      margin: 0;
      padding: 20px;
      overflow: auto;
      font-family: var(--font-code);
      font-size: 13px;
      line-height: 1.55;
      white-space: pre;
    }

    .copy-code {
      width: 32px;
      height: 28px;
      border: 1px solid #4d5d5f;
      border-radius: 3px;
      background: transparent;
      color: #d5e0de;
      cursor: pointer;
    }

    .table-scroll {
      margin: 24px 0 32px;
      overflow-x: auto;
      border-top: 2px solid var(--text);
      border-bottom: 1px solid var(--text);
    }

    .rendered-view table {
      width: 100%;
      border-collapse: collapse;
      font-size: calc(13px * var(--reader-scale));
      line-height: 1.4;
    }

    .rendered-view th,
    .rendered-view td {
      min-width: 130px;
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
    }

    .rendered-view th {
      background: var(--surface-subtle);
      color: var(--text);
      font-size: 11px;
      text-transform: uppercase;
    }

    .rendered-view tbody tr:nth-child(even) {
      background: color-mix(in srgb, var(--surface-subtle) 62%, transparent);
    }

    .rendered-view tbody tr:hover {
      background: var(--accent-soft);
    }

    .diagram {
      margin: 28px 0 34px;
      border: 1px solid var(--border);
      background: var(--surface-subtle);
    }

    .diagram figcaption {
      padding: 10px 14px;
      border-bottom: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
    }

    .diagram-canvas {
      min-height: 180px;
      overflow: auto;
      padding: 14px;
    }

    .diagram svg {
      min-width: 680px;
      display: block;
      margin: 0 auto;
    }

    .diagram details {
      border-top: 1px solid var(--border);
    }

    .diagram summary {
      padding: 10px 14px;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 11px;
    }

    .diagram pre {
      margin: 0;
      padding: 14px;
      overflow: auto;
      background: var(--code-bg);
      color: var(--code-text);
      font-family: var(--font-code);
      font-size: 12px;
    }

    mark {
      padding: 0.05em 0.1em;
      background: var(--signal-soft);
      color: var(--text);
      box-shadow: 0 0 0 1px var(--signal);
    }

    mark.is-current {
      background: var(--signal);
      color: #17120a;
    }

    .source-view {
      display: none;
    }

    .source-view pre {
      margin: 0;
      color: var(--text);
      font-family: var(--font-code);
      font-size: calc(13px * var(--reader-scale));
      line-height: 1.6;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }

    [data-mode="source"] .rendered-view {
      display: none;
    }

    [data-mode="source"] .source-view {
      display: block;
    }

    [data-mode="abnt"] {
      --content-w: 210mm;
      --reader-scale: 1;
    }

    [data-mode="abnt"] .main {
      background: #cfd5d7;
    }

    [data-mode="abnt"] .document-paper {
      width: 210mm;
      max-width: 100%;
      min-height: 297mm;
      padding: 30mm 20mm 20mm 30mm;
      border: 0;
      background: #ffffff;
      color: #000000;
      box-shadow: 0 10px 36px rgba(18, 27, 30, 0.2);
    }

    [data-mode="abnt"] .rendered-view {
      color: #000000;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 12pt;
      line-height: 1.5;
      text-align: justify;
    }

    [data-mode="abnt"] .rendered-view > h1 {
      margin: 0 0 30mm;
      color: #000000;
      font-size: 14pt;
      line-height: 1.5;
      text-align: center;
      text-transform: uppercase;
    }

    [data-mode="abnt"] .rendered-view h2 {
      margin: 0 0 1.5em;
      padding: 0;
      border: 0;
      color: #000000;
      font-size: 12pt;
      text-align: left;
      text-transform: uppercase;
    }

    [data-mode="abnt"] .rendered-view h2::before {
      display: none;
    }

    [data-mode="abnt"] .rendered-view h3,
    [data-mode="abnt"] .rendered-view h4 {
      color: #000000;
      font-size: 12pt;
      text-align: left;
    }

    [data-mode="abnt"] .rendered-view p {
      margin: 0;
      text-indent: 1.25cm;
    }

    [data-mode="abnt"] .rendered-view h1 + blockquote,
    [data-mode="abnt"] .rendered-view h2 + p,
    [data-mode="abnt"] .rendered-view h3 + p,
    [data-mode="abnt"] .rendered-view h4 + p,
    [data-mode="abnt"] .rendered-view blockquote p,
    [data-mode="abnt"] .rendered-view li p {
      text-indent: 0;
    }

    [data-mode="abnt"] .rendered-view blockquote {
      margin: 0 0 1.5em;
      padding: 0;
      border: 0;
      background: transparent;
      color: #000000;
      font-size: 10pt;
      line-height: 1;
      text-align: left;
    }

    [data-mode="abnt"] .rendered-view a,
    [data-mode="abnt"] .rendered-view code:not(pre code) {
      color: #000000;
    }

    [data-mode="abnt"] .rendered-view table {
      color: #000000;
      font-size: 10pt;
      line-height: 1;
    }

    [data-mode="abnt"] .rendered-view th,
    [data-mode="abnt"] .rendered-view td {
      background: #ffffff;
      color: #000000;
      border-color: #000000;
    }

    [data-mode="abnt"] .rendered-view hr {
      border-color: #000000;
    }

    [data-mode="abnt"] .diagram {
      background: #ffffff;
      border-color: #000000;
    }

    .sidebar-backdrop {
      display: none;
    }

    .toast {
      position: fixed;
      right: 18px;
      bottom: 18px;
      z-index: 200;
      max-width: min(360px, calc(100vw - 36px));
      padding: 12px 14px;
      border: 1px solid var(--border-strong);
      border-left: 4px solid var(--accent);
      background: var(--surface);
      color: var(--text);
      box-shadow: var(--shadow);
      font-size: 12px;
      opacity: 0;
      transform: translateY(12px);
      pointer-events: none;
      transition: opacity 160ms ease, transform 160ms ease;
    }

    .toast.is-visible {
      opacity: 1;
      transform: translateY(0);
    }

    @media (max-width: 1040px) {
      .app-header {
        grid-template-columns: minmax(200px, 1fr) auto;
      }

      .mode-switcher {
        order: 3;
        grid-column: 1 / -1;
        width: 100%;
      }

      :root {
        --header-h: 116px;
      }
    }

    @media (max-width: 820px) {
      :root {
        --header-h: 116px;
      }

      .menu-button {
        display: inline-grid;
      }

      .brand-kicker {
        display: none;
      }

      .sidebar {
        z-index: 150;
        width: min(88vw, 340px);
        transform: translateX(-105%);
        transition: transform 180ms ease;
      }

      .sidebar.is-open {
        transform: translateX(0);
      }

      .sidebar-backdrop {
        position: fixed;
        inset: var(--header-h) 0 0 0;
        z-index: 140;
        display: block;
        border: 0;
        background: rgba(10, 16, 17, 0.58);
        opacity: 0;
        pointer-events: none;
        transition: opacity 180ms ease;
      }

      .sidebar-backdrop.is-open {
        opacity: 1;
        pointer-events: auto;
      }

      .main {
        margin-left: 0;
        padding: 20px 12px 64px;
      }

      .document-paper {
        padding: 28px 20px;
      }

      .reader-status span:last-child {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      [data-mode="abnt"] .document-paper {
        width: 100%;
        min-height: auto;
        padding: 30px 22px;
      }
    }

    @media (max-width: 520px) {
      html,
      body {
        max-width: 100%;
        overflow-x: hidden;
      }

      .app-header {
        width: 100vw;
        max-width: 100%;
        grid-template-columns: minmax(0, 1fr) auto;
        gap: 8px;
        padding-inline: 10px;
      }

      .brand {
        gap: 8px;
      }

      .brand-title {
        font-size: 12px;
      }

      .mode-switcher,
      .mode-button {
        min-width: 0;
        max-width: 100%;
      }

      .header-actions .font-control {
        display: none;
      }

      .reader-toolbar {
        align-items: flex-start;
        flex-direction: column;
      }

      .reader-actions {
        width: 100%;
        justify-content: flex-end;
      }

      .rendered-view > h1 {
        font-size: 30px;
      }

      .rendered-view h2 {
        font-size: 23px;
      }

      .table-scroll,
      .diagram,
      .diagram-canvas {
        max-width: 100%;
      }
    }

    @media print {
      @page {
        size: A4 portrait;
        margin: 30mm 20mm 20mm 30mm;
      }

      :root {
        color-scheme: light;
      }

      body,
      [data-mode="abnt"] .main {
        background: #ffffff !important;
      }

      .app-header,
      .sidebar,
      .sidebar-backdrop,
      .reader-toolbar,
      .reading-progress,
      .toast,
      .skip-link {
        display: none !important;
      }

      .app-shell {
        padding: 0;
      }

      .main {
        margin: 0;
        padding: 0;
      }

      .document-paper,
      [data-mode="abnt"] .document-paper {
        width: auto;
        min-height: 0;
        margin: 0;
        padding: 0;
        border: 0;
        box-shadow: none !important;
      }

      .rendered-view {
        display: block !important;
        color: #000000 !important;
        font-family: Arial, Helvetica, sans-serif !important;
        font-size: 12pt !important;
        line-height: 1.5 !important;
        text-align: justify;
      }

      .source-view {
        display: none !important;
      }

      .doc-section {
        break-inside: auto;
      }

      .doc-section + .doc-section > h2 {
        break-before: page;
      }

      h2,
      h3,
      h4,
      table,
      figure,
      pre,
      blockquote {
        break-inside: avoid;
      }

      a {
        color: #000000 !important;
        text-decoration: none;
      }

      a[href^="http"]::after {
        content: " (" attr(href) ")";
        font-size: 9pt;
        overflow-wrap: anywhere;
      }

      .copy-code,
      details {
        display: none !important;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
      }
    }
  </style>
</head>
<body data-theme="light" data-mode="reading">
  <a class="skip-link" href="#conteudo">Ir para o conteúdo</a>
  <div class="reading-progress" id="reading-progress" aria-hidden="true"></div>

  <header class="app-header">
    <div class="brand">
      <button class="icon-button menu-button" id="menu-button" type="button" aria-label="Abrir sumário" title="Abrir sumário">☰</button>
      <div class="brand-mark" aria-hidden="true">SIE</div>
      <div class="brand-copy">
        <p class="brand-kicker">Inteligência documental</p>
        <p class="brand-title">Análise competitiva das seções unifilares</p>
      </div>
    </div>

    <div class="mode-switcher" role="group" aria-label="Modo de visualização">
      <button class="mode-button" type="button" data-mode-target="reading" aria-pressed="true">Leitura</button>
      <button class="mode-button" type="button" data-mode-target="abnt" aria-pressed="false" title="Visualização A4 baseada na ABNT NBR 14724:2024">ABNT</button>
      <button class="mode-button" type="button" data-mode-target="source" aria-pressed="false">Fonte</button>
    </div>

    <div class="header-actions">
      <button class="icon-button font-control" id="font-decrease" type="button" aria-label="Diminuir texto" title="Diminuir texto">A−</button>
      <button class="icon-button font-control" id="font-increase" type="button" aria-label="Aumentar texto" title="Aumentar texto">A+</button>
      <button class="icon-button" id="theme-toggle" type="button" aria-label="Alternar tema" title="Alternar tema">◐</button>
      <button class="icon-button" id="print-button" type="button" aria-label="Imprimir em formato ABNT" title="Imprimir em formato ABNT">⎙</button>
    </div>
  </header>

  <div class="app-shell">
    <aside class="sidebar" id="sidebar" aria-label="Navegação do documento">
      <div class="sidebar-inner">
        <div class="document-facts" aria-label="Estatísticas do documento">
          <div class="fact"><strong>${sectionCount}</strong><span>seções</span></div>
          <div class="fact"><strong>${lineCount.toLocaleString("pt-BR")}</strong><span>linhas</span></div>
          <div class="fact"><strong>${wordCount.toLocaleString("pt-BR")}</strong><span>palavras</span></div>
        </div>

        <div class="search-wrap">
          <label for="document-search">Pesquisar no relatório</label>
          <input class="search-input" id="document-search" type="search" autocomplete="off" placeholder="Termo, módulo, concorrente...">
          <span class="search-count" id="search-count" aria-live="polite">0</span>
        </div>

        <nav class="toc" aria-label="Sumário">
          <p class="toc-heading">Sumário</p>
          <ol class="toc-list" id="toc-list"></ol>
        </nav>

        <div class="sidebar-footer">
          <strong>Fonte íntegra</strong><br>
          SHA-256 ${sha256}<br>
          ${lineCount.toLocaleString("pt-BR")} linhas incorporadas
        </div>
      </div>
    </aside>

    <button class="sidebar-backdrop" id="sidebar-backdrop" type="button" aria-label="Fechar sumário"></button>

    <main class="main" id="conteudo">
      <div class="reader-toolbar" aria-label="Ferramentas do documento">
        <div class="reader-status">
          <span class="integrity-dot" aria-hidden="true"></span>
          <span>Conteúdo integral verificado · ${sha256.slice(0, 12)}</span>
        </div>
        <div class="reader-actions">
          <button class="icon-button" id="copy-source" type="button" aria-label="Copiar Markdown original" title="Copiar Markdown original">⧉</button>
          <button class="icon-button" id="download-source" type="button" aria-label="Baixar Markdown original" title="Baixar Markdown original">⇩</button>
          <button class="icon-button" id="copy-link" type="button" aria-label="Copiar link da seção atual" title="Copiar link da seção atual">#</button>
        </div>
      </div>

      <article class="document-paper" aria-label="Análise competitiva">
        <div class="rendered-view" id="rendered-view"></div>
        <div class="source-view" id="source-view" aria-label="Fonte Markdown original">
          <pre id="source-pre"></pre>
        </div>
      </article>
    </main>
  </div>

  <div class="toast" id="toast" role="status" aria-live="polite"></div>
  <script id="markdown-source" type="application/json">${sourceJson}</script>
  <script>
    (function () {
      "use strict";

      var markdown = JSON.parse(document.getElementById("markdown-source").textContent);
      var renderedView = document.getElementById("rendered-view");
      var sourcePre = document.getElementById("source-pre");
      var tocList = document.getElementById("toc-list");
      var sidebar = document.getElementById("sidebar");
      var sidebarBackdrop = document.getElementById("sidebar-backdrop");
      var searchInput = document.getElementById("document-search");
      var searchCount = document.getElementById("search-count");
      var toast = document.getElementById("toast");
      var currentSectionId = "";
      var searchMatches = [];
      var currentMatch = -1;
      var toastTimer = 0;
      var slugCounts = new Map();

      function escapeHtml(value) {
        return String(value)
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#039;");
      }

      function slugify(value) {
        var base = value
          .normalize("NFD")
          .replace(/[\\u0300-\\u036f]/g, "")
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, "-")
          .replace(/^-|-$/g, "") || "secao";
        var count = slugCounts.get(base) || 0;
        slugCounts.set(base, count + 1);
        return count === 0 ? base : base + "-" + (count + 1);
      }

      function renderInline(value) {
        var codeTokens = [];
        var text = String(value).replace(/\\x60([^\\x60]+)\\x60/g, function (_, code) {
          var token = "@@CODE" + codeTokens.length + "@@";
          codeTokens.push("<code>" + escapeHtml(code) + "</code>");
          return token;
        });
        text = escapeHtml(text);
        text = text.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, function (_, label, href) {
          var safeHref = href.replace(/&amp;/g, "&");
          var external = /^https?:\\/\\//i.test(safeHref);
          return '<a href="' + escapeHtml(safeHref) + '"' +
            (external ? ' target="_blank" rel="noopener noreferrer"' : "") +
            ">" + label + "</a>";
        });
        text = text.replace(/\\*\\*([^*]+)\\*\\*/g, "<strong>$1</strong>");
        text = text.replace(/(^|[^*])\\*([^*]+)\\*/g, "$1<em>$2</em>");
        codeTokens.forEach(function (token, index) {
          text = text.replace("@@CODE" + index + "@@", token);
        });
        return text;
      }

      function isTableSeparator(line) {
        return /^\\s*\\|?\\s*:?-{3,}:?\\s*(\\|\\s*:?-{3,}:?\\s*)+\\|?\\s*$/.test(line);
      }

      function splitTableRow(line) {
        return line.trim().replace(/^\\|/, "").replace(/\\|$/, "").split("|").map(function (cell) {
          return cell.trim();
        });
      }

      function isListLine(line) {
        return /^\\s*[-*+]\\s+/.test(line) || /^\\s*\\d+\\.\\s+/.test(line);
      }

      function isSpecial(lines, index) {
        var line = lines[index] || "";
        var next = lines[index + 1] || "";
        return /^#{1,6}\\s+/.test(line) ||
          /^\\s*\x60{3}/.test(line) ||
          /^\\s*>/.test(line) ||
          /^\\s*---+\\s*$/.test(line) ||
          isListLine(line) ||
          (/^\\s*\\|/.test(line) && isTableSeparator(next));
      }

      function renderMarkdown(source) {
        slugCounts.clear();
        var lines = source.replace(/\\r\\n/g, "\\n").split("\\n");
        var out = [];
        var i = 0;
        var sectionOpen = false;

        while (i < lines.length) {
          var line = lines[i];

          if (!line.trim()) {
            i += 1;
            continue;
          }

          var fence = line.match(/^\\s*\x60{3}\\s*([^\\s]*)\\s*$/);
          if (fence) {
            var language = fence[1] || "texto";
            var codeLines = [];
            i += 1;
            while (i < lines.length && !/^\\s*\x60{3}\\s*$/.test(lines[i])) {
              codeLines.push(lines[i]);
              i += 1;
            }
            i += 1;
            var code = codeLines.join("\\n");
            if (language.toLowerCase() === "mermaid") {
              out.push(
                '<figure class="diagram" data-graph="' + encodeURIComponent(code) + '">' +
                '<figcaption>Diagrama técnico</figcaption>' +
                '<div class="diagram-canvas"></div>' +
                '<details><summary>Ver definição textual</summary><pre>' +
                escapeHtml(code) +
                "</pre></details></figure>"
              );
            } else {
              out.push(
                '<div class="code-block"><div class="code-label"><span>' +
                escapeHtml(language) +
                '</span><button class="copy-code" type="button" aria-label="Copiar bloco de código" title="Copiar bloco">⧉</button></div><pre><code>' +
                escapeHtml(code) +
                "</code></pre></div>"
              );
            }
            continue;
          }

          var heading = line.match(/^(#{1,6})\\s+(.+)$/);
          if (heading) {
            var level = heading[1].length;
            var label = heading[2].trim();
            var id = slugify(label);
            if (level === 2) {
              if (sectionOpen) out.push("</section>");
              out.push('<section class="doc-section" data-section-id="' + id + '">');
              sectionOpen = true;
            }
            out.push("<h" + level + ' id="' + id + '">' + renderInline(label) + "</h" + level + ">");
            i += 1;
            continue;
          }

          if (/^\\s*---+\\s*$/.test(line)) {
            out.push("<hr>");
            i += 1;
            continue;
          }

          if (/^\\s*>/.test(line)) {
            var quote = [];
            while (i < lines.length && /^\\s*>/.test(lines[i])) {
              quote.push(lines[i].replace(/^\\s*>\\s?/, ""));
              i += 1;
            }
            out.push("<blockquote><p>" + quote.map(renderInline).join("<br>") + "</p></blockquote>");
            continue;
          }

          if (/^\\s*\\|/.test(line) && isTableSeparator(lines[i + 1] || "")) {
            var headers = splitTableRow(line);
            i += 2;
            var rows = [];
            while (i < lines.length && /^\\s*\\|/.test(lines[i])) {
              rows.push(splitTableRow(lines[i]));
              i += 1;
            }
            var table = '<div class="table-scroll" tabindex="0"><table><thead><tr>';
            headers.forEach(function (cell) {
              table += "<th scope=\\"col\\">" + renderInline(cell) + "</th>";
            });
            table += "</tr></thead><tbody>";
            rows.forEach(function (row) {
              table += "<tr>";
              headers.forEach(function (_, index) {
                table += "<td>" + renderInline(row[index] || "") + "</td>";
              });
              table += "</tr>";
            });
            table += "</tbody></table></div>";
            out.push(table);
            continue;
          }

          if (isListLine(line)) {
            var ordered = /^\\s*\\d+\\.\\s+/.test(line);
            var tag = ordered ? "ol" : "ul";
            var items = [];
            while (i < lines.length) {
              var itemMatch = ordered
                ? lines[i].match(/^\\s*\\d+\\.\\s+(.+)$/)
                : lines[i].match(/^\\s*[-*+]\\s+(.+)$/);
              if (!itemMatch) break;
              var item = itemMatch[1];
              i += 1;
              while (
                i < lines.length &&
                /^\\s{2,}\\S/.test(lines[i]) &&
                !isListLine(lines[i]) &&
                !/^\\s*\x60{3}/.test(lines[i])
              ) {
                item += " " + lines[i].trim();
                i += 1;
              }
              items.push(item);
              while (i < lines.length && !lines[i].trim()) {
                var lookAhead = lines[i + 1] || "";
                if ((ordered && /^\\s*\\d+\\.\\s+/.test(lookAhead)) ||
                    (!ordered && /^\\s*[-*+]\\s+/.test(lookAhead))) {
                  i += 1;
                } else {
                  break;
                }
              }
            }
            out.push("<" + tag + ">" + items.map(function (item) {
              return "<li>" + renderInline(item) + "</li>";
            }).join("") + "</" + tag + ">");
            continue;
          }

          var paragraph = [line.trim()];
          i += 1;
          while (i < lines.length && lines[i].trim() && !isSpecial(lines, i)) {
            paragraph.push(lines[i].trim());
            i += 1;
          }
          out.push("<p>" + renderInline(paragraph.join(" ")) + "</p>");
        }

        if (sectionOpen) out.push("</section>");
        return out.join("\\n");
      }

      function parseGraph(source) {
        var lines = source.split("\\n").map(function (line) { return line.trim(); }).filter(Boolean);
        var direction = /\\bLR\\b/.test(lines[0] || "") ? "LR" : "TD";
        var nodes = new Map();
        var edges = [];
        lines.slice(1).forEach(function (line) {
          var match = line.match(/^(\\w+)(?:\\[([^\\]]+)\\])?\\s*-->\\s*(\\w+)(?:\\[([^\\]]+)\\])?$/);
          if (!match) return;
          var from = match[1];
          var to = match[3];
          if (match[2]) nodes.set(from, match[2]);
          if (match[4]) nodes.set(to, match[4]);
          if (!nodes.has(from)) nodes.set(from, from);
          if (!nodes.has(to)) nodes.set(to, to);
          edges.push({ from: from, to: to });
        });
        return { direction: direction, nodes: nodes, edges: edges };
      }

      function createSvgElement(name, attrs) {
        var element = document.createElementNS("http://www.w3.org/2000/svg", name);
        Object.keys(attrs || {}).forEach(function (key) {
          element.setAttribute(key, String(attrs[key]));
        });
        return element;
      }

      function renderGraph(figure) {
        var source = decodeURIComponent(figure.dataset.graph || "");
        var graph = parseGraph(source);
        var canvas = figure.querySelector(".diagram-canvas");
        if (!graph.edges.length) {
          canvas.innerHTML = '<p>Definição de diagrama disponível abaixo.</p>';
          return;
        }

        var indegree = new Map();
        var adjacency = new Map();
        graph.nodes.forEach(function (_, id) {
          indegree.set(id, 0);
          adjacency.set(id, []);
        });
        graph.edges.forEach(function (edge) {
          indegree.set(edge.to, (indegree.get(edge.to) || 0) + 1);
          adjacency.get(edge.from).push(edge.to);
        });

        var levels = new Map();
        var queue = [];
        indegree.forEach(function (degree, id) {
          if (degree === 0) {
            queue.push(id);
            levels.set(id, 0);
          }
        });
        while (queue.length) {
          var id = queue.shift();
          (adjacency.get(id) || []).forEach(function (child) {
            levels.set(child, Math.max(levels.get(child) || 0, (levels.get(id) || 0) + 1));
            indegree.set(child, indegree.get(child) - 1);
            if (indegree.get(child) === 0) queue.push(child);
          });
        }
        graph.nodes.forEach(function (_, id) {
          if (!levels.has(id)) levels.set(id, 0);
        });

        var groups = new Map();
        levels.forEach(function (level, id) {
          if (!groups.has(level)) groups.set(level, []);
          groups.get(level).push(id);
        });
        var maxLevel = Math.max.apply(null, Array.from(groups.keys()));
        var nodeW = 190;
        var nodeH = 58;
        var levelGap = graph.direction === "LR" ? 80 : 64;
        var rowGap = graph.direction === "LR" ? 34 : 42;
        var positions = new Map();

        groups.forEach(function (ids, level) {
          ids.forEach(function (id, index) {
            var x = graph.direction === "LR"
              ? 28 + level * (nodeW + levelGap)
              : 28 + index * (nodeW + rowGap);
            var y = graph.direction === "LR"
              ? 28 + index * (nodeH + rowGap)
              : 28 + level * (nodeH + levelGap);
            positions.set(id, { x: x, y: y });
          });
        });

        var maxGroupSize = Math.max.apply(null, Array.from(groups.values()).map(function (ids) {
          return ids.length;
        }));
        var width = graph.direction === "LR"
          ? 56 + (maxLevel + 1) * nodeW + maxLevel * levelGap
          : 56 + maxGroupSize * nodeW + Math.max(0, maxGroupSize - 1) * rowGap;
        var height = graph.direction === "LR"
          ? 56 + maxGroupSize * nodeH + Math.max(0, maxGroupSize - 1) * rowGap
          : 56 + (maxLevel + 1) * nodeH + maxLevel * levelGap;

        var svg = createSvgElement("svg", {
          viewBox: "0 0 " + width + " " + height,
          width: width,
          height: height,
          role: "img",
          "aria-label": "Diagrama de fluxo com " + graph.nodes.size + " elementos"
        });
        var title = createSvgElement("title");
        title.textContent = "Fluxo técnico derivado da definição Mermaid";
        svg.appendChild(title);
        var defs = createSvgElement("defs");
        var marker = createSvgElement("marker", {
          id: "arrow-" + Math.random().toString(36).slice(2),
          viewBox: "0 0 10 10",
          refX: 9,
          refY: 5,
          markerWidth: 7,
          markerHeight: 7,
          orient: "auto-start-reverse"
        });
        marker.appendChild(createSvgElement("path", {
          d: "M 0 0 L 10 5 L 0 10 z",
          fill: "var(--accent)"
        }));
        defs.appendChild(marker);
        svg.appendChild(defs);
        var markerId = marker.id;

        graph.edges.forEach(function (edge) {
          var from = positions.get(edge.from);
          var to = positions.get(edge.to);
          var path;
          if (graph.direction === "LR") {
            var sx = from.x + nodeW;
            var sy = from.y + nodeH / 2;
            var tx = to.x;
            var ty = to.y + nodeH / 2;
            var mx = (sx + tx) / 2;
            path = "M " + sx + " " + sy + " H " + mx + " V " + ty + " H " + tx;
          } else {
            var sx2 = from.x + nodeW / 2;
            var sy2 = from.y + nodeH;
            var tx2 = to.x + nodeW / 2;
            var ty2 = to.y;
            var my = (sy2 + ty2) / 2;
            path = "M " + sx2 + " " + sy2 + " V " + my + " H " + tx2 + " V " + ty2;
          }
          svg.appendChild(createSvgElement("path", {
            d: path,
            fill: "none",
            stroke: "var(--accent)",
            "stroke-width": 2,
            "marker-end": "url(#" + markerId + ")"
          }));
        });

        graph.nodes.forEach(function (label, id) {
          var pos = positions.get(id);
          var group = createSvgElement("g", { transform: "translate(" + pos.x + " " + pos.y + ")" });
          group.appendChild(createSvgElement("rect", {
            width: nodeW,
            height: nodeH,
            rx: 4,
            fill: "var(--surface)",
            stroke: "var(--border-strong)",
            "stroke-width": 1.5
          }));
          var words = label.split(/\\s+/);
          var lines = [""];
          words.forEach(function (word) {
            var current = lines[lines.length - 1];
            if ((current + " " + word).trim().length > 24 && lines.length < 2) {
              lines.push(word);
            } else {
              lines[lines.length - 1] = (current + " " + word).trim();
            }
          });
          var text = createSvgElement("text", {
            x: nodeW / 2,
            y: lines.length === 1 ? 34 : 26,
            fill: "var(--text)",
            "font-family": "Arial, sans-serif",
            "font-size": 13,
            "font-weight": 700,
            "text-anchor": "middle"
          });
          lines.forEach(function (textLine, index) {
            var tspan = createSvgElement("tspan", {
              x: nodeW / 2,
              dy: index === 0 ? 0 : 17
            });
            tspan.textContent = textLine;
            text.appendChild(tspan);
          });
          group.appendChild(text);
          svg.appendChild(group);
        });

        canvas.replaceChildren(svg);
      }

      function buildToc() {
        var headings = Array.from(renderedView.querySelectorAll("h2"));
        tocList.innerHTML = "";
        headings.forEach(function (heading) {
          var item = document.createElement("li");
          var link = document.createElement("a");
          link.className = "toc-link";
          link.href = "#" + heading.id;
          link.textContent = heading.textContent;
          link.dataset.target = heading.id;
          link.addEventListener("click", function () {
            closeSidebar();
          });
          item.appendChild(link);
          tocList.appendChild(item);
        });
      }

      function clearMarks() {
        renderedView.querySelectorAll("mark").forEach(function (mark) {
          mark.replaceWith(document.createTextNode(mark.textContent));
        });
        renderedView.normalize();
        searchMatches = [];
        currentMatch = -1;
      }

      function runSearch() {
        clearMarks();
        var query = searchInput.value.trim();
        Array.from(tocList.querySelectorAll(".toc-link")).forEach(function (link) {
          link.parentElement.hidden = query.length > 1 &&
            !link.textContent.toLocaleLowerCase("pt-BR").includes(query.toLocaleLowerCase("pt-BR"));
        });
        if (query.length < 2) {
          searchCount.textContent = "0";
          return;
        }

        var walker = document.createTreeWalker(renderedView, NodeFilter.SHOW_TEXT, {
          acceptNode: function (node) {
            if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
            if (node.parentElement.closest("script, style, .code-label, button")) {
              return NodeFilter.FILTER_REJECT;
            }
            return NodeFilter.FILTER_ACCEPT;
          }
        });
        var nodes = [];
        var current;
        while ((current = walker.nextNode())) nodes.push(current);
        var escaped = query.replace(/[.*+?^{}$()|[\\]\\\\]/g, "\\\\$&");
        var regex = new RegExp(escaped, "gi");

        nodes.forEach(function (node) {
          var value = node.nodeValue;
          if (!regex.test(value)) return;
          regex.lastIndex = 0;
          var fragment = document.createDocumentFragment();
          var lastIndex = 0;
          var match;
          while ((match = regex.exec(value))) {
            fragment.appendChild(document.createTextNode(value.slice(lastIndex, match.index)));
            var mark = document.createElement("mark");
            mark.dataset.searchMatch = "";
            mark.textContent = match[0];
            fragment.appendChild(mark);
            lastIndex = match.index + match[0].length;
          }
          fragment.appendChild(document.createTextNode(value.slice(lastIndex)));
          node.replaceWith(fragment);
        });
        searchMatches = Array.from(renderedView.querySelectorAll("mark"));
        searchCount.textContent = String(searchMatches.length);
        if (searchMatches.length) selectMatch(0);
      }

      function selectMatch(index) {
        if (!searchMatches.length) return;
        currentMatch = (index + searchMatches.length) % searchMatches.length;
        searchMatches.forEach(function (match) { match.classList.remove("is-current"); });
        searchMatches[currentMatch].classList.add("is-current");
        searchMatches[currentMatch].scrollIntoView({ behavior: "smooth", block: "center" });
        searchCount.textContent = (currentMatch + 1) + "/" + searchMatches.length;
      }

      function setMode(mode, persist) {
        document.body.dataset.mode = mode;
        document.querySelectorAll("[data-mode-target]").forEach(function (button) {
          button.setAttribute("aria-pressed", String(button.dataset.modeTarget === mode));
        });
        if (persist !== false) localStorage.setItem("sie-report-mode", mode);
        if (mode === "source") {
          sourcePre.focus({ preventScroll: true });
        }
      }

      function setTheme(theme) {
        document.body.dataset.theme = theme;
        localStorage.setItem("sie-report-theme", theme);
      }

      function openSidebar() {
        sidebar.classList.add("is-open");
        sidebarBackdrop.classList.add("is-open");
        document.body.classList.add("is-locked");
        document.getElementById("menu-button").setAttribute("aria-expanded", "true");
      }

      function closeSidebar() {
        sidebar.classList.remove("is-open");
        sidebarBackdrop.classList.remove("is-open");
        document.body.classList.remove("is-locked");
        document.getElementById("menu-button").setAttribute("aria-expanded", "false");
      }

      function showToast(message) {
        clearTimeout(toastTimer);
        toast.textContent = message;
        toast.classList.add("is-visible");
        toastTimer = window.setTimeout(function () {
          toast.classList.remove("is-visible");
        }, 2200);
      }

      function copyText(value, successMessage) {
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(value).then(function () {
            showToast(successMessage);
          });
          return;
        }
        var textarea = document.createElement("textarea");
        textarea.value = value;
        textarea.setAttribute("readonly", "");
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        textarea.remove();
        showToast(successMessage);
      }

      function initializeObservers() {
        var headings = Array.from(renderedView.querySelectorAll("h2"));
        var observer = new IntersectionObserver(function (entries) {
          var visible = entries
            .filter(function (entry) { return entry.isIntersecting; })
            .sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
          if (!visible.length) return;
          currentSectionId = visible[0].target.id;
          tocList.querySelectorAll(".toc-link").forEach(function (link) {
            link.classList.toggle("is-active", link.dataset.target === currentSectionId);
          });
        }, { rootMargin: "-18% 0px -72% 0px", threshold: [0, 1] });
        headings.forEach(function (heading) { observer.observe(heading); });
      }

      renderedView.innerHTML = renderMarkdown(markdown);
      sourcePre.textContent = markdown;
      buildToc();
      renderedView.querySelectorAll(".diagram").forEach(renderGraph);
      renderedView.querySelectorAll(".copy-code").forEach(function (button) {
        button.addEventListener("click", function () {
          copyText(button.closest(".code-block").querySelector("code").textContent, "Bloco copiado.");
        });
      });
      initializeObservers();

      document.querySelectorAll("[data-mode-target]").forEach(function (button) {
        button.addEventListener("click", function () {
          setMode(button.dataset.modeTarget);
        });
      });

      document.getElementById("theme-toggle").addEventListener("click", function () {
        setTheme(document.body.dataset.theme === "dark" ? "light" : "dark");
      });
      document.getElementById("font-decrease").addEventListener("click", function () {
        var current = Number(getComputedStyle(document.documentElement).getPropertyValue("--reader-scale")) || 1;
        var next = Math.max(0.88, Math.round((current - 0.06) * 100) / 100);
        document.documentElement.style.setProperty("--reader-scale", String(next));
        localStorage.setItem("sie-report-scale", String(next));
      });
      document.getElementById("font-increase").addEventListener("click", function () {
        var current = Number(getComputedStyle(document.documentElement).getPropertyValue("--reader-scale")) || 1;
        var next = Math.min(1.24, Math.round((current + 0.06) * 100) / 100);
        document.documentElement.style.setProperty("--reader-scale", String(next));
        localStorage.setItem("sie-report-scale", String(next));
      });
      document.getElementById("print-button").addEventListener("click", function () {
        var previous = document.body.dataset.mode;
        setMode("abnt", false);
        window.setTimeout(function () {
          window.print();
          window.setTimeout(function () { setMode(previous, false); }, 250);
        }, 120);
      });
      document.getElementById("copy-source").addEventListener("click", function () {
        copyText(markdown, "Markdown integral copiado.");
      });
      document.getElementById("download-source").addEventListener("click", function () {
        var blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
        var url = URL.createObjectURL(blob);
        var anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = "competitor-analysis.md";
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
        URL.revokeObjectURL(url);
        showToast("Download do Markdown iniciado.");
      });
      document.getElementById("copy-link").addEventListener("click", function () {
        var value = location.href.split("#")[0] + (currentSectionId ? "#" + currentSectionId : "");
        copyText(value, "Link da seção copiado.");
      });
      document.getElementById("menu-button").addEventListener("click", function () {
        if (sidebar.classList.contains("is-open")) closeSidebar();
        else openSidebar();
      });
      sidebarBackdrop.addEventListener("click", closeSidebar);

      var searchTimer = 0;
      searchInput.addEventListener("input", function () {
        clearTimeout(searchTimer);
        searchTimer = window.setTimeout(runSearch, 180);
      });
      searchInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && searchMatches.length) {
          event.preventDefault();
          selectMatch(currentMatch + (event.shiftKey ? -1 : 1));
        }
        if (event.key === "Escape") {
          searchInput.value = "";
          runSearch();
          searchInput.blur();
        }
      });

      window.addEventListener("keydown", function (event) {
        if (event.key === "/" && !/input|textarea/i.test(document.activeElement.tagName)) {
          event.preventDefault();
          searchInput.focus();
          openSidebar();
        }
        if (event.key === "Escape") closeSidebar();
      });

      window.addEventListener("scroll", function () {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        var ratio = max > 0 ? window.scrollY / max : 0;
        document.getElementById("reading-progress").style.width = Math.min(100, ratio * 100) + "%";
      }, { passive: true });

      var storedTheme = localStorage.getItem("sie-report-theme");
      var preferredTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      setTheme(storedTheme || preferredTheme);
      var storedMode = localStorage.getItem("sie-report-mode");
      setMode(["reading", "abnt", "source"].includes(storedMode) ? storedMode : "reading", false);
      var storedScale = Number(localStorage.getItem("sie-report-scale"));
      if (storedScale >= 0.88 && storedScale <= 1.24) {
        document.documentElement.style.setProperty("--reader-scale", String(storedScale));
      }

      if (location.hash) {
        window.setTimeout(function () {
          var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
          if (target) target.scrollIntoView();
        }, 40);
      }
    })();
  </script>
</body>
</html>`;

writeFileSync(outputPath, html, "utf8");

console.log(
  JSON.stringify(
    {
      source: sourcePath,
      output: outputPath,
      bytes: Buffer.byteLength(html),
      sourceBytes: Buffer.byteLength(markdown),
      sha256,
      lineCount,
      wordCount,
      sectionCount,
    },
    null,
    2,
  ),
);
