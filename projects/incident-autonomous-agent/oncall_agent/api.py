"""本機 HTTP/SSE 入口；審批只接受明確的人類決策。"""

import hmac
import json
import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from .models import Decision, IncidentRequest, Settings
from .retrieval import ROOT
from .runtime import ConflictError, Runtime

logger = logging.getLogger(__name__)


def create_app(settings=None, runtime=None):
    settings = settings or Settings.from_env()

    @asynccontextmanager
    async def lifespan(app):
        app.state.runtime = runtime or Runtime(settings)
        try:
            yield
        finally:
            if runtime is None:
                app.state.runtime.close()

    app = FastAPI(title="晨光外送 · 值班助理", lifespan=lifespan)

    def authorize(authorization: str = Header(default="")):
        if settings.api_token and not hmac.compare_digest(
            authorization, f"Bearer {settings.api_token}"
        ):
            raise HTTPException(status_code=401, detail="需要有效 API Token")

    @app.exception_handler(ConflictError)
    async def conflict(request, exc):
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(KeyError)
    async def missing(request, exc):
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=404, content={"detail": "找不到事件"})

    @app.get("/")
    def index():
        return FileResponse(ROOT / "static/index.html")

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "mode": settings.mode,
            "checkpoint": settings.checkpoint,
            "simulation": True,
        }

    @app.post("/api/incidents", dependencies=[Depends(authorize)])
    def start(request: IncidentRequest):
        try:
            return app.state.runtime.start(request)
        except Exception as exc:
            logger.error("Investigation failed: %s", type(exc).__name__)
            raise HTTPException(
                503, "調查失敗，請檢查模型或 MCP 連線"
            ) from exc

    @app.post("/api/incidents/stream", dependencies=[Depends(authorize)])
    def stream(request: IncidentRequest):
        def events():
            try:
                for event in app.state.runtime.stream_new(request):
                    payload = json.dumps(event["data"], ensure_ascii=False)
                    yield (f"event: {event['event']}\ndata: {payload}\n\n")
            except Exception as exc:
                logger.error("Stream failed: %s", type(exc).__name__)
                yield (
                    "event: failure\n"
                    'data: {"message":"調查失敗，未授權寫入"}\n\n'
                )

        return StreamingResponse(
            events(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    @app.get("/api/incidents/{incident_id}", dependencies=[Depends(authorize)])
    def snapshot(incident_id: str):
        return app.state.runtime.snapshot(incident_id)

    @app.post(
        "/api/incidents/{incident_id}/decision",
        dependencies=[Depends(authorize)],
    )
    def decide(incident_id: str, decision: Decision):
        return app.state.runtime.decide(incident_id, decision)

    return app


app = create_app()
