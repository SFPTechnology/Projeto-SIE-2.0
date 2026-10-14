"""Persistencia local isolada para projetos em teste (sem API publica).
SQLite com revisoes otimistas e trilha transacional de alteracoes.
Nao armazena decisao de conformidade normativa.
"""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID


class ConflitoRevisao(ValueError):
    pass


class RepositorioProjetos:
    def __init__(self, caminho: str | Path):
        self.caminho = str(caminho)
        with self._conectar() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS projetos(
                    id TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    dados_json TEXT NOT NULL,
                    revisao INTEGER NOT NULL CHECK(revisao >= 1),
                    atualizado_em TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS eventos_auditoria(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projeto_id TEXT NOT NULL REFERENCES projetos(id),
                    acao TEXT NOT NULL,
                    revisao INTEGER NOT NULL,
                    criado_em TEXT NOT NULL
                );
            """)

    def _conectar(self):
        db = sqlite3.connect(self.caminho, timeout=5)
        db.execute("PRAGMA foreign_keys = ON")
        db.row_factory = sqlite3.Row
        return db

    def salvar(self, projeto_id: str, nome: str, dados: dict, revisao_esperada: int) -> int:
        projeto_id = str(UUID(projeto_id))
        nome = nome.strip()
        if not 1 <= len(nome) <= 160:
            raise ValueError("Nome do projeto invalido")
        if not isinstance(dados, dict):
            raise ValueError("Dados do projeto devem ser um objeto")
        if not isinstance(revisao_esperada, int) or isinstance(revisao_esperada, bool) or revisao_esperada < 0:
            raise ValueError("Revisao esperada invalida")
        conteudo = json.dumps(dados, ensure_ascii=False, sort_keys=True, allow_nan=False)
        agora = datetime.now(timezone.utc).isoformat()
        with self._conectar() as db:
            db.execute("BEGIN IMMEDIATE")
            anterior = db.execute("SELECT revisao FROM projetos WHERE id = ?", (projeto_id,)).fetchone()
            revisao_atual = anterior["revisao"] if anterior else 0
            if revisao_atual != revisao_esperada:
                raise ConflitoRevisao(f"Revisao esperada {revisao_esperada}, atual {revisao_atual}")
            nova_revisao = revisao_atual + 1
            if anterior:
                db.execute(
                    "UPDATE projetos SET nome=?, dados_json=?, revisao=?, atualizado_em=? WHERE id=?",
                    (nome, conteudo, nova_revisao, agora, projeto_id),
                )
            else:
                db.execute(
                    "INSERT INTO projetos(id,nome,dados_json,revisao,atualizado_em) VALUES(?,?,?,?,?)",
                    (projeto_id, nome, conteudo, nova_revisao, agora),
                )
            db.execute(
                "INSERT INTO eventos_auditoria(projeto_id,acao,revisao,criado_em) VALUES(?,?,?,?)",
                (projeto_id, "CRIAR" if anterior is None else "ATUALIZAR", nova_revisao, agora),
            )
        return nova_revisao

    def carregar(self, projeto_id: str) -> dict | None:
        projeto_id = str(UUID(projeto_id))
        with self._conectar() as db:
            row = db.execute("SELECT * FROM projetos WHERE id=?", (projeto_id,)).fetchone()
        if row is None:
            return None
        return {
            "id": row["id"], "nome": row["nome"], "dados": json.loads(row["dados_json"]),
            "revisao": row["revisao"], "atualizado_em": row["atualizado_em"],
        }

    def historico(self, projeto_id: str) -> list[dict]:
        projeto_id = str(UUID(projeto_id))
        with self._conectar() as db:
            rows = db.execute(
                "SELECT acao,revisao,criado_em FROM eventos_auditoria WHERE projeto_id=? ORDER BY id",
                (projeto_id,),
            ).fetchall()
        return [dict(row) for row in rows]
