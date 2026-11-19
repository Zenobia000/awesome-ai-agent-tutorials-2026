from fastapi.testclient import TestClient
from oncall_agent.api import create_app
from oncall_agent.models import Settings


def test_http_sse_approval_and_replay(runtime):
    app = create_app(runtime.settings, runtime)
    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        response = client.post("/api/incidents/stream", json={})
        assert response.status_code == 200
        assert "event: state" in response.text
        assert "awaiting_approval" in response.text
        import json

        states = [
            json.loads(block.split("data: ", 1)[1])
            for block in response.text.strip().split("\n\n")
            if block.startswith("event: state")
        ]
        state = states[0]
        identifier = state["incident_id"]
        assert client.get(f"/api/incidents/{identifier}").json()["pending"]
        decision = {
            "action_id": identifier,
            "approved": True,
            "reviewer": "api-test",
        }
        route = f"/api/incidents/{identifier}/decision"
        assert client.post(route, json=decision).json()["status"] == "verified"
        assert client.post(route, json=decision).status_code == 409
        assert client.get("/api/incidents/missing").status_code == 404


def test_bearer_token_and_input_validation(runtime):
    settings = Settings(api_token="test-only-token")
    with TestClient(create_app(settings, runtime)) as client:
        assert client.post("/api/incidents", json={}).status_code == 401
        headers = {"Authorization": "Bearer test-only-token"}
        assert (
            client.post(
                "/api/incidents",
                headers=headers,
                json={"service": "arbitrary"},
            ).status_code
            == 422
        )
        response = client.post("/api/incidents", headers=headers, json={})
        assert response.json()["status"] == "awaiting_approval"
