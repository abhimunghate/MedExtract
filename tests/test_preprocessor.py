from nlp.preprocessor import TextPreprocessor


def test_tokenization():
    processor = TextPreprocessor()

    tokens = processor.tokenize(
        "The patient has fever."
    )

    assert "fever" in tokens


def test_sentences():
    processor = TextPreprocessor()

    sentences = processor.sentences(
        "Patient has fever. Patient has cough."
    )

    assert len(sentences) == 2