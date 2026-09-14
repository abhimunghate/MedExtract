from pathlib import Path

import spacy


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR / "models" / "medical_ner"
)


class MedicalNERModel:

    def __init__(self):

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                "Trained medical NER model was not found. "
                "Run training/train_ner.py first."
            )

        self.nlp = spacy.load(
            MODEL_PATH
        )


    def extract(self, text):

        doc = self.nlp(text)

        entities = []


        for entity in doc.ents:

            entities.append({
                "text": entity.text,
                "label": entity.label_,
                "start": entity.start_char,
                "end": entity.end_char,
                "source": "NER"
            })


        return entities