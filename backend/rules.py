"""Deterministic rule evaluation for LUCERNA 65."""

from __future__ import annotations

from backend.content import localized, read_json

SEVERITY_ORDER = {
    "urgent": 5,
    "priority": 4,
    "high": 4,
    "scheduled": 3,
    "medium": 3,
    "preventive": 2,
    "exploratory": 1,
    "low": 0,
}

ATTENTION_LABELS = {
    "ca": {
        "urgent": "Atenció immediata orientativa",
        "priority": "Valoració prioritària orientativa",
        "scheduled": "Seguiment programable",
        "preventive": "Informació preventiva",
    },
    "es": {
        "urgent": "Atención inmediata orientativa",
        "priority": "Valoración prioritaria orientativa",
        "scheduled": "Seguimiento programable",
        "preventive": "Información preventiva",
    },
    "en": {
        "urgent": "Immediate attention, for orientation",
        "priority": "Priority professional review, for orientation",
        "scheduled": "Scheduled follow-up",
        "preventive": "Preventive information",
    },
}


def load_knowledge() -> dict:
    return {
        "indicators": read_json("ontology/indicators.json"),
        "rules": read_json("ontology/rules.json"),
        "actions": read_json("actions.json"),
        "sources": read_json("ontology/sources.json"),
        "resources": read_json("resources/barcelona.json"),
    }


def evaluate_state(state: dict) -> dict:
    locale = state.get("locale", "ca")
    knowledge = load_knowledge()
    indicator_map = {item["id"]: item for item in knowledge["indicators"]}
    indicators = [
        _localize_indicator(indicator_map[indicator_id], locale)
        for indicator_id in state.get("indicator_ids", [])
        if indicator_id in indicator_map
    ]
    rule_hits = _rule_hits(state, indicators, knowledge)
    attention = _attention(indicators, state.get("actions", []), rule_hits, locale)
    recommendations = _recommendations(state, indicators, attention, knowledge, locale, rule_hits)
    source_ids = sorted({
        source_id
        for indicator in indicators
        for source_id in indicator.get("source_ids", [])
    } | {
        source_id
        for recommendation in recommendations
        for source_id in recommendation.get("source_ids", [])
    })
    return {
        "attention": attention,
        "indicators": indicators,
        "recommendations": recommendations,
        "resources": _resources(attention, knowledge, locale),
        "source_ids": source_ids,
        "sources": [_localize_source(item, locale) for item in knowledge["sources"] if item["id"] in source_ids],
        "domains_explored": sorted({record.get("domain", "context") for record in state.get("answered", [])}),
        "pending_questions": _pending_questions(state, indicators, locale),
        "limitations": _limitations(locale),
        "rule_hits": rule_hits,
    }


def _attention(indicators: list[dict], actions: list[str], rule_hits: list[dict], locale: str) -> dict:
    levels = [hit["attention_level"] for hit in rule_hits if hit.get("attention_level")]
    if any(str(action).startswith("ACTION_URGENT") for action in actions):
        levels.append("urgent")
    for indicator in indicators:
        severity = indicator.get("severity", "medium")
        if severity == "urgent":
            levels.append("urgent")
        elif severity == "high":
            levels.append("priority")
        elif severity == "medium":
            levels.append("scheduled")
    level = max(levels or ["preventive"], key=lambda item: SEVERITY_ORDER.get(item, 0))
    labels = ATTENTION_LABELS.get(locale, ATTENTION_LABELS["ca"])
    return {
        "level": level,
        "label": labels.get(level, labels["preventive"]),
        "rank": SEVERITY_ORDER.get(level, 1),
    }


def _recommendations(state: dict, indicators: list[dict], attention: dict, knowledge: dict,
                     locale: str, rule_hits: list[dict]) -> list[dict]:
    action_ids = list(state.get("actions", []))
    for hit in rule_hits:
        action = hit.get("action")
        if action and action not in action_ids:
            action_ids.append(action)
    if not action_ids and indicators:
        action_ids.append("ACTION_GENERATE_REPORT")
    action_map = {item["id"]: item for item in knowledge.get("actions", [])}
    out = []
    for action_id in action_ids:
        item = action_map.get(action_id)
        if not item:
            continue
        instructions = item.get(f"instructions_{locale}") or item.get("instructions", [])
        rationale = " ".join(instructions[:2])
        out.append({
            "id": item["id"],
            "priority": _action_priority(item),
            "text": localized(item, "label", locale, item.get("label", item["id"])),
            "rationale": rationale,
            "instructions": instructions,
            "source_ids": _source_ids_for_action(item["id"]),
        })
    return sorted(out, key=lambda r: -SEVERITY_ORDER.get(r["priority"], 0))[:10]


