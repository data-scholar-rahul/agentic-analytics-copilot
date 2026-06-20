from dataclasses import dataclass


@dataclass(frozen=True)
class MatchedIntent:
    intent_name: str
    sql: str
    answer_template: str


class IntentRouter:
    def match(self, question: str) -> MatchedIntent | None:
        normalized_question = question.lower().strip()
        
        if self._is_forecast_question(normalized_question):
            return None
        
        if self._is_order_count_by_status(normalized_question):
            return MatchedIntent(
                intent_name="order_count_by_status",
                sql="""
                SELECT
                    order_status,
                    COUNT(*) AS order_count
                FROM mart.orders
                GROUP BY order_status
                ORDER BY order_count DESC
                """,
                answer_template="Here is the order count by status.",
            )

        if self._is_revenue_by_month(normalized_question):
            return MatchedIntent(
                intent_name="revenue_by_month",
                sql="""
                SELECT
                    DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS revenue_month,
                    SUM(op.payment_value) AS revenue
                FROM mart.orders AS o
                JOIN mart.order_payments AS op
                    ON o.order_id = op.order_id
                WHERE o.order_status = 'delivered'
                GROUP BY revenue_month
                ORDER BY revenue_month
                """,
                answer_template="Here is revenue by month for delivered orders.",
            )

        if self._is_top_product_categories_by_revenue(normalized_question):
            return MatchedIntent(
                intent_name="top_product_categories_by_revenue",
                sql="""
                SELECT
                    COALESCE(pct.product_category_name_english, p.product_category_name) AS product_category,
                    SUM(op.payment_value) AS revenue
                FROM mart.orders AS o
                JOIN mart.order_payments AS op
                    ON o.order_id = op.order_id
                JOIN mart.order_items AS oi
                    ON o.order_id = oi.order_id
                JOIN mart.products AS p
                    ON oi.product_id = p.product_id
                LEFT JOIN mart.product_category_translation AS pct
                    ON p.product_category_name = pct.product_category_name
                WHERE o.order_status = 'delivered'
                GROUP BY product_category
                ORDER BY revenue DESC
                """,
                answer_template="Here are the top product categories by revenue.",
            )

        return None

    def _is_order_count_by_status(self, question: str) -> bool:
        return (
            "order" in question
            and "status" in question
            and ("count" in question or "number" in question)
        )

    def _is_revenue_by_month(self, question: str) -> bool:
        return (
            ("revenue" in question or "sales" in question)
            and ("month" in question or "monthly" in question)
        )

    def _is_top_product_categories_by_revenue(self, question: str) -> bool:
        return (
            ("top" in question or "highest" in question or "best" in question)
            and ("category" in question or "categories" in question)
            and ("revenue" in question or "sales" in question)
        )
    
    def _is_forecast_question(self, question: str) -> bool:
        return (
            "forecast" in question
            or "predict" in question
            or "projection" in question
            or "next month" in question
            or "future" in question
        )