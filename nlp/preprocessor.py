import spacy


class TextPreprocessor:
    """Handles basic NLP preprocessing using spaCy."""

    def __init__(self, model_name="en_core_web_sm"):
        self.nlp = spacy.load(model_name)

    def process(self, text):
        """Process input text using the spaCy pipeline."""
        return self.nlp(text)

    def tokenize(self, text):
        """Return a list of tokens."""
        doc = self.process(text)
        return [token.text for token in doc]

    def lemmatize(self, text):
        """Return tokens with their lemmas."""
        doc = self.process(text)

        return [
            {
                "text": token.text,
                "lemma": token.lemma_
            }
            for token in doc
            if not token.is_space
        ]

    def sentences(self, text):
        """Split text into sentences."""
        doc = self.process(text)

        return [sentence.text.strip() for sentence in doc.sents]