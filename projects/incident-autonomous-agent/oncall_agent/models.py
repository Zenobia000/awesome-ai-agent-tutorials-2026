"""HTTP、工具與模型回應共用的驗證邊界。"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool

Service = Literal["order-api", "order-db-proxy", "payment-api", "notification"]
RESTARTABLE = frozenset({"order-db-proxy", "notification"})


class Arguments(BaseModel):
    model_config = ConfigDict(extra="forbid")


class IncidentRequest(Arguments):
    service: Service = "order-db-proxy"
    question: str = Field(
        default="下單持續 502，請調查原因。", min_length=1, max_length=2000
    )


class ServiceArgs(Arguments):
    service: Service


class LogArgs(ServiceArgs):
    limit: int = Field(default=10, ge=1, le=50)


class SearchArgs(Arguments):
    query: str = Field(min_length=1, max_length=2000)
    limit: int = Field(default=3, ge=1, le=10)


class SQLArgs(Arguments):
    sql: str = Field(min_length=1, max_length=2000)


class Diagnosis(Arguments):
    summary: str = Field(min_length=1, max_length=4000)
    evidence: list[str] = Field(min_length=1, max_length=12)
    action: Literal["restart", "none"]
    target: Service
    rationale: str = Field(min_length=1, max_length=2000)


class Decision(Arguments):
    action_id: str = Field(min_length=1, max_length=64)
    approved: StrictBool
    reviewer: str = Field(min_length=1, max_length=100)
    comment: str = Field(default="", max_length=1000)


class RestartArgs(ServiceArgs):
    action_id: str = Field(min_length=1, max_length=64)
    expected_revision: int = Field(ge=0)


class Settings(BaseModel):
    mode: Literal["demo", "live"] = "demo"
    checkpoint: Literal["memory", "postgres"] = "memory"
    data_dir: str = ".oncall-data"
    database_url: str = ""
    api_token: str = ""
    neo4j_uri: str = ""
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""
    recursion_limit: int = Field(default=40, ge=10, le=100)

    @classmethod
    def from_env(cls):
        import os

        from dotenv import load_dotenv

        load_dotenv()
        return cls(
            mode=os.getenv("ONCALL_MODE", "demo"),
            checkpoint=os.getenv("ONCALL_CHECKPOINT", "memory"),
            data_dir=os.getenv("ONCALL_DATA_DIR", ".oncall-data"),
            database_url=os.getenv("ONCALL_DATABASE_URL", ""),
            api_token=os.getenv("ONCALL_API_TOKEN", ""),
            neo4j_uri=os.getenv("ONCALL_NEO4J_URI", ""),
            neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
            neo4j_password=os.getenv("NEO4J_PASSWORD", ""),
        )
