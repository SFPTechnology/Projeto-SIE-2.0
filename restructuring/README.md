# SIE 2.0 — Fundação modular (incremento 001)

Este diretório é um **protótipo técnico isolado**, não substitui o SIE legado e não realiza dimensionamento normativo. A API só valida estrutura de dados; os motores ficam bloqueados até haver dados normativos e testes de referência auditados.

## Teste local (Windows, PowerShell)

```powershell
cd restructuring/apps/api
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
python -m pytest -q
python -m uvicorn sie_api.main:app --reload
```

Abra http://127.0.0.1:8000/docs e experimente GET /api/v1/health e POST /api/v1/projetos/validar.

## Limites
- Nenhum cálculo é aprovado para emprego profissional.
- Nenhum arquivo pré-existente foi removido ou substituído.
- O legado TypeScript permanece sob análise de equivalência funcional.
- Integração com projetos persistidos, UI, desenhos, norma e banco ainda são tarefas futuras.
