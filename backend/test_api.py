from fastapi.testclient import TestClient

from api.analyze import app as fastapi_app


client = TestClient(fastapi_app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_fastapi_entrypoint_serves_frontend_assets():
    index = client.get("/")
    assert index.status_code == 200
    assert "LUCERNA 65" in index.text

    script = client.get("/app.js")
    assert script.status_code == 200
    assert "/api/session/start" in script.text


def test_ai_status_contract_does_not_expose_secrets():
    response = client.get("/api/ai/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["usesFor"] == ["free_text_fact_extraction"]
    assert "attention_level" in payload["doesNotUseFor"]
    serialized = str(payload).lower()
    assert "api_key" not in serialized
    assert "secret" not in serialized


def test_session_start_and_report():
    response = client.post("/api/session/start", json={"profile": "health", "locale": "ca"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["currentNode"]["id"] == "Q000"

    response = client.post(
        "/api/session/answer",
        json={"state": payload["state"], "answer_id": "yes", "note": ""},
    )
    assert response.status_code == 200
    state = response.json()["state"]

    report = client.post("/api/report", json={"state": state, "confirmed_facts": []})
    assert report.status_code == 200
    assert report.json()["attention"]["level"] == "urgent"

    pdf = client.post("/api/report/pdf", json={"state": state, "confirmed_facts": []})
    assert pdf.status_code == 200
    assert pdf.headers["content-type"] == "application/pdf"
    assert pdf.content.startswith(b"%PDF")
