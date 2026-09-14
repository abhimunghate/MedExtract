import json
from collections import defaultdict
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


def calculate_metrics(
    true_entities,
    predicted_entities
):

    true_positive = len(
        true_entities & predicted_entities
    )

    false_positive = len(
        predicted_entities - true_entities
    )

    false_negative = len(
        true_entities - predicted_entities
    )


    if true_positive + false_positive:

        precision = (
            true_positive /
            (true_positive + false_positive)
        )

    else:

        precision = 0.0


    if true_positive + false_negative:

        recall = (
            true_positive /
            (true_positive + false_negative)
        )

    else:

        recall = 0.0


    if precision + recall:

        f1 = (
            2 * precision * recall /
            (precision + recall)
        )

    else:

        f1 = 0.0


    return (
        precision,
        recall,
        f1
    )


def evaluate():

    nlp = spacy.load(
        MODEL_DIR
    )

    data = load_data()


    overall_true = set()

    overall_predicted = set()


    per_label_true = defaultdict(set)

    per_label_predicted = defaultdict(set)


    for index, item in enumerate(data):

        text = item["text"]

        doc = nlp(text)


        for entity in item["entities"]:

            key = (
                index,
                entity["start"],
                entity["end"],
                entity["label"]
            )


            overall_true.add(key)

            per_label_true[
                entity["label"]
            ].add(key)


        for entity in doc.ents:

            key = (
                index,
                entity.start_char,
                entity.end_char,
                entity.label_
            )


            overall_predicted.add(key)

            per_label_predicted[
                entity.label_
            ].add(key)


    labels = sorted(
        set(per_label_true)
        |
        set(per_label_predicted)
    )


    print("\n==============================================")

    print(
        "        MEDICAL NER EVALUATION"
    )

    print("==============================================\n")


    print(
        f"{'Entity':15}"
        f"{'Precision':>12}"
        f"{'Recall':>12}"
        f"{'F1':>12}"
    )

    print("-" * 51)


    for label in labels:

        precision, recall, f1 = (
            calculate_metrics(
                per_label_true[label],
                per_label_predicted[label]
            )
        )


        print(
            f"{label:15}"
            f"{precision:>12.3f}"
            f"{recall:>12.3f}"
            f"{f1:>12.3f}"
        )


    print("-" * 51)


    precision, recall, f1 = (
        calculate_metrics(
            overall_true,
            overall_predicted
        )
    )


    print(
        f"{'OVERALL':15}"
        f"{precision:>12.3f}"
        f"{recall:>12.3f}"
        f"{f1:>12.3f}"
    )


    print("\n==============================================")


if __name__ == "__main__":
    evaluate()