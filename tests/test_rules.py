from nlp.rule_engine import MedicalRuleEngine


def test_dosage_extraction():
    engine = MedicalRuleEngine()

    entities = engine.extract_dosages(
        "Take Paracetamol 500 mg."
    )

    assert entities[0]["text"].lower() == "500 mg"


def test_frequency_extraction():
    engine = MedicalRuleEngine()

    entities = engine.extract_frequencies(
        "Take the medicine twice daily."
    )

    assert entities[0]["text"].lower() == "twice daily"


def test_duration_extraction():
    engine = MedicalRuleEngine()

    entities = engine.extract_durations(
        "Continue treatment for 5 days."
    )

    assert entities[0]["text"].lower() == "for 5 days"