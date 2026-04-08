"""Read-only BigQuery integration layer."""

from __future__ import annotations

from typing import Any

from app.config import Settings


class BigQueryService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @staticmethod
    def _validate_read_only_sql(sql: str) -> str:
        normalized = sql.strip().rstrip(";")
        first_token = normalized.split(maxsplit=1)[0].lower() if normalized else ""
        if first_token not in {"select", "with"}:
            raise ValueError("Only read-only SELECT and WITH queries are allowed.")
        return normalized

    def run_query(self, sql: str, limit: int = 20) -> list[dict[str, Any]]:
        validated_sql = self._validate_read_only_sql(sql)

        from google.cloud import bigquery

        client = bigquery.Client(
            project=self.settings.bigquery_project or self.settings.google_cloud_project or None,
        )
        query_job = client.query(validated_sql, location=self.settings.bigquery_location)
        rows = query_job.result(max_results=limit)

        return [
            {column: row[column] for column in row.keys()}
            for row in rows
        ]

    def run_default_query(self, limit: int = 10) -> list[dict[str, Any]]:
        return self.run_query(self.settings.bigquery_default_query, limit=limit)


def run_bigquery_sql_tool(sql: str, limit: int = 20) -> dict[str, Any]:
    settings = Settings.from_env()
    service = BigQueryService(settings)
    return {
        "service": "bigquery",
        "rows": service.run_query(sql=sql, limit=limit),
        "row_count": limit,
    }
