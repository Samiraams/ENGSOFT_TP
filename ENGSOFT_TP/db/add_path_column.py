import sqlite3

conn = sqlite3.connect("datalabeler.db")
conn.execute("PRAGMA foreign_keys = ON;")
conn.execute(
conn.close()
print("Coluna 'path' adicionada com NOT NULL e default ''.")
