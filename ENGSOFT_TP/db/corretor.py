#!/usr/bin/env python3
import sqlite3
import sys

    # 1) Inicia transação
    cursor.execute("BEGIN TRANSACTION;")

    # 2) Cria tabela nova sem NOT NULL em owner_name
    cursor.execute("""
    CREATE TABLE datasets_new (
      id               INTEGER PRIMARY KEY AUTOINCREMENT,
      name             VARCHAR(100)   NOT NULL,
      owner_name       VARCHAR(100),         -- agora opcional
      description      TEXT           NOT NULL,
      type             TEXT           NOT NULL CHECK(type IN ('csv','jsonl')),
      separator        TEXT           CHECK(separator IN ('COMMA','SEMICOLON','TAB','PIPE','SPACE')),
      sample_size      INTEGER        NOT NULL CHECK(sample_size > 0),
      num_samples      INTEGER        NOT NULL CHECK(num_samples > 0),
      num_evaluators   INTEGER        NOT NULL CHECK(num_evaluators > 0),
      is_multilabel    INTEGER        NOT NULL DEFAULT 0,
      is_private       INTEGER        NOT NULL DEFAULT 0,
      access_pwd       VARCHAR(255),
      created_at       DATETIME       DEFAULT CURRENT_TIMESTAMP,
      CHECK (is_private = 0 
             OR (access_pwd IS NOT NULL AND access_pwd <> ''))
    );
    """)

    # 3) Copia dados da tabela antiga
    cursor.execute("""
    INSERT INTO datasets_new (
      id, name, owner_name, description, type,
      separator, sample_size, num_samples,
      num_evaluators, is_multilabel,
      is_private, access_pwd, created_at
    )
    SELECT
      id, name, owner_name, description, type,
      separator, sample_size, num_samples,
      num_evaluators, is_multilabel,
      is_private, access_pwd, created_at
    FROM datasets;
    """)

    # 4) Drop da tabela antiga
    cursor.execute("DROP TABLE datasets;")

    # 5) Renomeia a nova
    cursor.execute("ALTER TABLE datasets_new RENAME TO datasets;")

    # 6) (Re)crie índices ou FKs, se houverem
    # Por exemplo, se havia um índice em datasets(name):
    # cursor.execute("CREATE INDEX idx_datasets_name ON datasets(name);")
    #
    # Se houver triggers ou outros constraints, recrie aqui.

    # 7) Reabilita FKs e dá commit
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    print("Coluna owner_name agora é opcional (NOT NULL removido).")
except Exception as e:
    conn.rollback()
    print("Erro ao alterar esquema:", e, file=sys.stderr)
finally:
    conn.close()
