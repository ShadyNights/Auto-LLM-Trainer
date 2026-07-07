import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        if self.connection is None or self.connection.closed:
            self.connection = psycopg2.connect(
                dbname=os.getenv("PGDATABASE", "traveler_db"),
                user=os.getenv("PGUSER", "postgres"),
                password=os.getenv("PGPASSWORD", "postgres"),
                host=os.getenv("PGHOST", "localhost"),
                port=os.getenv("PGPORT", "5432"),
            )
        return self.connection

    @contextmanager
    def get_cursor(self, commit_on_success: bool = True):
        conn = self.connect()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit_on_success:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    @contextmanager
    def transaction(self):
        """Allows grouping multiple cursor operations in one transaction."""
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
