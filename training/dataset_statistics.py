import json
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "ner_training_data.json"
)


def main():

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)


    label_counts = Counter()


    total_entities = 0


    for item in data:

        for entity in item["entities"]:

            label_counts[
                entity["label"]
            ] += 1

            total_entities += 1


    print(
        "\n========== DATASET STATISTICS =========="
    )

    print(
        f"Training examples: {len(data)}"
    )

    print(
        f"Total entities:    {total_entities}"
    )


    print("\nEntities by category:")


    for label, count in sorted(
        label_counts.items()
    ):

        print(
            f"{label:15} {count}"
        )


if __name__ == "__main__":
    main()