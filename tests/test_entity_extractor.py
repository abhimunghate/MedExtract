from nlp.entity_extractor import MedicalEntityExtractor


def test_symptom_extraction():
    extractor = MedicalEntityExtractor()

    entities = extractor.extract(
        "The patient has fever."
    )

    assert any(
        entity["text"].lower() == "fever"
        and entity["label"] == "SYMPTOM"
        for entity in entities
    )


def test_medicine_extraction():
    extractor = MedicalEntityExtractor()

    entities = extractor.extract(
        "The patient was prescribed Paracetamol."
    )

    assert any(
        entity["text"].lower() == "paracetamol"
        and entity["label"] == "MEDICINE"
        for entity in entities
    )