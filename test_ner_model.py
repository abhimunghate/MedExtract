import spacy


nlp = spacy.load(
    "models/medical_ner"
)


text = (
    "The patient has fever and headache. "
    "The doctor prescribed Paracetamol."
)


doc = nlp(text)


print("\nInput:")
print(text)

print("\nDetected entities:")

for entity in doc.ents:

    print(
        f"{entity.text:20} "
        f"{entity.label_:15} "
        f"{entity.start_char}-{entity.end_char}"
    )