def _rule_hits(state: dict, indicators: list[dict], knowledge: dict) -> list[dict]:
    indicator_ids = {item["id"] for item in indicators}
    hits = []
    for rule in knowledge.get("rules", {}).get("rules", []):
        when = rule.get("when", {})
        any_ids = set(when.get("any_indicator", []))
        all_ids = set(when.get("all_indicators", []))
        if any_ids and not any_ids.intersection(indicator_ids):
            continue
        if all_ids and not all_ids.issubset(indicator_ids):
            continue
        # Context fields not present in the demo state are treated as soft gates:
        # they should not block a prototype recommendation, but the explanation
        # remains visible for professional review.
        then = rule.get("then", {})
        hits.append({
            "id": rule.get("id"),
            "attention_level": then.get("attention_level"),
            "action": then.get("action"),
            "report_flag": then.get("report_flag"),
            "explanation": rule.get("explanation", ""),
        })
    return hits


def _action_priority(item: dict) -> str:
    category = item.get("category")
    if category == "urgent":
        return "urgent"
    if category == "priority":
        return "priority"
    if category == "scheduled":
        return "scheduled"
    return "preventive"


def _source_ids_for_action(action_id: str) -> list[str]:
    if "HEALTH" in action_id:
        return ["SRC_CAT_SALUT_VM", "SRC_CAT_DONES_GRANS"]
    if "LEGAL" in action_id:
        return ["SRC_CAT_DONES_GRANS", "SRC_GDPR"]
    if "URGENT" in action_id or "SPECIALIST" in action_id:
        return ["SRC_CAT_PROTOCOL_MARC_2022"]
    return ["SRC_CAT_DONES_GRANS"]


def _pending_questions(state: dict, indicators: list[dict], locale: str) -> list[str]:
    pending = []
    if not state.get("answers", {}).get("Q010"):
        pending.append({
            "ca": "Confirmar si l'entrevista es pot fer en condicions de privacitat.",
            "es": "Confirmar si la entrevista puede hacerse en condiciones de privacidad.",
            "en": "Confirm whether the interview can take place in private conditions.",
        }.get(locale, "Confirmar si l'entrevista es pot fer en condicions de privacitat."))
    for indicator in indicators:
        pending.extend(indicator.get("follow_up", [])[:2])
    return list(dict.fromkeys(pending))[:10]


def _resources(attention: dict, knowledge: dict, locale: str) -> list[dict]:
    result = []
    for item in knowledge["resources"]:
        min_attention = item.get("min_attention")
        if min_attention == "medium":
            min_attention = "scheduled"
        elif min_attention == "high":
            min_attention = "priority"
        if min_attention and SEVERITY_ORDER[attention["level"]] < SEVERITY_ORDER[min_attention]:
            continue
        result.append({
            "id": item["id"],
            "name": localized(item, "name", locale),
            "description": localized(item, "description", locale),
            "territory": item.get("territory", "Barcelona"),
            "verification_status": item.get("verification_status", "pending"),
            "source_ids": item.get("source_ids", []),
        })
    return result[:6]


def _limitations(locale: str) -> list[str]:
    if locale == "es":
        return [
            "Resultado orientativo: no es un diagnóstico, peritaje, denuncia ni resolución.",
            "Las decisiones corresponden siempre a la profesional y al circuito del servicio.",
            "No se han guardado datos personales en el servidor en este modo demo.",
            "Las fuentes y recursos territoriales deben verificarse antes de usar casos reales.",
        ]
    if locale == "en":
        return [
            "The result is for orientation only: it is not a diagnosis, expert opinion, complaint or administrative decision.",
            "Decisions always belong to the professional and the service pathway.",
            "No personal data has been stored on the server in this demo mode.",
            "Territorial sources and resources must be verified before use in real cases.",
        ]
    return [
        "Resultat orientatiu: no és un diagnòstic, peritatge, denúncia ni resolució.",
        "Les decisions corresponen sempre a la professional i al circuit del servei.",
        "No s'han guardat dades personals al servidor en aquest mode demo.",
        "Les fonts i recursos territorials s'han de verificar abans d'usar casos reals.",
    ]


def _localize_indicator(item: dict, locale: str) -> dict:
    return {
        "id": item["id"],
        "domain": item.get("domain", "context"),
        "severity": item.get("severity", "medium"),
        "label": localized(item, "label", locale),
        "rationale": localized(item, "rationale", locale),
        "source_ids": item.get("source_ids", []),
        "follow_up": item.get(f"follow_up_{locale}", item.get("follow_up_ca", [])),
    }


def _localize_source(item: dict, locale: str) -> dict:
    return {
        "id": item["id"],
        "organism": item.get("organism", ""),
        "title": localized(item, "title", locale),
        "version": item.get("version", ""),
        "status": item.get("status", "placeholder"),
        "url": item.get("url", ""),
    }
