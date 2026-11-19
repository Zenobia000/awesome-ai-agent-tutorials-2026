"""唯一寫入路徑：調查 → 計畫 → 審批 → 執行 → 驗證。"""

from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from .models import RESTARTABLE, Decision, Diagnosis, RestartArgs


class IncidentInput(TypedDict):
    incident_id: str
    service: str
    question: str


class IncidentState(IncidentInput, total=False):
    status: str
    evidence: dict
    diagnosis: dict
    proposal: dict
    decision: dict
    receipt: dict
    verification: dict
    error: str
    timeline: list[dict]


def build_graph(tools, operations, checkpointer, harness=None, limit=40):
    def investigate(state):
        service = state["service"]
        jobs = {
            "metrics": lambda: tools.metrics(service),
            "logs": lambda: tools.logs(service),
            "runbooks": lambda: tools.runbooks.search(
                service + " " + state["question"]
            ),
            "topology": lambda: tools.topology.lookup(service),
            "orders": lambda: tools.query(
                "SELECT status, COUNT(*) AS count FROM orders GROUP BY status"
            ),
        }
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {key: pool.submit(job) for key, job in jobs.items()}
            evidence = {
                key: future.result() for key, future in futures.items()
            }
        if harness:
            diagnosis = harness.investigate(
                state["incident_id"],
                service,
                state["question"],
                evidence,
                limit,
            )
        else:
            unhealthy = evidence["metrics"]["state"] != "healthy"
            diagnosis = Diagnosis(
                summary=(
                    f"{service} 已降級，需處理。"
                    if unhealthy
                    else f"{service} 目前健康，不需重啟。"
                ),
                evidence=[
                    f"p95={evidence['metrics']['p95_ms']}ms; "
                    f"error_rate={evidence['metrics']['error_rate']}",
                    *[row["message"] for row in evidence["logs"]],
                    *[hit["source"] for hit in evidence["runbooks"]["hits"]],
                ][:12],
                action=(
                    "restart"
                    if unhealthy and service in RESTARTABLE
                    else "none"
                ),
                target=service,
                rationale="依教學 runbook 提出建議；須由人審批。",
            )
        return {
            "status": "investigated",
            "evidence": evidence,
            "diagnosis": diagnosis.model_dump(),
            "timeline": [
                {
                    "step": "investigate",
                    "mode": (
                        "live-deepagents" if harness else "deterministic-demo"
                    ),
                }
            ],
        }

    def plan(state):
        diagnosis = Diagnosis.model_validate(state["diagnosis"])
        service = state["service"]
        if diagnosis.target != service:
            return {"status": "blocked", "error": "建議目標與調查服務不符"}
        if service not in RESTARTABLE:
            return {
                "status": "manual_review",
                "error": "服務不在白名單；僅提供調查結果",
            }
        if (
            diagnosis.action == "none"
            or state["evidence"]["metrics"]["state"] == "healthy"
        ):
            return {"status": "resolved", "proposal": {}}
        proposal = RestartArgs(
            service=service,
            action_id=state["incident_id"],
            expected_revision=state["evidence"]["metrics"]["revision"],
        ).model_dump()
        return {
            "status": "awaiting_approval",
            "proposal": proposal,
            "timeline": state["timeline"] + [{"step": "plan"}],
        }

    def approve(state):
        decision = Decision.model_validate(
            interrupt(
                {
                    "type": "restart_approval",
                    "proposal": state["proposal"],
                    "summary": state["diagnosis"]["summary"],
                    "message": "只會修改教學模擬服務；請人工核准或拒絕。",
                }
            )
        )
        if decision.action_id != state["proposal"]["action_id"]:
            raise ValueError("審批與操作識別碼不符")
        return {
            "decision": decision.model_dump(),
            "status": "approved" if decision.approved else "denied",
            "timeline": state["timeline"]
            + [
                {
                    "step": "approve",
                    "reviewer": decision.reviewer,
                    "approved": decision.approved,
                }
            ],
        }

    def execute(state):
        decision = Decision.model_validate(state["decision"])
        proposal = RestartArgs.model_validate(state["proposal"])
        if not decision.approved or decision.action_id != proposal.action_id:
            raise ValueError("缺少有效人工核准")
        try:
            receipt = operations.restart(proposal)
        except (ValueError, RuntimeError) as exc:
            return {"status": "execution_failed", "error": str(exc)}
        return {
            "status": "executed",
            "receipt": receipt,
            "timeline": state["timeline"] + [{"step": "execute", **receipt}],
        }

    def verify(state):
        try:
            metrics = tools.metrics(state["service"])
            success = (
                metrics["state"] == "healthy"
                and metrics["p95_ms"] < 1000
                and metrics["error_rate"] < 0.05
            )
            verification = {"passed": success, "metrics": metrics}
        except Exception as exc:
            success = False
            verification = {"passed": False, "error": type(exc).__name__}
        return {
            "status": "verified" if success else "verification_failed",
            "verification": verification,
            "timeline": state["timeline"]
            + [{"step": "verify", "passed": success}],
        }

    graph = StateGraph(IncidentState, input_schema=IncidentInput)
    for name, node in [
        ("investigate", investigate),
        ("plan", plan),
        ("approve", approve),
        ("execute", execute),
        ("verify", verify),
    ]:
        graph.add_node(name, node)
    graph.add_edge(START, "investigate")
    graph.add_edge("investigate", "plan")
    graph.add_conditional_edges(
        "plan",
        lambda s: "approve" if s["status"] == "awaiting_approval" else END,
    )
    graph.add_conditional_edges(
        "approve", lambda s: "execute" if s["status"] == "approved" else END
    )
    graph.add_conditional_edges(
        "execute", lambda s: "verify" if s["status"] == "executed" else END
    )
    graph.add_edge("verify", END)
    return graph.compile(checkpointer=checkpointer)
