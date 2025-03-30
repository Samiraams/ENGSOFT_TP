PRAGMA foreign_keys = ON;

-- 1) evaluators
CREATE TABLE evaluators (

  description      TEXT           NOT NULL,
  type             TEXT           NOT NULL CHECK(type IN ('csv','jsonl')),
  separator        TEXT           CHECK(separator IN ('COMMA','SEMICOLON','TAB','PIPE','SPACE')),
  sample_size      INTEGER        NOT NULL CHECK(sample_size > 0),
  
  FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
);

-- 4) dataset_labels
CREATE TABLE dataset_labels (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  dataset_id INTEGER NOT NULL,
  label_text VARCHAR(255) NOT NULL,
  FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
  UNIQUE(dataset_id, label_text)
);

-- 5) samples
CREATE TABLE samples (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  dataset_id     INTEGER NOT NULL,
  sample_number  INTEGER NOT NULL,
  is_completed   INTEGER NOT NULL DEFAULT 0,
  created_at     DATETIME  DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
  UNIQUE(dataset_id, sample_number)
);

-- 6) sample_rows
CREATE TABLE sample_rows (
  sample_id  INTEGER NOT NULL,
  dataset_id INTEGER NOT NULL,
  row_index  INTEGER NOT NULL,
  FOREIGN KEY(sample_id)  REFERENCES samples(id)  ON DELETE CASCADE,
  FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
  UNIQUE(sample_id, row_index),
  UNIQUE(dataset_id, row_index)
);

-- 7) annotations
CREATE TABLE annotations (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  sample_id       INTEGER NOT NULL,
  row_index       INTEGER NOT NULL,
  evaluator_email VARCHAR(255) NOT NULL,
  label_id        INTEGER NOT NULL,
  created_at      DATETIME    DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(sample_id)       REFERENCES samples(id)       ON DELETE CASCADE,
  FOREIGN KEY(evaluator_email) REFERENCES evaluators(email) ON DELETE CASCADE,
  FOREIGN KEY(label_id)        REFERENCES dataset_labels(id) ON DELETE CASCADE,
  UNIQUE(sample_id, row_index, evaluator_email)
);
