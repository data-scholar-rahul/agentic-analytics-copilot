from app.db.postgres_client import PostgresClient


CREATE_SCHEMAS_SQL = """
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS mart;
CREATE SCHEMA IF NOT EXISTS semantic;
CREATE SCHEMA IF NOT EXISTS agent_ops;
"""


CREATE_AGENT_OPS_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS agent_ops.conversations (
    conversation_id UUID PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_ops.messages (
    message_id UUID PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES agent_ops.conversations(conversation_id),
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_ops.agent_runs (
    run_id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES agent_ops.conversations(conversation_id),
    user_question TEXT NOT NULL,
    interpreted_question TEXT,
    intent TEXT,
    status TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    latency_ms INTEGER
);

CREATE TABLE IF NOT EXISTS agent_ops.agent_steps (
    step_id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES agent_ops.agent_runs(run_id),
    node_name TEXT NOT NULL,
    input_summary TEXT,
    output_summary TEXT,
    status TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS agent_ops.generated_sql (
    sql_id UUID PRIMARY KEY,
    run_id UUID REFERENCES agent_ops.agent_runs(run_id),
    attempt_number INTEGER NOT NULL,
    generated_sql TEXT NOT NULL,
    validation_status TEXT,
    validation_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_ops.query_executions (
    execution_id UUID PRIMARY KEY,
    run_id UUID REFERENCES agent_ops.agent_runs(run_id),
    sql_id UUID REFERENCES agent_ops.generated_sql(sql_id),
    row_count INTEGER,
    execution_time_ms INTEGER,
    status TEXT NOT NULL,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_ops.chart_specs (
    chart_id UUID PRIMARY KEY,
    run_id UUID REFERENCES agent_ops.agent_runs(run_id),
    chart_type TEXT,
    chart_spec_json JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_ops.model_usage (
    usage_id UUID PRIMARY KEY,
    run_id UUID REFERENCES agent_ops.agent_runs(run_id),
    model_name TEXT NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    estimated_cost NUMERIC(12, 6),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_ops.errors (
    error_id UUID PRIMARY KEY,
    run_id UUID REFERENCES agent_ops.agent_runs(run_id),
    error_type TEXT NOT NULL,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_ops.feedback (
    feedback_id UUID PRIMARY KEY,
    run_id UUID REFERENCES agent_ops.agent_runs(run_id),
    rating INTEGER,
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


CREATE_SEMANTIC_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS semantic.metric_catalog (
    metric_id UUID PRIMARY KEY,
    metric_name TEXT NOT NULL UNIQUE,
    business_definition TEXT NOT NULL,
    sql_expression TEXT,
    grain TEXT,
    default_filters TEXT,
    required_tables TEXT[],
    caveats TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS semantic.table_catalog (
    table_id UUID PRIMARY KEY,
    schema_name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    business_description TEXT NOT NULL,
    grain TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(schema_name, table_name)
);

CREATE TABLE IF NOT EXISTS semantic.column_catalog (
    column_id UUID PRIMARY KEY,
    schema_name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    column_name TEXT NOT NULL,
    business_description TEXT NOT NULL,
    data_type TEXT,
    example_values TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(schema_name, table_name, column_name)
);

CREATE TABLE IF NOT EXISTS semantic.join_rules (
    join_rule_id UUID PRIMARY KEY,
    left_schema TEXT NOT NULL,
    left_table TEXT NOT NULL,
    left_column TEXT NOT NULL,
    right_schema TEXT NOT NULL,
    right_table TEXT NOT NULL,
    right_column TEXT NOT NULL,
    relationship_type TEXT,
    business_description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS semantic.business_glossary (
    glossary_id UUID PRIMARY KEY,
    term TEXT NOT NULL UNIQUE,
    definition TEXT NOT NULL,
    example TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


def setup_database(client: PostgresClient) -> None:
    client.execute_statement(CREATE_SCHEMAS_SQL)
    client.execute_statement(CREATE_AGENT_OPS_TABLES_SQL)
    client.execute_statement(CREATE_SEMANTIC_TABLES_SQL)