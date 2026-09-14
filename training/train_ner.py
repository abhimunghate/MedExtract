import json
import random
from pathlib import Path

import spacy
from spacy.training import Example
from spacy.util import minibatch


BASE_DIR = Path(__file__).resolve().parent.parent

TRAINING_FILE = (
    BASE_DIR / "data" / "ner_training_data.json"
)

MODEL_DIR = (
    BASE_DIR / "models" / "medical_ner"
)


def load_data():

    with open(
        TRAINING_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def create_examples(nlp, data):

    examples = []


    for item in data:

        doc = nlp.make_doc(
            item["text"]
        )


        entities = []


        for entity in item["entities"]:

            entities.append(
                (
                    entity["start"],
                    entity["end"],
                    entity["label"]
                )
            )


        example = Example.from_dict(
            doc,
            {
                "entities": entities
            }
        )


        examples.append(example)


    return examples


def train():

    print("Loading dataset...")

    data = load_data()


    print(
        f"Training examples: {len(data)}"
    )


    nlp = spacy.blank("en")


    ner = nlp.add_pipe("ner")


    labels = set()


    for item in data:

        for entity in item["entities"]:

            labels.add(
                entity["label"]
            )


    for label in sorted(labels):

        ner.add_label(label)


    examples = create_examples(
        nlp,
        data
    )


    optimizer = nlp.initialize(
        get_examples=lambda: examples
    )


    epochs = 40


    print("\nTraining model...\n")


    for epoch in range(epochs):

        random.shuffle(examples)

        losses = {}


        batches = minibatch(
            examples,
            size=4
        )


        for batch in batches:

            nlp.update(
                batch,
                drop=0.2,
                sgd=optimizer,
                losses=losses
            )


        print(
            f"Epoch {epoch + 1:02d}/{epochs} "
            f"Loss: {losses.get('ner', 0):.4f}"
        )


    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    nlp.to_disk(MODEL_DIR)


    print(
        "\nModel successfully saved."
    )

    print(
        f"Location: {MODEL_DIR}"
    )


if __name__ == "__main__":
    train()