"""Adaptive, auditable question tree for LUCERNA 65."""

from __future__ import annotations

import secrets
from datetime import datetime, timezone
from typing import Any

from backend.content import locale_or_ca, localized, read_json

PROFILE_LABELS = {
    "health": {"ca": "Salut", "es": "Salud", "en": "Health"},
    "social": {"ca": "Serveis socials", "es": "Servicios sociales", "en": "Social services"},
    "psychology": {"ca": "Psicologia", "es": "Psicología", "en": "Psychology"},
    "care": {"ca": "Cures i residències", "es": "Cuidados y residencias", "en": "Care and residential services"},
    "legal": {"ca": "Àmbit jurídic", "es": "Ámbito jurídico", "en": "Legal field"},
    "community": {"ca": "Comunitari", "es": "Comunitario", "en": "Community"},
}


def load_tree(locale: str = "ca") -> dict:
    # One bilingual source keeps the audit trail stable; locale controls labels.
    _ = locale_or_ca(locale)
    return read_json("questions/ca/tree.json")


def node_index(tree: dict) -> dict[str, dict]:
    return {node["id"]: node for node in tree.get("nodes", [])}


def start_state(profile: str = "health", locale: str = "ca", mode: str = "demo") -> dict:
    locale = locale_or_ca(locale)
    tree = load_tree(locale)
    profile = profile if profile in PROFILE_LABELS else "health"
    pending = list(tree.get("entry_nodes") or [tree["start"]])
    state = {
        "session_id": f"demo-{secrets.token_urlsafe(6)}",
        "locale": locale,
        "profile": profile,
        "mode": mode if mode in {"demo", "interview", "review", "training"} else "demo",
        "tree_version": tree.get("version", "unknown"),
        "pending": pending,
        "answered": [],
        "answers": {},
        "indicator_ids": [],
        "actions": [],
        "free_facts": [],
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    state["current_node_id"] = _next_node_id(state, tree)
    return state


def public_node(node: dict | None, locale: str) -> dict | None:
    if not node:
        return None
    out = {
        "id": node["id"],
        "domain": node.get("domain", "context"),
        "priority": node.get("priority", "exploratory"),
        "question": localized(node, "question", locale),
        "help": localized(node, "help", locale),
        "why": localized(node, "why", locale),
        "source_ids": node.get("sources", []),
        "allows_note": bool(node.get("allows_note", True)),
        "answers": [],
    }
    for answer in node.get("answers", []):
        out["answers"].append({
            "id": answer["id"],
            "label": localized(answer, "label", locale),
            "tone": answer.get("tone", "neutral"),
        })
    return out


def current_node(state: dict) -> dict | None:
    tree = load_tree(state.get("locale", "ca"))
    return node_index(tree).get(state.get("current_node_id"))


def answer_current(state: dict, answer_id: str, note: str = "") -> dict:
    locale = locale_or_ca(state.get("locale", "ca"))
    tree = load_tree(locale)
    nodes = node_index(tree)
    current_id = state.get("current_node_id") or _next_node_id(state, tree)
    if not current_id:
        state["complete"] = True
        return state
    node = nodes[current_id]
    answer = _find_answer(node, answer_id)
    if answer is None:
        raise ValueError(f"Answer '{answer_id}' is not valid for node '{current_id}'")

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    record = {
        "node_id": current_id,
        "domain": node.get("domain", "context"),
        "priority": node.get("priority", "exploratory"),
        "question": localized(node, "question", locale),
        "answer_id": answer["id"],
        "answer_label": localized(answer, "label", locale),
        "note": (note or "").strip()[:1200],
        "source_ids": node.get("sources", []),
        "answered_at": now,
    }
    state.setdefault("answered", []).append(record)
    state.setdefault("answers", {})[current_id] = record
    state["pending"] = [item for item in state.get("pending", []) if item != current_id]
    _extend_unique(state.setdefault("indicator_ids", []), answer.get("activate_indicators", []))
    _extend_unique(state.setdefault("actions", []), answer.get("actions", []))

    queue = []
    if answer.get("next"):
        queue.append(answer["next"])
    queue.extend(answer.get("enqueue", []))
    if not queue:
        fallback_next = _fallback_next_after(current_id, state, tree)
        if fallback_next:
            queue.append(fallback_next)
    _prepend_pending(state, queue)

    state["updated_at"] = now
    state["current_node_id"] = _next_node_id(state, tree)
    state["complete"] = not bool(state["current_node_id"])
    return state


def add_free_facts(state: dict, facts: list[str]) -> dict:
    clean = []
    for fact in facts:
        value = " ".join(str(fact or "").split()).strip()
        if value and value not in clean:
            clean.append(value[:600])
    _extend_unique(state.setdefault("free_facts", []), clean)
    state["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return state


def relocalize_state(state: dict, locale: str) -> dict:
    """Switch visible labels in an existing session without changing its logic."""
    locale = locale_or_ca(locale)
    state["locale"] = locale
    tree = load_tree(locale)
    nodes = node_index(tree)
    relocalized_answers = {}
    for record in state.get("answered", []):
        node_id = record.get("node_id")
        node = nodes.get(node_id)
        if not node:
            continue
        answer = _find_answer(node, record.get("answer_id"))
        record["question"] = localized(node, "question", locale)
        if answer:
            record["answer_label"] = localized(answer, "label", locale)
        relocalized_answers[node_id] = record
    if isinstance(state.get("answers"), dict):
        for node_id, record in relocalized_answers.items():
            state["answers"][node_id] = record
    state["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return state


def progress(state: dict) -> dict:
    tree = load_tree(state.get("locale", "ca"))
    total = len(tree.get("entry_nodes", [])) + len({r["node_id"] for r in state.get("answered", []) if r.get("priority") != "branch"})
    answered = len(state.get("answered", []))
    domains = sorted({record.get("domain", "context") for record in state.get("answered", [])})
    return {
        "answered": answered,
        "pending": len(state.get("pending", [])),
        "domains": domains,
        "estimateMinutes": max(1, min(8, 2 + len(state.get("pending", [])) // 3)),
        "completionRatio": min(1, answered / max(1, total)),
    }


def response_payload(state: dict) -> dict:
    node = current_node(state)
    return {
        "state": state,
        "currentNode": public_node(node, state.get("locale", "ca")),
        "progress": progress(state),
    }


def _find_answer(node: dict, answer_id: str) -> dict | None:
    for answer in node.get("answers", []):
        if answer.get("id") == answer_id:
            return answer
    return None


def _next_node_id(state: dict, tree: dict) -> str | None:
    nodes = node_index(tree)
    answered = set(state.get("answers", {}).keys())
    profile = state.get("profile", "health")
    for node_id in state.get("pending", []):
        node = nodes.get(node_id)
        if not node or node_id in answered:
            continue
        profiles = set(node.get("profiles", []))
        if profiles and profile not in profiles:
            continue
        if not _condition_ok(node, state):
            continue
        return node_id
    return None


def _condition_ok(node: dict, state: dict) -> bool:
    requires = set(node.get("requires_indicators", []))
    if requires and not requires.intersection(state.get("indicator_ids", [])):
        return False
    excludes = set(node.get("exclude_if_indicators", []))
    if excludes and excludes.intersection(state.get("indicator_ids", [])):
        return False
    if node.get("requires_private_setting"):
        answer = state.get("answers", {}).get("safety_private_01", {})
        if answer.get("answer_id") == "no":
            return False
    return True


def _fallback_next_after(current_id: str, state: dict, tree: dict) -> str | None:
    """Continue the prototype itinerary when an answer has no explicit route."""
    nodes = tree.get("nodes", [])
    answered = set(state.get("answers", {}).keys())
    profile = state.get("profile", "health")
    try:
        current_index = next(index for index, node in enumerate(nodes) if node.get("id") == current_id)
    except StopIteration:
        return None

    for node in nodes[current_index + 1:]:
        node_id = node.get("id")
        if not node_id or node_id in answered:
            continue
        profiles = set(node.get("profiles", []))
        if profiles and profile not in profiles:
            continue
        if not _condition_ok(node, state):
            continue
        return str(node_id)
    return None


def _prepend_pending(state: dict, node_ids: list[Any]) -> None:
    pending = list(state.get("pending", []))
    answered = set(state.get("answers", {}).keys())
    clean = []
    for node_id in node_ids:
        if not node_id or node_id in answered or node_id in clean:
            continue
        clean.append(str(node_id))
    state["pending"] = clean + [item for item in pending if item not in clean]


def _extend_unique(target: list, values: list) -> None:
    for value in values or []:
        if value and value not in target:
            target.append(value)
