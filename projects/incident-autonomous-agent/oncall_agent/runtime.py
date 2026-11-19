"""管理 checkpoint 生命週期；對同一事件串行處理決策。"""

from contextlib import ExitStack
from threading import Lock
from uuid import uuid4

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from .models import Decision, IncidentRequest, Settings
from .retrieval import Runbooks, Topology
from .storage import Operations
from .tools import ReadTools
from .workflow import build_graph


class ConflictError(ValueError):
    pass


class Runtime:
    def __init__(self, settings: Settings, checkpointer=None, harness=None):
        self.settings = settings
        self.resources = ExitStack()
        if settings.mode == "live" and not settings.api_token:
            raise ValueError("live 模式必須設定 ONCALL_API_TOKEN")
        if checkpointer is None and settings.checkpoint == "postgres":
            if not settings.database_url:
                raise ValueError("請設定 ONCALL_DATABASE_URL")
            from langgraph.checkpoint.postgres import PostgresSaver

            checkpointer = self.resources.enter_context(
                PostgresSaver.from_conn_string(settings.database_url)
            )
            checkpointer.setup()
        self.checkpointer = checkpointer or InMemorySaver()
        self.operations = Operations(settings.data_dir)
        self.tools = ReadTools(
            self.operations,
            Runbooks(settings),
            Topology(settings),
            use_mcp=settings.mode == "live",
        )
        if settings.mode == "live" and harness is None:
            from .harness import Harness

            harness = Harness(self.tools, self.checkpointer)
        self.graph = build_graph(
            self.tools,
            self.operations,
            self.checkpointer,
            harness,
            settings.recursion_limit,
        )
        # This teaching server intentionally uses one process/worker.
        self.lock = Lock()

    def config(self, incident_id):
        return {
            "configurable": {"thread_id": incident_id},
            "recursion_limit": self.settings.recursion_limit,
        }

    def snapshot(self, incident_id):
        state = self.graph.get_state(self.config(incident_id))
        if not state.values:
            raise KeyError("找不到事件")
        result = dict(state.values)
        result["pending"] = [
            item.value for task in state.tasks for item in task.interrupts
        ]
        return result

    def stream_new(self, request: IncidentRequest):
        incident_id = str(uuid4())
        with self.lock:
            yield {"event": "incident", "data": {"incident_id": incident_id}}
            for update in self.graph.stream(
                {"incident_id": incident_id, **request.model_dump()},
                self.config(incident_id),
                stream_mode="updates",
            ):
                for step in update:
                    if step != "__interrupt__":
                        yield {"event": "step", "data": {"step": step}}
            yield {"event": "state", "data": self.snapshot(incident_id)}

    def start(self, request):
        result = None
        for event in self.stream_new(request):
            if event["event"] == "state":
                result = event["data"]
        return result

    def decide(self, incident_id, decision: Decision):
        with self.lock:
            state = self.snapshot(incident_id)
            if not state["pending"] or state["status"] != "awaiting_approval":
                raise ConflictError("事件目前沒有待審操作")
            if decision.action_id != state["proposal"]["action_id"]:
                raise ConflictError("操作識別碼不符")
            self.graph.invoke(
                Command(resume=decision.model_dump()), self.config(incident_id)
            )
            return self.snapshot(incident_id)

    def close(self):
        self.resources.close()
