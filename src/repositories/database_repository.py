import pandas as pd
from typing import Optional
from src.infrastructure.database.connection import DatabaseConnection
from src.domain.enums.table_type import TableType

class DatabaseRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_records(self, table: TableType, limit: int = 50) -> pd.DataFrame:
        """Returns records for a whitelisted table as a pandas DataFrame."""
        try:
            # TableType enum ensures the table name is safe and whitelisted.
            query = f"SELECT * FROM {table.value} ORDER BY id DESC LIMIT %s"
            
            with self.db.get_cursor() as cur:
                cur.execute(query, (limit,))
                rows = cur.fetchall()
                if rows:
                    return pd.DataFrame(rows)
                return pd.DataFrame()
        except Exception:
            return pd.DataFrame()
