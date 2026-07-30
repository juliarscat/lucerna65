"""Report assembly for LUCERNA 65."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.content import read_json
from backend.rules import evaluate_state

REPORT_COPY = {
    "ca": {
        "title": "LUCERNA 65 - Informe orientatiu revisable",
        "mandatory_disclaimer": "Resultat orientatiu subjecte a revisió humana.",
    },
    "es": {
        "title": "LUCERNA 65 - Informe orientativo revisable",
        "mandatory_disclaimer": "Resultado orientativo sujeto a revisión humana.",
    },
    "en": {
        "title": "LUCERNA 65 - Reviewable orientative report",
        "mandatory_disclaimer": "Orientative result subject to human review.",
    },
}


def build_report(state: dict, confirmed_facts: list[str] | None = None) -> dict:
    evaluation = evaluate_state(state)
    schema = _report_schema()
    locale = state.get("locale", "ca")
    copy = REPORT_COPY.get(locale, REPORT_COPY["ca"])
    facts = _facts_from_answers(state)
    for fact in confirmed_facts or state.get("free_facts", []):
        clean = " ".join(str(fact or "").split()).strip()
        if clean and clean not in facts:
            facts.append(clean[:600])
    return {
        "title": copy.get("title") or schema.get("title", "LUCERNA 65 - Informe orientatiu revisable"),
        "mandatory_disclaimer": copy.get("mandatory_disclaimer") or schema.get(
            "mandatory_disclaimer",
            "Resultat orientatiu subjecte a revisió humana.",
        ),
        "session_id": state.get("session_id"),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "locale": state.get("locale", "ca"),
        "profile": state.get("profile", "health"),
        "mode": state.get("mode", "demo"),
        "attention": evaluation["attention"],
        "domains_explored": evaluation["domains_explored"],
        "facts_confirmed": facts,
        "indicators": evaluation["indicators"],
        "pending_questions": evaluation["pending_questions"],
        "recommendations": evaluation["recommendations"],
        "resources": evaluation["resources"],
        "sources": evaluation["sources"],
        "limitations": evaluation["limitations"],
        "rule_hits": evaluation.get("rule_hits", []),
        "audit": {
            "tree_version": state.get("tree_version"),
            "data_mode": "ephemeral",
            "stores_sensitive_data": False,
            "answers_count": len(state.get("answered", [])),
            "human_review_required": True,
        },
    }


def _report_schema() -> dict:
    try:
        return read_json("ontology/report_schema.json")
    except Exception:  # noqa: BLE001
        return {}


def _facts_from_answers(state: dict) -> list[str]:
    out = []
    for record in state.get("answered", []):
        answer_id = record.get("answer_id")
        if answer_id in {"unknown", "skip"}:
            continue
        text = f"{record.get('question')}: {record.get('answer_label')}"
        if record.get("note"):
            text += f" ({record['note']})"
        out.append(text)
    return out
