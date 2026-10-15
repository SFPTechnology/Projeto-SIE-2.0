"""Persistencia local isolada para projetos em teste (sem API publica).
SQLite com revisoes otimistas e trilha transacional de alteracoes.
Nao armazena decisao de conformidade normativa.
"""
import json
import sqlite3
from hashlib import sha256
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID
from .normative_snapshots import (serializar_catalogo, validar_snapshot,
                                  diferenca_snapshot)


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
                CREATE TABLE IF NOT EXISTS snapshots_normativos(
                    projeto_id TEXT NOT NULL REFERENCES projetos(id),
                    revisao_projeto INTEGER NOT NULL CHECK(revisao_projeto >= 1),
                    hash_sha256 TEXT NOT NULL,
                    catalogo_json TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status='NAO_HOMOLOGADO'),
                    criado_em TEXT NOT NULL,
                    PRIMARY KEY(projeto_id, revisao_projeto)
                );
                CREATE TABLE IF NOT EXISTS eventos_snapshot_normativo(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    projeto_id TEXT NOT NULL REFERENCES projetos(id),
                    revisao_projeto INTEGER NOT NULL,
                    hash_sha256 TEXT NOT NULL,
                    alteracoes_json TEXT NOT NULL,
                    criado_em TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS versoes_projeto(
                    projeto_id TEXT NOT NULL REFERENCES projetos(id),
                    revisao INTEGER NOT NULL CHECK(revisao >= 1),
                    nome TEXT NOT NULL,
                    dados_json TEXT NOT NULL,
                    hash_sha256 TEXT NOT NULL CHECK(length(hash_sha256)=64),
                    criado_em TEXT NOT NULL,
                    PRIMARY KEY(projeto_id, revisao)
                );
                CREATE TRIGGER IF NOT EXISTS f01_versao_sem_update
                    BEFORE UPDATE ON versoes_projeto
                    BEGIN SELECT RAISE(ABORT, 'versao de projeto imutavel'); END;
                CREATE TRIGGER IF NOT EXISTS f01_versao_sem_delete
                    BEFORE DELETE ON versoes_projeto
                    BEGIN SELECT RAISE(ABORT, 'versao de projeto imutavel'); END;
                CREATE TRIGGER IF NOT EXISTS f01_snapshot_sem_update
                    BEFORE UPDATE ON snapshots_normativos
                    BEGIN SELECT RAISE(ABORT, 'snapshot normativo imutavel'); END;
                CREATE TRIGGER IF NOT EXISTS f01_snapshot_sem_delete
                    BEFORE DELETE ON snapshots_normativos
                    BEGIN SELECT RAISE(ABORT, 'snapshot normativo imutavel'); END;
                CREATE TRIGGER IF NOT EXISTS f01_evento_sem_update
                    BEFORE UPDATE ON eventos_snapshot_normativo
                    BEGIN SELECT RAISE(ABORT, 'evento normativo imutavel'); END;
                CREATE TRIGGER IF NOT EXISTS f01_evento_sem_delete
                    BEFORE DELETE ON eventos_snapshot_normativo
                    BEGIN SELECT RAISE(ABORT, 'evento normativo imutavel'); END;
            """)

    @contextmanager
    def _conectar(self):
        db = sqlite3.connect(self.caminho, timeout=5)
        try:
            db.execute("PRAGMA foreign_keys = ON")
            db.row_factory = sqlite3.Row
            with db:
                yield db
        finally:
            db.close()

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
        if len(conteudo.encode("utf-8")) > 1_048_576:
            raise ValueError("Projeto excede tamanho local permitido (1 MiB)")
        # Registro é obtido exclusivamente do catálogo local do servidor. A entrada
        # arbitrária do usuário não contém chaves de aprovação confiáveis.
        catalogo_json, hash_catalogo = serializar_catalogo()
        catalogo_atual = validar_snapshot(catalogo_json, hash_catalogo)
        agora = datetime.now(timezone.utc).isoformat()
        with self._conectar() as db:
            db.execute("BEGIN IMMEDIATE")
            anterior = db.execute("SELECT revisao FROM projetos WHERE id = ?", (projeto_id,)).fetchone()
            revisao_atual = anterior["revisao"] if anterior else 0
            if revisao_atual != revisao_esperada:
                raise ConflitoRevisao(f"Revisao esperada {revisao_esperada}, atual {revisao_atual}")
            anterior_snapshot = db.execute(
                "SELECT catalogo_json,hash_sha256 FROM snapshots_normativos "
                "WHERE projeto_id=? ORDER BY revisao_projeto DESC LIMIT 1",
                (projeto_id,),
            ).fetchone()
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
            # Histórico completo: somete versões criadas APÓS habilitar este recurso.
            # Registrar nome e dados efetivamente gravados na mesma transação.
            registro_versao = json.dumps(
                {"projeto_id": projeto_id, "revisao": nova_revisao,
                 "nome": nome, "dados": json.loads(conteudo)},
                ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
            )
            hash_versao = sha256(registro_versao.encode("utf-8")).hexdigest()
            db.execute(
                "INSERT INTO versoes_projeto(projeto_id,revisao,nome,dados_json,"
                "hash_sha256,criado_em) VALUES(?,?,?,?,?,?)",
                (projeto_id, nova_revisao, nome, conteudo, hash_versao, agora),
            )
            db.execute(
                "INSERT INTO eventos_auditoria(projeto_id,acao,revisao,criado_em) VALUES(?,?,?,?)",
                (projeto_id, "CRIAR" if anterior is None else "ATUALIZAR", nova_revisao, agora),
            )
            db.execute(
                "INSERT INTO snapshots_normativos(projeto_id,revisao_projeto,hash_sha256,"
                "catalogo_json,status,criado_em) VALUES (?,?,?,?,?,?)",
                (projeto_id, nova_revisao, hash_catalogo, catalogo_json,
                 "NAO_HOMOLOGADO", agora),
            )
            # Não reconstruir retroativamente versões anteriores de projetos legados.
            # Um snapshot mais recente permite identificar impacto sem recalcular.
            diferenca = (diferenca_snapshot(
                validar_snapshot(anterior_snapshot["catalogo_json"],
                                  anterior_snapshot["hash_sha256"]),
                catalogo_atual,
            ) if anterior_snapshot else {
                "changed": False, "changes": [], "requires_technical_revalidation": False,
                "release_allowed": False, "recalculated_automatically": False,
            })
            db.execute(
                "INSERT INTO eventos_snapshot_normativo("
                "projeto_id,revisao_projeto,hash_sha256,alteracoes_json,criado_em)"
                " VALUES(?,?,?,?,?)",
                (projeto_id, nova_revisao, hash_catalogo,
                 json.dumps(diferenca, ensure_ascii=False, sort_keys=True), agora),
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

    def snapshot_normativo(self, projeto_id: str, revisao_projeto: int) -> dict | None:
        """Retorna cópia histórica do CATÁLOGO, não valores calculados."""
        projeto_id = str(UUID(projeto_id))
        if type(revisao_projeto) is not int or revisao_projeto < 1:
            raise ValueError("Revisao de projeto invalida")
        with self._conectar() as db:
            row = db.execute(
                "SELECT * FROM snapshots_normativos WHERE projeto_id=? AND revisao_projeto=?",
                (projeto_id, revisao_projeto),
            ).fetchone()
        if row is None:
            return None
        snapshot = validar_snapshot(row["catalogo_json"], row["hash_sha256"])
        return {"projeto_id": projeto_id, "revisao_projeto": row["revisao_projeto"],
                "hash_sha256": row["hash_sha256"], "criado_em": row["criado_em"],
                "status": row["status"], "snapshot": snapshot,
                "catalogo_associado_na_gravacao": True,
                "regras_utilizadas_no_calculo_comprovadas": False}

    def impacto_normativo(self, projeto_id: str, revisao_projeto: int) -> dict | None:
        antigo = self.snapshot_normativo(projeto_id, revisao_projeto)
        if antigo is None:
            return None
        atual_json, digest = serializar_catalogo()
        atual = validar_snapshot(atual_json, digest)
        return {"projeto_id": antigo["projeto_id"], "revisao_projeto": revisao_projeto,
                "snapshot_sha256": antigo["hash_sha256"],
                "catalogo_atual_sha256": digest,
                **diferenca_snapshot(antigo["snapshot"], atual),
                "normative_conformity_verified": False}

    def historico_snapshot_normativo(self, projeto_id: str) -> list[dict]:
        projeto_id = str(UUID(projeto_id))
        with self._conectar() as db:
            rows = db.execute(
                "SELECT revisao_projeto,hash_sha256,alteracoes_json,criado_em "
                "FROM eventos_snapshot_normativo WHERE projeto_id=? ORDER BY id",
                (projeto_id,),
            ).fetchall()
        return [{"revisao_projeto": r["revisao_projeto"],
                 "hash_sha256": r["hash_sha256"],
                 "impacto_no_salvamento": json.loads(r["alteracoes_json"]),
                 "criado_em": r["criado_em"]} for r in rows]


    def carregar_revisao(self, projeto_id: str, revisao: int) -> dict | None:
        """Recupera só a versão salva desde a criação do histórico, com digest."""
        projeto_id = str(UUID(projeto_id))
        if type(revisao) is not int or revisao < 1:
            raise ValueError("Revisao historica invalida")
        with self._conectar() as db:
            row = db.execute(
                "SELECT revisao,nome,dados_json,hash_sha256,criado_em FROM versoes_projeto "
                "WHERE projeto_id=? AND revisao=?", (projeto_id, revisao),
            ).fetchone()
        if row is None:
            return None  # Sem backfill fictício para projetos legados.
        dados = json.loads(row["dados_json"])
        encoded = json.dumps(
            {"projeto_id": projeto_id, "revisao": row["revisao"],
             "nome": row["nome"], "dados": dados},
            ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
        ).encode("utf-8")
        if sha256(encoded).hexdigest() != row["hash_sha256"]:
            raise ValueError("Integridade da revisao historica comprometida")
        return {
            "id": projeto_id, "revisao": row["revisao"],
            "nome": row["nome"], "dados": dados, "criado_em": row["criado_em"],
            "hash_sha256": row["hash_sha256"],
            "historico_recuperavel": True, "normative_conformity_verified": False,
            "regras_efetivamente_usadas_comprovadas": False,
        }

    def listar_revisoes(self, projeto_id: str) -> list[dict]:
        """Somente metadados de revisões realmente preservadas."""
        projeto_id = str(UUID(projeto_id))
        with self._conectar() as db:
            rows = db.execute(
                "SELECT revisao,nome,hash_sha256,criado_em FROM versoes_projeto "
                "WHERE projeto_id=? ORDER BY revisao", (projeto_id,),
            ).fetchall()
        return [{"revisao": row["revisao"], "nome": row["nome"],
                 "hash_sha256": row["hash_sha256"], "criado_em": row["criado_em"]}
                for row in rows]
