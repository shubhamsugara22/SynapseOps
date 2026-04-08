"""Read-only AlloyDB access layer using the AlloyDB Python connector."""

from __future__ import annotations

from typing import Any, Sequence

from app.config import Settings


class AlloyDBService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @staticmethod
    def _validate_read_only_sql(sql: str) -> str:
        normalized = sql.strip().rstrip(";")
        first_token = normalized.split(maxsplit=1)[0].lower() if normalized else ""
        if first_token not in {"select", "with"}:
            raise ValueError("Only read-only SELECT and WITH queries are allowed.")
        return normalized

    def is_configured(self) -> bool:
        return bool(self.settings.alloydb_instance and self.settings.alloydb_user)

    def run_query(
        self,
        sql: str,
        params: Sequence[Any] | None = None,
    ) -> list[dict[str, Any]]:
        if not self.is_configured():
            raise RuntimeError("AlloyDB is not configured. Set ALLOYDB_INSTANCE and ALLOYDB_USER.")

        validated_sql = self._validate_read_only_sql(sql)

        from google.cloud.alloydb.connector import Connector, IPTypes

        connector = Connector()
        ip_type = getattr(IPTypes, self.settings.alloydb_ip_type.upper(), IPTypes.PSC)

        connect_kwargs: dict[str, Any] = {
            "user": self.settings.alloydb_user,
            "db": self.settings.alloydb_database,
            "ip_type": ip_type,
            "enable_iam_auth": self.settings.alloydb_enable_iam_auth,
        }
        if self.settings.alloydb_password:
            connect_kwargs["password"] = self.settings.alloydb_password

        connection = connector.connect(
            self.settings.alloydb_instance,
            "pg8000",
            **connect_kwargs,
        )

        try:
            cursor = connection.cursor()
            cursor.execute(validated_sql, params or ())
            rows = cursor.fetchall()
            columns = [item[0] for item in cursor.description or []]
            return [dict(zip(columns, row)) for row in rows]
        finally:
            connection.close()
            connector.close()

    def run_default_query(self) -> list[dict[str, Any]]:
        return self.run_query(self.settings.alloydb_default_query)


def run_alloydb_sql_tool(sql: str) -> dict[str, Any]:
    settings = Settings.from_env()
    service = AlloyDBService(settings)
    return {
        "service": "alloydb",
        "rows": service.run_query(sql=sql),
    }
