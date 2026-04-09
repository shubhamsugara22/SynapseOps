"""Environment-driven application settings."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_int(value: str | None, default: int) -> int:
    if value is None or not value.strip():
        return default
    return int(value)


@dataclass(slots=True)
class Settings:
    app_name: str = "SynapseOps"
    app_env: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"

    google_cloud_project: str = ""
    google_cloud_location: str = "us-central1"
    google_genai_use_vertexai: bool = True
    google_api_key: str = ""
    adk_model: str = "gemini-2.5-flash"

    bigquery_project: str = ""
    bigquery_location: str = "US"
    bigquery_default_query: str = (
        "SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` "
        "WHERE state = 'CA' LIMIT 10"
    )

    alloydb_instance: str = ""
    alloydb_user: str = ""
    alloydb_password: str = ""
    alloydb_database: str = "postgres"
    alloydb_enable_iam_auth: bool = False
    alloydb_ip_type: str = "PSC"
    alloydb_default_query: str = "SELECT NOW() AS current_time"

    mcp_bigquery_toolbox_url: str = ""
    mcp_google_maps_url: str = ""
    mcp_bigquery_enabled: bool = True
    mcp_maps_enabled: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        resolved_port = _as_int(os.getenv("APP_PORT") or os.getenv("PORT"), cls.port)
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            app_env=os.getenv("APP_ENV", cls.app_env),
            host=os.getenv("APP_HOST", cls.host),
            port=resolved_port,
            log_level=os.getenv("APP_LOG_LEVEL", cls.log_level),
            google_cloud_project=os.getenv("GOOGLE_CLOUD_PROJECT", ""),
            google_cloud_location=os.getenv("GOOGLE_CLOUD_LOCATION", cls.google_cloud_location),
            google_genai_use_vertexai=_as_bool(
                os.getenv("GOOGLE_GENAI_USE_VERTEXAI"),
                cls.google_genai_use_vertexai,
            ),
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
            adk_model=os.getenv("ADK_MODEL", cls.adk_model),
            bigquery_project=os.getenv("BIGQUERY_PROJECT", ""),
            bigquery_location=os.getenv("BIGQUERY_LOCATION", cls.bigquery_location),
            bigquery_default_query=os.getenv(
                "BIGQUERY_DEFAULT_QUERY",
                cls.bigquery_default_query,
            ),
            alloydb_instance=os.getenv("ALLOYDB_INSTANCE", ""),
            alloydb_user=os.getenv("ALLOYDB_USER", ""),
            alloydb_password=os.getenv("ALLOYDB_PASSWORD", ""),
            alloydb_database=os.getenv("ALLOYDB_DATABASE", cls.alloydb_database),
            alloydb_enable_iam_auth=_as_bool(
                os.getenv("ALLOYDB_ENABLE_IAM_AUTH"),
                cls.alloydb_enable_iam_auth,
            ),
            alloydb_ip_type=os.getenv("ALLOYDB_IP_TYPE", cls.alloydb_ip_type),
            alloydb_default_query=os.getenv("ALLOYDB_DEFAULT_QUERY", cls.alloydb_default_query),
            mcp_bigquery_toolbox_url=os.getenv("MCP_BIGQUERY_TOOLBOX_URL", ""),
            mcp_google_maps_url=os.getenv("MCP_GOOGLE_MAPS_URL", ""),
            mcp_bigquery_enabled=_as_bool(
                os.getenv("MCP_BIGQUERY_ENABLED"),
                cls.mcp_bigquery_enabled,
            ),
            mcp_maps_enabled=_as_bool(
                os.getenv("MCP_MAPS_ENABLED"),
                cls.mcp_maps_enabled,
            ),
        )

    def has_google_auth(self) -> bool:
        return bool(self.google_cloud_project or self.google_api_key)

    def as_public_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["google_api_key"] = "configured" if self.google_api_key else ""
        data["alloydb_password"] = "configured" if self.alloydb_password else ""
        return data
