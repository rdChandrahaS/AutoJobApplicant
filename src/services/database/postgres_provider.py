import os
import psycopg
from src.services.interfaces.DatabaseProvider import DatabaseProvider
from langchain_postgres import PostgresChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

class PostgresDatabase(DatabaseProvider):
    def __init__(self):
        self.uri = os.getenv("DB_URI")
        self.table_name = "chat_history"
        self.sessions_table = "user_sessions"
        self._init_tables()

    def _get_connection(self):
        return psycopg.connect(self.uri, autocommit=True)

    def _init_tables(self):
        with self._get_connection() as conn:
            PostgresChatMessageHistory.create_tables(conn, self.table_name)
            with conn.cursor() as cur:
                cur.execute(f"CREATE TABLE IF NOT EXISTS {self.sessions_table} (session_id TEXT PRIMARY KEY, title TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

    def add_user_message(self, session_id: str, message: str):
        history = self.get_history(session_id)
        history.add_user_message(message)

    def add_ai_message(self, session_id: str, message: str):
        history = self.get_history(session_id)
        history.add_ai_message(message)

    def get_history(self, session_id: str):
        return PostgresChatMessageHistory(self.table_name, str(session_id), sync_connection=self._get_connection())

    def save_session_title(self, session_id: str, title: str):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"INSERT INTO {self.sessions_table} (session_id, title) VALUES (%s, %s) ON CONFLICT (session_id) DO NOTHING;", (str(session_id), title))

    def get_all_sessions(self):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT session_id, title FROM {self.sessions_table} ORDER BY created_at DESC;")
                return [{"id": r[0], "title": r[1]} for r in cur.fetchall()]

    def delete_session(self, session_id: str):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {self.sessions_table} WHERE session_id = %s;", (str(session_id),))
                cur.execute(f"DELETE FROM {self.table_name} WHERE session_id = %s;", (str(session_id),))