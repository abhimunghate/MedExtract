import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR / "data" / "ner_training_data.json"
)


def validate_entity(text, entity):

    start = entity["start"]
    end = entity["end"]

    if start < 0:
        return False, "Start position is negative."

    if end > len(text):
        return False, "End position exceeds text length."

    if start >= end:
        return False, "Start must be smaller than end."

    extracted_text = text[start:end]

    if not extracted_text.strip():
        return False, "Entity contains only whitespace."

    return True, extracted_text


def validate_dataset():

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        dataset = json.load(file)


    errors = 0


    for index, item in enumerate(dataset):

        text = item.get("text", "")

        if not text:

            print(
                f"[ERROR] Example {index}: "
                "empty text"
            )

            errors += 1

            continue


        for entity in item.get("entities", []):

            valid, message = validate_entity(
                text,
                entity
            )


            if not valid:

                print(
                    f"[ERROR] Example {index}: "
                    f"{message}"
                )

                errors += 1

                continue


            extracted = text[
                entity["start"]:entity["end"]
            ]


            print(
                f"[OK] {entity['label']:15} "
                f"→ {extracted}"
            )


    print("\n-------------------------")

    if errors == 0:

        print(
            "Dataset validation successful."
        )

    else:

        print(
            f"Dataset contains {errors} error(s)."
        )


if __name__ == "__main__":
    validate_dataset()