from nlp import MedicalEntityExtractor


def main():
    extractor = MedicalEntityExtractor()

    text = """
    The patient has been experiencing high fever, severe headache,
    cough and fatigue for three days. The patient also reports
    shortness of breath.

    The doctor diagnosed the patient with influenza and prescribed
    Paracetamol 500 mg twice daily for five days.

    The patient was advised to monitor blood pressure and heart rate.
    """

    entities = extractor.extract(text)

    print("\nExtracted Medical Entities")
    print("=" * 50)

    for entity in entities:
        print(
            f"{entity['text']:25} "
            f"→ {entity['label']}"
        )


if __name__ == "__main__":
    main()