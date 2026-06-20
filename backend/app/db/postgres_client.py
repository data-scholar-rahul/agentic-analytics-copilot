from typing import Any

import psycopg
from psycopg.rows import dict_row

class PostgresClient:
    def __init__(self, database_url: str):
        self.database_url = database_url
    
    def execute_select(self, sql: str) -> list[dict[str, Any]]:
        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                return [dict(row) for row in rows]
    
    def execute_statement(self, sql: str) -> None:
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
