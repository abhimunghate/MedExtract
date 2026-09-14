from flask import Blueprint, jsonify, request

from nlp.entity_extractor import MedicalEntityExtractor
from nlp.utils import group_entities_by_label


extraction_bp = Blueprint(
    "extraction",
    __name__,
    url_prefix="/api"
)


# Create the NLP extractor once when the application starts.
extractor = MedicalEntityExtractor()


@extraction_bp.route("/health", methods=["GET"])
def health_check():
    """Check whether the API is running."""

    return jsonify({
        "status": "ok",
        "service": "MedExtract",
        "nlp_model": "custom_medical_ner"
    })


@extraction_bp.route("/extract", methods=["POST"])
def extract_entities():
    """Extract medical entities from submitted text."""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body must contain JSON data."
        }), 400

    text = data.get("text")

    if not text:
        return jsonify({
            "status": "error",
            "message": "The 'text' field is required."
        }), 400

    if not isinstance(text, str):
        return jsonify({
            "status": "error",
            "message": "The 'text' field must be a string."
        }), 400

    text = text.strip()

    if not text:
        return jsonify({
            "status": "error",
            "message": "Medical text cannot be empty."
        }), 400

    entities = extractor.extract(text)

    grouped_entities = group_entities_by_label(entities)

    return jsonify({
        "status": "success",
        "input_text": text,
        "entity_count": len(entities),
        "entities": entities,
        "grouped_entities": grouped_entities
    })
    
@extraction_bp.route("/model-info", methods=["GET"])
def model_info():
    """Return information about the medical NLP model."""

    return jsonify({
        "model": "Custom Medical NER",
        "framework": "spaCy",
        "pipeline": [
            "Preprocessing",
            "Custom NER",
            "Dictionary Matching",
            "Rule Extraction",
            "Entity Resolution"
        ],
        "entity_types": [
            "SYMPTOM",
            "MEDICINE",
            "DISEASE",
            "MEDICAL_TERM",
            "DOSAGE",
            "FREQUENCY",
            "DURATION"
        ]
    })