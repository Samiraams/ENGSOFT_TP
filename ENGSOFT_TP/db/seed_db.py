#!/usr/bin/env python3
import sqlite3, pathlib, datetime


        "sample_size": 50,
        "num_samples": 20,
        "num_evaluators": 3,
        "is_multilabel": 1,
        "is_private": 0,
        "access_pwd": None,
        "attrs": ["username", "email", "message"],
        "labels": ["elogio", "reclamação", "dúvida", "sugestão"],
    },
    {
        "name": "Product Reviews",
        "owner": "Maria Oliveira",                   # 👈 novo
        "description": "Short reviews of consumer electronics collected from e-commerce.",
        "type": "jsonl",
        "separator": None,
        "sample_size": 30,
        "num_samples": 10,
        "num_evaluators": 4,
        "is_multilabel": 0,
        "is_private": 0,
        "access_pwd": None,
        "attrs": ["category", "review"],
        "labels": ["bug", "improvement", "praise"],
    },
]

for ds in datasets:
    cur = conn.execute(
        """INSERT INTO datasets
           (name, owner_name, description, type, separator,
            sample_size, num_samples, num_evaluators,
            is_multilabel, is_private, access_pwd, created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            ds["name"], ds["owner"], ds["description"], ds["type"], ds["separator"],
            ds["sample_size"], ds["num_samples"], ds["num_evaluators"],
            ds["is_multilabel"], ds["is_private"], ds["access_pwd"],
            datetime.datetime.utcnow(),
        ),
    )
    ds_id = cur.lastrowid

    conn.executemany(
        "INSERT INTO dataset_attributes(dataset_id, attr_name) VALUES (?,?)",
        [(ds_id, a) for a in ds["attrs"]],
    )
    conn.executemany(
        "INSERT INTO dataset_labels(dataset_id, label_text) VALUES (?,?)",
        [(ds_id, l) for l in ds["labels"]],
    )

conn.commit()
conn.close()
print("Seeds aplicados com sucesso.")
