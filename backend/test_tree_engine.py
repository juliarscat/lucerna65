from backend.report import build_report
from backend.tree_engine import answer_current, relocalize_state, start_state


def test_core_tree_starts_from_imported_json():
    state = start_state(profile="social", locale="ca", mode="demo")
    assert state["current_node_id"] == "Q000"
    state = answer_current(state, "no")
    assert state["current_node_id"] == "Q010"


def test_no_route_urgent_branch_continues_to_general_itinerary():
    state = start_state(profile="health", locale="ca", mode="demo")
    state = answer_current(state, "yes")
    assert state["current_node_id"] == "Q001"
    state = answer_current(state, "yes")
    assert state["current_node_id"] == "Q010"
    assert not state.get("complete")


def test_no_route_privacy_branch_returns_to_general_itinerary():
    state = start_state(profile="health", locale="ca", mode="demo")
    state = answer_current(state, "no")
    state = answer_current(state, "no")
    assert state["current_node_id"] == "Q011"
    state = answer_current(state, "yes")
    assert state["current_node_id"] == "Q012"
    state = answer_current(state, "yes")
    assert state["current_node_id"] == "Q020"
    assert not state.get("complete")


def test_no_private_setting_activates_privacy_indicator():
    state = start_state(profile="health", locale="ca", mode="demo")
    state = answer_current(state, "no")
    state = answer_current(state, "no")
    assert "privacy_denied" in state["indicator_ids"]
    assert state["current_node_id"] == "Q011"


def test_normalization_yes_activates_indicators():
    state = start_state(profile="health", locale="ca", mode="demo")
    state = answer_current(state, "no")
    state = answer_current(state, "yes")
    state = answer_current(state, "yes")
    assert "historical_normalization" in state["indicator_ids"]
    assert "duty_language" in state["indicator_ids"]


def test_report_contains_limitations_and_audit():
    state = start_state(profile="health", locale="ca", mode="demo")
    state = answer_current(state, "yes")
    report = build_report(state)
    assert report["audit"]["data_mode"] == "ephemeral"
    assert report["limitations"]
    assert report["mandatory_disclaimer"]


def test_english_locale_and_relocalize_existing_answers():
    state = start_state(profile="health", locale="en", mode="demo")
    assert state["locale"] == "en"
    state = answer_current(state, "yes")
    assert state["answered"][0]["answer_label"] == "Yes"
    state = relocalize_state(state, "es")
    assert state["answered"][0]["answer_label"] == "Sí"
    assert state["answered"][0]["question"].startswith("¿Hay algún indicio")
