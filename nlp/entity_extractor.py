
import pandas as pd
import spacy
from pathlib import Path

from .rule_engine import MedicalRuleEngine
from .ner_model import MedicalNERModel


class MedicalEntityExtractor:
    """Hybrid medical entity extraction system."""

    def __init__(self, data_directory="data"):
        self.data_directory = Path(data_directory)

        # Load spaCy language model
        self.nlp = spacy.load("en_core_web_sm")

        # Initialize rule engine
        self.rule_engine = MedicalRuleEngine()

        # Initialize trained NER model
        self.ner_model = MedicalNERModel()

        # Load medical dictionaries
        self.symptoms = self._load_terms(
            "symptoms.csv", "term"
        )

        self.medicines = self._load_terms(
            "medicines.csv", "medicine"
        )

        self.diseases = self._load_terms(
            "diseases.csv", "disease"
        )

        self.medical_terms = self._load_terms(
            "medical_terms.csv", "term"
        )

        # Initialize PhraseMatcher
        self.matcher = spacy.matcher.PhraseMatcher(
            self.nlp.vocab,
            attr="LOWER"
        )

        self._build_matcher()

    def _load_terms(self, filename, column):
        """Load medical terms from a CSV file."""

        file_path = self.data_directory / filename

        dataframe = pd.read_csv(file_path)

        return (
            dataframe[column]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .unique()
            .tolist()
        )

    def _build_matcher(self):
        """Create phrase-matching patterns."""

        symptom_patterns = [
            self.nlp.make_doc(term)
            for term in self.symptoms
        ]

        medicine_patterns = [
            self.nlp.make_doc(term)
            for term in self.medicines
        ]

        disease_patterns = [
            self.nlp.make_doc(term)
            for term in self.diseases
        ]

        medical_term_patterns = [
            self.nlp.make_doc(term)
            for term in self.medical_terms
        ]

        self.matcher.add(
            "SYMPTOM",
            symptom_patterns
        )

        self.matcher.add(
            "MEDICINE",
            medicine_patterns
        )

        self.matcher.add(
            "DISEASE",
            disease_patterns
        )

        self.matcher.add(
            "MEDICAL_TERM",
            medical_term_patterns
        )

    def extract(self, text):
        """Extract medical entities using NER, dictionaries, and rules."""

        # Phase 5: Machine learning NER extraction
        ner_entities = self.ner_model.extract(text)

        # Phase 2: Dictionary extraction
        dictionary_entities = self.extract_dictionary_entities(text)

        # Phase 2: Rule-based extraction
        rule_entities = self.extract_rule_entities(text)

        # Combine all extraction results
        all_entities = (
            ner_entities
            + dictionary_entities
            + rule_entities
        )

        # Remove duplicate and overlapping entities
        return self.resolve_overlaps(all_entities)

    def extract_dictionary_entities(self, text):
        """Extract entities using medical dictionaries."""

        doc = self.nlp(text)

        entities = []

        matches = self.matcher(doc)

        for match_id, start, end in matches:

            span = doc[start:end]

            entities.append({
                "text": span.text,
                "label": self.nlp.vocab.strings[match_id],
                "start": span.start_char,
                "end": span.end_char
            })

        return entities

    def extract_rule_entities(self, text):
        """Extract entities using the medical rule engine."""

        return self.rule_engine.extract_all(text)

    @staticmethod
    def resolve_overlaps(entities):
        """Remove duplicate or overlapping entities."""

        entities = sorted(
            entities,
            key=lambda entity: (
                entity["start"],
                -(entity["end"] - entity["start"])
            )
        )

        selected = []

        for entity in entities:

            overlap = False

            for existing in selected:

                if (
                    entity["start"] < existing["end"]
                    and entity["end"] > existing["start"]
                ):
                    overlap = True
                    break

            if not overlap:
                selected.append(entity)

        return sorted(
            selected,
            key=lambda entity: entity["start"]
        )