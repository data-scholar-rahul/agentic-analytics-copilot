from app.db.postgres_client import PostgresClient
from app.schemas.semantic import SemanticContextResponse


class SemanticService:
    def __init__(self, db: PostgresClient):
        self.db = db

    def get_metrics(self) -> list[dict]:
        sql = """
        SELECT
            metric_name,
            business_definition,
            sql_expression,
            grain,
            default_filters,
            required_tables,
            caveats
        FROM semantic.metric_catalog
        ORDER BY metric_name;
        """
        return self.db.execute_select(sql)

    def get_tables(self) -> list[dict]:
        sql = """
        SELECT
            schema_name,
            table_name,
            business_description,
            grain
        FROM semantic.table_catalog
        ORDER BY schema_name, table_name;
        """
        return self.db.execute_select(sql)

    def get_join_rules(self) -> list[dict]:
        sql = """
        SELECT
            left_schema,
            left_table,
            left_column,
            right_schema,
            right_table,
            right_column,
            relationship_type,
            business_description
        FROM semantic.join_rules
        ORDER BY left_table, right_table;
        """
        return self.db.execute_select(sql)

    def get_glossary(self) -> list[dict]:
        sql = """
        SELECT
            term,
            definition,
            example
        FROM semantic.business_glossary
        ORDER BY term;
        """
        return self.db.execute_select(sql)

    def get_semantic_context(self) -> SemanticContextResponse:
        return SemanticContextResponse(
            metrics=self.get_metrics(),
            tables=self.get_tables(),
            join_rules=self.get_join_rules(),
            glossary=self.get_glossary(),
        )