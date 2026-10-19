"""Persistencia local isolada para projetos em teste (sem API publica).
SQLite com revisoes otimistas e trilha transacional de alteracoes.
Nao armazena decisao de conformidade normativa.
"""
import json
import sqlite3
from hashlib import sha256
from .analysis_contracts import AnaliseCircuito
from .application import analisar_circuito
from .calculation_traces import preparar_registro, validar_registro
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID
from .normative_snapshots import (serializar_catalogo, validar_snapshot,
                                  diferenca_snapshot)


class ConflitoRevisao(ValueError):
    pass


def _dados_revisao_validada(projeto_id: str, row) -> dict:
    """Validate the immutable saved version inside the caller's transaction."""
    dados = json.loads(row["dados_json"])
    encoded = json.dumps(
        {"projeto_id": projeto_id, "revisao": row["revisao"],
         "nome": row["nome"], "dados": dados},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")
    if sha256(encoded).hexdigest() != row["hash_sha256"]:
        raise ValueError("Integridade da revisao historica comprometida")
    return dados


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
                CREATE TABLE IF NOT EXISTS ensaios_calculo(
                    id TEXT PRIMARY KEY,
                    projeto_id TEXT NOT NULL,
                    revisao_projeto INTEGER NOT NULL,
                    circuito_nome TEXT NOT NULL,
                    registro_json TEXT NOT NULL,
                    hash_sha256 TEXT NOT NULL CHECK(length(hash_sha256)=64),
                    criado_em TEXT NOT NULL,
                    FOREIGN KEY(projeto_id,revisao_projeto)
                        REFERENCES versoes_projeto(projeto_id,revisao)
                );
                CREATE INDEX IF NOT EXISTS f01_ensaio_por_circuito
                    ON ensaios_calculo(projeto_id,revisao_projeto,circuito_nome);
                CREATE TRIGGER IF NOT EXISTS f01_ensaio_sem_update
                    BEFORE UPDATE ON ensaios_calculo
                    BEGIN SELECT RAISE(ABORT, 'ensaio de calculo imutavel'); END;
                CREATE TRIGGER IF NOT EXISTS f01_ensaio_sem_delete
                    BEFORE DELETE ON ensaios_calculo
                    BEGIN SELECT RAISE(ABORT, 'ensaio de calculo imutavel'); END;
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
        dados = _dados_revisao_validada(projeto_id, row)
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


    def registrar_ensaio(self, projeto_id: str, revisao: int,
                         circuito_nome: str, parametros: dict) -> dict:
        """Executa motor no servidor e persiste a trilha do ensaio, NAO conformidade."""
        projeto_id = str(UUID(projeto_id))
        if type(revisao) is not int or revisao < 1:
            raise ValueError("Revisao de projeto invalida")
        if not isinstance(circuito_nome, str) or not 1 <= len(circuito_nome.strip()) <= 120:
            raise ValueError("Identificacao de circuito invalida")
        circuito_nome = circuito_nome.strip()
        if not isinstance(parametros, dict):
            raise ValueError("Parametros de ensaio invalidos")
        solicitada = AnaliseCircuito.model_validate(parametros).model_dump(mode="json")
        with self._conectar() as db:
            db.execute("BEGIN IMMEDIATE")
            atual = db.execute(
                "SELECT revisao FROM projetos WHERE id=?",
                (projeto_id,),
            ).fetchone()
            if atual is None:
                raise ValueError("Projeto inexistente")
            if atual["revisao"] != revisao:
                raise ConflitoRevisao("Ensaio exige revisao atual e imutavel do projeto")
            historico = db.execute(
                "SELECT revisao,nome,dados_json,hash_sha256 FROM versoes_projeto "
                "WHERE projeto_id=? AND revisao=?",
                (projeto_id, revisao),
            ).fetchone()
            if historico is None:
                raise ValueError("Revisao sem historico recuperavel; salvar antes do ensaio")
            dados_historicos = _dados_revisao_validada(projeto_id, historico)
            circuitos = dados_historicos.get("circuitos", [])
            if not isinstance(circuitos, list):
                raise ValueError("Lista de circuitos invalida")
            coincidentes = [
                c for c in circuitos if isinstance(c, dict)
                and isinstance(c.get("nome"), str)
                and c["nome"].strip().casefold() == circuito_nome.casefold()
            ]
            if len(coincidentes) != 1:
                raise ValueError("Circuito ausente ou identificado ambiguamente na revisao")
            armazenado = coincidentes[0]
            # Project metadata (name/type/etc.) is separate from the complete
            # typed analysis input. Missing/invalid legacy values cannot be
            # filled from a new request or the mutable current project copy.
            campos = AnaliseCircuito.model_fields
            try:
                entrada = AnaliseCircuito.model_validate({
                    campo: armazenado[campo] for campo in campos if campo in armazenado
                }).model_dump(mode="json")
            except ValueError as exc:
                raise ValueError(
                    "Circuito salvo incompleto ou inválido para ensaio; "
                    "salve uma nova revisão com todos os parâmetros de análise") from exc
            for campo in campos:
                if entrada[campo] != solicitada[campo]:
                    raise ValueError(
                        f"Ensaio incompatível com campo salvo do circuito: {campo}")
            # Always execute the immutable server-saved input after comparison.
            # Retorno da funcao real, nao "expected" produzido pelo cliente.
            resultado = analisar_circuito(entrada)
            if (resultado["liberado_para_uso_normativo"] is not False or
                resultado["status_engenharia"] != "PENDENTE"):
                raise ValueError("Motor nao possui estado seguro para ensaio nao homologado")
            _, serializado, digest = preparar_registro(
                projeto_id, revisao, armazenado["nome"].strip(), entrada, resultado,
            )
            if len(serializado.encode("utf-8")) > 1_048_576:
                raise ValueError("Registro de calculo excede 1 MiB")
            registro = validar_registro(serializado, digest)
            db.execute(
                "INSERT INTO ensaios_calculo(id,projeto_id,revisao_projeto,"
                "circuito_nome,registro_json,hash_sha256,criado_em) VALUES(?,?,?,?,?,?,?)",
                (registro["id"], projeto_id, revisao, registro["circuito_nome"],
                 serializado, digest, datetime.now(timezone.utc).isoformat()),
            )
        return {**registro, "hash_sha256": digest}

    def consultar_ensaio(self, projeto_id: str, ensaio_id: str) -> dict | None:
        projeto_id, ensaio_id = str(UUID(projeto_id)), str(UUID(ensaio_id))
        with self._conectar() as db:
            row = db.execute(
                "SELECT registro_json,hash_sha256 FROM ensaios_calculo "
                "WHERE projeto_id=? AND id=?", (projeto_id, ensaio_id),
            ).fetchone()
        if row is None:
            return None
        item = validar_registro(row["registro_json"], row["hash_sha256"])
        if item["projeto_id"] != projeto_id or item["id"] != ensaio_id:
            raise ValueError("Vinculo do ensaio ao projeto inconsistente")
        return {**item, "hash_sha256": row["hash_sha256"]}

    def listar_ensaios(self, projeto_id: str, revisao: int) -> list[dict]:
        projeto_id = str(UUID(projeto_id))
        if type(revisao) is not int or revisao < 1:
            raise ValueError("Revisao de projeto invalida")
        with self._conectar() as db:
            rows = db.execute(
                "SELECT id,registro_json,hash_sha256,criado_em FROM ensaios_calculo "
                "WHERE projeto_id=? AND revisao_projeto=? ORDER BY criado_em,id",
                (projeto_id, revisao),
            ).fetchall()
        result = []
        for row in rows:
            item = validar_registro(row["registro_json"], row["hash_sha256"])
            if item["id"] != row["id"] or item["projeto_id"] != projeto_id or item["revisao_projeto"] != revisao:
                raise ValueError("Vinculo de ensaio inconsistente")
            result.append({"id": row["id"], "circuito_nome": item["circuito_nome"],
                           "hash_sha256": row["hash_sha256"],
                           "criado_em": row["criado_em"],
                           "normative_conformity_verified": False})
        return result
