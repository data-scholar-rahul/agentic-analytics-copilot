#!/usr/bin/env bash
set -e

DB_NAME="analytics_agent"

echo "Seeding semantic catalog..."
psql -d "$DB_NAME" -f backend/sql/003_seed_semantic_catalog.sql

echo "Semantic catalog counts:"
psql -d "$DB_NAME" -c "
SELECT 'semantic.metric_catalog' AS table_name, COUNT(*) FROM semantic.metric_catalog
UNION ALL
SELECT 'semantic.table_catalog', COUNT(*) FROM semantic.table_catalog
UNION ALL
SELECT 'semantic.join_rules', COUNT(*) FROM semantic.join_rules
UNION ALL
SELECT 'semantic.business_glossary', COUNT(*) FROM semantic.business_glossary
ORDER BY table_name;
"