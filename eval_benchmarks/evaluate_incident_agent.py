"""免模型回歸評估：驗證行為與檢索，不代表真實事故修復成功率。"""

import argparse
import json
import platform
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "projects/incident-autonomous-agent"))

from oncall_agent.models import (  # noqa: E402
    Decision,
    IncidentRequest,
    Settings,
)
from oncall_agent.retrieval import Runbooks  # noqa: E402
from oncall_agent.runtime import Runtime  # noqa: E402


def evaluate():
    cases = json.loads(
        (Path(__file__).parent / "incident_cases.json").read_text()
    )
    results = []
    started = time.perf_counter()
    for case in cases["incidents"]:
        with tempfile.TemporaryDirectory(prefix="incident-eval-") as directory:
            runtime = Runtime(Settings(data_dir=directory))
            try:
                if not case.get("recover", True):
                    with runtime.operations.connect() as conn:
                        conn.execute(
                            "UPDATE services SET recover_on_restart=0"
                        )
                state = runtime.start(IncidentRequest(service=case["service"]))
                writes_before = runtime.operations.status(case["service"])[
                    "restart_count"
                ]
                if state["pending"]:
                    state = runtime.decide(
                        state["incident_id"],
                        Decision(
                            action_id=state["proposal"]["action_id"],
                            approved=case["approve"],
                            reviewer="benchmark-human",
                        ),
                    )
                writes = runtime.operations.status(case["service"])[
                    "restart_count"
                ]
                results.append(
                    {
                        "name": case["name"],
                        "status": state["status"],
                        "writes_before_approval": writes_before,
                        "writes": writes,
                        "passed": (
                            state["status"] == case["expected_status"]
                            and writes == case["expected_writes"]
                            and writes_before == 0
                        ),
                    }
                )
            finally:
                runtime.close()
    runbooks = Runbooks(Settings())
    retrieval = []
    for case in cases["retrieval"]:
        hits = runbooks.search(case["query"])["hits"]
        rank = next(
            (
                i
                for i, hit in enumerate(hits, 1)
                if hit["source"] == case["source"]
            ),
            None,
        )
        retrieval.append(
            {"query": case["query"], "expected": case["source"], "rank": rank}
        )
    return {
        "mode": cases["mode"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "scope": "六個固定教學情境與四筆檢索；不代表模型或線上事故表現",
        "metrics": {
            "scenario_pass_rate": sum(r["passed"] for r in results)
            / len(results),
            "writes_before_approval": sum(
                r["writes_before_approval"] for r in results
            ),
            "retrieval_hit_at_3": sum(r["rank"] is not None for r in retrieval)
            / len(retrieval),
            "retrieval_mrr_at_3": sum(
                1 / r["rank"] if r["rank"] else 0 for r in retrieval
            )
            / len(retrieval),
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        "incidents": results,
        "retrieval": retrieval,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate()
    content = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content + "\n")
    print(content)
    if report["metrics"]["scenario_pass_rate"] < 1:
        sys.exit(1)
