#!/us

    # atributos
    attrs = conn.execute(
        "SELECT attr_name FROM dataset_attributes WHERE dataset_id=? ORDER BY id",
        (ds["id"],)
    ).fetchall()
