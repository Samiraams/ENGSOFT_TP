import sqlite3

class Database:
    def __init__(self, db_path="db/data_labeler.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)
