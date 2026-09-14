import json
from pathlib import Path

import spacy


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = (
    BASE_DIR / "models" / "medical_ner"
)

EVALUATION_FILE = (
    BASE_DIR / "data" / "ner_evaluation_data.json"
)


def load_data():

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def analyze_errors():

    nlp = spacy.load(
        MODEL_DIR
    )

    data = load_data()


    for index, item in enumerate(data):

        text = item["text"]

        doc = nlp(text)


        actual = {
            (
                entity["start"],
                entity["end"],
                entity["label"]
            )
            for entity in item["entities"]
        }


        predicted = {
            (
                entity.start_char,
                entity.end_char,
                entity.label_
            )
            for entity in doc.ents
        }


        false_positives = (
            predicted - actual
        )

        false_negatives = (
            actual - predicted
        )


        if false_positives:

            print("\nFALSE POSITIVE")

            print(f"Text: {text}")

            for start, end, label in false_positives:

                print(
                    f"Predicted: "
                    f"{text[start:end]} "
                    f"({label})"
                )


        if false_negatives:

            print("\nFALSE NEGATIVE")

            print(f"Text: {text}")

            for start, end, label in false_negatives:

                print(
                    f"Missed: "
                    f"{text[start:end]} "
                    f"({label})"
                )


if __name__ == "__main__":
    analyze_errors()