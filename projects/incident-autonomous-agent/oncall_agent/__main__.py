"""python -m oncall_agent demo / serve / seed-topology。"""

import argparse
import json
import tempfile

from .models import Decision, IncidentRequest, Settings
from .runtime import Runtime


def main():
    parser = argparse.ArgumentParser(description="晨光外送教學值班助理")
    parser.add_argument("command", choices=["demo", "serve", "seed-topology"])
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.command == "demo":
        # The scripted demo labels its own explicit approval; it is not an
        # production approval policy. API runs always wait for human input.
        with tempfile.TemporaryDirectory(prefix="oncall-demo-") as directory:
            runtime = Runtime(Settings(data_dir=directory))
            try:
                state = runtime.start(IncidentRequest())
                print("[DEMO] 調查完成，操作仍未執行：")
                print(json.dumps(state, ensure_ascii=False, indent=2))
                input("按 Enter 模擬人工核准；Ctrl-C 取消：")
                result = runtime.decide(
                    state["incident_id"],
                    Decision(
                        action_id=state["proposal"]["action_id"],
                        approved=True,
                        reviewer="demo-human",
                    ),
                )
                print(json.dumps(result, ensure_ascii=False, indent=2))
            finally:
                runtime.close()
    elif args.command == "serve":
        import uvicorn

        uvicorn.run(
            "oncall_agent.api:app", host="127.0.0.1", port=args.port, workers=1
        )
    else:
        from neo4j import GraphDatabase

        from .retrieval import ROOT

        settings = Settings.from_env()
        if not settings.neo4j_uri or not settings.neo4j_password:
            parser.error("請設定 ONCALL_NEO4J_URI 與 NEO4J_PASSWORD")
        edges = json.loads((ROOT / "data/topology.json").read_text())
        with GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        ) as driver:
            driver.execute_query(
                "UNWIND $edges AS edge "
                "MERGE (a:Service {name:edge[0]}) "
                "MERGE (b:Service {name:edge[1]}) "
                "MERGE (a)-[:DEPENDS_ON]->(b)",
                edges=edges,
            )
        print("已載入教學拓撲。")


if __name__ == "__main__":
    main()
