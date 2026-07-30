"""FastAPI surface for LUCERNA 65."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from backend.config import load_config
from backend.pdf_report import render_report_pdf
from backend.report import build_report
from backend.text_analysis import extract_facts
from backend.tree_engine import add_free_facts, answer_current, relocalize_state, response_payload, start_state

cfg = load_config()
app = FastAPI(title="LUCERNA 65 API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.allowed_origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": (
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'"
    ),
}


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    for key, value in SECURITY_HEADERS.items():
        response.headers.setdefault(key, value)
    return response


class StartRequest(BaseModel):
    profile: str = "health"
    locale: str = "ca"
    mode: str = "demo"


class AnswerRequest(BaseModel):
    state: dict
    answer_id: str
    note: str = Field(default="", max_length=1200)


class TextFactsRequest(BaseModel):
    text: str = Field(default="", max_length=6000)
    locale: str = "ca"


class AddFactsRequest(BaseModel):
    state: dict
    facts: list[str] = Field(default_factory=list)


class LocaleRequest(BaseModel):
    state: dict
    locale: str = "ca"


class ReportRequest(BaseModel):
    state: dict
    confirmed_facts: list[str] = Field(default_factory=list)


class AnalyzeRequest(BaseModel):
    text: str = Field(default="", max_length=6000)
    state: dict | None = None
    locale: str = "ca"


@app.get("/api/health")
def health():
    return {"ok": True, "name": "LUCERNA 65", "version": app.version}


@app.get("/api/capabilities")
def capabilities():
    return load_config().capabilities()


@app.get("/api/ai/status")
def ai_status():
    caps = load_config().capabilities()
    return {
        "enabled": caps["llm"]["enabled"],
        "mode": caps["mode"],
        "providers": caps["llm"]["providers"],
        "primaryProvider": caps["llm"]["primaryProvider"],
        "fallbackProviders": caps["llm"]["fallbackProviders"],
        "purpose": caps["llm"]["purpose"],
        "usesFor": ["free_text_fact_extraction"],
        "doesNotUseFor": ["attention_level", "indicator_rules", "question_routing", "final_decision"],
    }


@app.post("/api/session/start")
def session_start(payload: StartRequest):
    return response_payload(start_state(payload.profile, payload.locale, payload.mode))


@app.post("/api/session/answer")
def session_answer(payload: AnswerRequest):
    try:
        state = answer_current(payload.state, payload.answer_id, payload.note)
        return response_payload(state)
    except ValueError as exc:
        return JSONResponse(status_code=422, content={"error": str(exc)})


@app.post("/api/text/facts")
def text_facts(payload: TextFactsRequest):
    return extract_facts(payload.text, payload.locale)


@app.post("/api/ai/facts")
def ai_facts(payload: TextFactsRequest):
    return extract_facts(payload.text, payload.locale)


@app.post("/api/session/facts")
def session_facts(payload: AddFactsRequest):
    return response_payload(add_free_facts(payload.state, payload.facts))


@app.post("/api/session/locale")
def session_locale(payload: LocaleRequest):
    return response_payload(relocalize_state(payload.state, payload.locale))


@app.post("/api/report")
def report(payload: ReportRequest):
    return build_report(payload.state, payload.confirmed_facts)


@app.post("/api/report/pdf")
def report_pdf(payload: ReportRequest):
    report_data = build_report(payload.state, payload.confirmed_facts)
    session_id = str(report_data.get("session_id") or "report").replace("/", "-")
    filename = f"lucerna65-{session_id}.pdf"
    return Response(
        render_report_pdf(report_data, payload.state),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest):
    """Compatibility endpoint for the source project's API pattern."""
    if payload.state:
        return build_report(payload.state)
    return extract_facts(payload.text, payload.locale)
