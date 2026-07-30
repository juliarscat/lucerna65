from backend.text_analysis import _literal_spans


def test_literal_spans_reject_reformulated_subjects():
    source = (
        "La dona explica que la seva filla controla la targeta bancària "
        "i que no pot parlar sola durant les visites."
    )
    values = [
        "La filla no pot parlar sola durant les visites",
        "no pot parlar sola durant les visites",
    ]

    assert _literal_spans(values, source) == ["no pot parlar sola durant les visites"]
