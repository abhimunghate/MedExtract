import re


class MedicalRuleEngine:
    """Extracts structured medical information using regular expressions."""

    DOSAGE_PATTERN = re.compile(
        r"\b\d+(?:\.\d+)?\s?(?:mg|mcg|g|kg|ml|mL|mg/mL|units?)\b",
        re.IGNORECASE
    )

    FREQUENCY_PATTERN = re.compile(
        r"\b(?:once|twice|thrice|one|two|three)\s+(?:daily|a day|per day)\b"
        r"|\b(?:daily|weekly|monthly)\b"
        r"|\b\d+\s+times?\s+(?:daily|a day|per day)\b",
        re.IGNORECASE
    )

    DURATION_PATTERN = re.compile(
        r"\b(?:for\s+)?\d+\s+(?:day|days|week|weeks|month|months|year|years)\b",
        re.IGNORECASE
    )

    def extract_dosages(self, text):
        """Extract dosage expressions."""
        return self._create_entities(
            self.DOSAGE_PATTERN, text, "DOSAGE"
        )

    def extract_frequencies(self, text):
        """Extract frequency expressions."""
        return self._create_entities(
            self.FREQUENCY_PATTERN, text, "FREQUENCY"
        )

    def extract_durations(self, text):
        """Extract duration expressions."""
        return self._create_entities(
            self.DURATION_PATTERN, text, "DURATION"
        )

    @staticmethod
    def _create_entities(pattern, text, label):
        """Convert regex matches into entity dictionaries."""
        entities = []

        for match in pattern.finditer(text):
            entities.append({
                "text": match.group(),
                "label": label,
                "start": match.start(),
                "end": match.end()
            })

        return entities

    def extract_all(self, text):
        """Extract all rule-based entities."""
        return (
            self.extract_dosages(text)
            + self.extract_frequencies(text)
            + self.extract_durations(text)
        )