# MedExtract

## Medical Text Information Extraction using NLP

**MedExtract** is an educational Natural Language Processing (NLP) system designed to extract predefined medical entities from unstructured medical text.

The system combines **Custom Named Entity Recognition (NER)**, **dictionary-based matching**, and **rule-based extraction** to identify important medical information such as symptoms, medicines, diseases, dosage, frequency, and duration.

> **Note:** MedExtract is developed for educational and NLP research purposes. It is not intended for medical diagnosis or clinical decision-making.

---

## Features

* Medical text preprocessing
* Custom Named Entity Recognition using spaCy
* Dictionary-based medical entity matching
* Rule-based medical information extraction
* Entity overlap and duplicate resolution
* REST API using Flask
* Web-based user interface
* Extraction history
* JSON export
* CSV export
* Model information endpoint
* API health monitoring
* Model evaluation
* Precision, Recall, and F1-score calculation

---

## System Architecture

```text
                 Medical Text
                      │
                      ▼
              Text Preprocessing
                      │
                      ▼
               Custom NER Model
                      │
                      ▼
             Dictionary Matching
                      │
                      ▼
                 Rule Engine
                      │
                      ▼
              Entity Resolution
                      │
                      ▼
          Extracted Medical Entities
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      Web Interface           REST API
```

The system uses a hybrid extraction approach where machine-learning-based NER is combined with dictionary and rule-based methods to improve entity coverage.

---

## Entity Types

| Entity Type    | Description                                                 |
| -------------- | ----------------------------------------------------------- |
| `SYMPTOM`      | Patient symptoms such as fever, cough, headache, and nausea |
| `MEDICINE`     | Medicines and drugs                                         |
| `DISEASE`      | Diseases and medical conditions                             |
| `MEDICAL_TERM` | General medical terminology                                 |
| `DOSAGE`       | Medication dosage information                               |
| `FREQUENCY`    | Medication or treatment frequency                           |
| `DURATION`     | Treatment or symptom duration                               |

---

## Technologies Used

### Backend

* **Python**
* **Flask**
* **spaCy**
* **Pandas**
* **NumPy**

### Frontend

* **HTML**
* **CSS**
* **JavaScript**

### NLP Techniques

* Natural Language Processing
* Named Entity Recognition
* Phrase Matching
* Dictionary-based Extraction
* Rule-based Extraction
* Entity Resolution

---

## Project Structure

```text
MedExtract/
│
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
├── test_ner_model.py
│
├── config/
│   ├── __init__.py
│   └── config.py
│
├── data/
│   ├── medical_terms.csv
│   ├── medicines.csv
│   ├── symptoms.csv
│   ├── diseases.csv
│   ├── sample_medical_text.txt
│   ├── ner_training_data.json
│   └── ner_evaluation_data.json
│
├── models/
│   └── medical_ner/
│       ├── config.cfg
│       ├── meta.json
│       ├── tokenizer
│       └── ...
│
├── nlp/
│   ├── __init__.py
│   ├── preprocessor.py
│   ├── entity_extractor.py
│   ├── ner_model.py
│   ├── rule_engine.py
│   └── utils.py
│
├── routes/
│   ├── __init__.py
│   └── extraction_routes.py
│
├── training/
│   ├── __init__.py
│   ├── train_ner.py
│   ├── evaluate_model.py
│   ├── validate_data.py
│   ├── error_analysis.py
│   └── experiment_results.md
│
├── tests/
│   ├── test_preprocessor.py
│   ├── test_entity_extractor.py
│   ├── test_rules.py
│   └── test_api.py
│
├── outputs/
│   └── .gitkeep
│
├── templates/
│   ├── index.html
│   └── results.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js
```

> Update the project tree if your actual folder structure contains additional files or folders.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/abhimunghate/MedExtract.git
cd MedExtract
```

Replace `<repository-url>` with the URL of your GitHub repository.

---

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

---

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
venv\Scripts\activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Install the spaCy Language Model

If the project uses the standard English spaCy model:

```bash
python -m spacy download en_core_web_sm
```

---

## Training the Custom NER Model

Before training, validate the training data:

```bash
python training/validate_data.py
```

Then train the custom medical NER model:

```bash
python training/train_ner.py
```

The trained model can then be used by the MedExtract extraction pipeline.

---

## Model Evaluation

The trained NER model can be evaluated using:

```bash
python training/evaluate_model.py
```

The evaluation measures:

* **Precision**
* **Recall**
* **F1-score**

### Evaluation Metrics

**Precision**

Measures how many of the entities predicted by the model are correct.

```text
Precision = Correct Predictions / Total Predictions
```

**Recall**

Measures how many of the actual entities were successfully identified.

```text
Recall = Correct Predictions / Total Actual Entities
```

**F1-Score**

Provides a combined measure of precision and recall.

```text
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

---

## Running the Application

Start the Flask application:

```bash
python app.py
```

The application will start on the local Flask development server.

Open the URL displayed in the terminal, typically:

```text
http://127.0.0.1:5000
```

---

## REST API

MedExtract provides REST API endpoints for interacting with the NLP system.

### Health Check

```http
GET /api/health
```

Example response:

```json
{
    "status": "ok",
    "service": "MedExtract",
    "nlp_model": "custom_medical_ner"
}
```

---

### Model Information

```http
GET /api/model-info
```

Example response:

```json
{
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
}
```

---

### Extract Medical Entities

```http
POST /api/extract
```

Request:

```json
{
    "text": "The patient has fever and headache and was prescribed paracetamol 500 mg twice daily."
}
```

Example response:

```json
{
    "status": "success",
    "input_text": "The patient has fever and headache and was prescribed paracetamol 500 mg twice daily.",
    "entity_count": 5,
    "entities": [
        {
            "text": "fever",
            "label": "SYMPTOM",
            "start": 20,
            "end": 25
        },
        {
            "text": "headache",
            "label": "SYMPTOM",
            "start": 30,
            "end": 38
        },
        {
            "text": "paracetamol",
            "label": "MEDICINE",
            "start": 59,
            "end": 70
        }
    ]
}
```

> The exact entities and entity count depend on the trained model, dictionaries, rules, and input text.

---

## API Testing

The project includes automated API tests using **pytest**.

Run the tests with:

```bash
pytest
```

The tests cover:

* Health endpoint
* Entity extraction endpoint
* Missing text validation
* Empty text validation
* API response status codes

---

## Extraction Pipeline

The MedExtract extraction process follows these stages:

### 1. Preprocessing

The input medical text is processed using spaCy to prepare it for entity extraction.

### 2. Custom NER

The trained custom NER model identifies medical entities that it has learned from the training data.

### 3. Dictionary Matching

Predefined medical dictionaries are used to identify known:

* Symptoms
* Medicines
* Diseases
* Medical terms

### 4. Rule-Based Extraction

The rule engine identifies structured medical information such as:

* Dosage
* Frequency
* Duration

### 5. Entity Resolution

Results from the NER model, dictionary matcher, and rule engine are combined.

Duplicate and overlapping entities are removed to produce the final entity list.

---

## Example

### Input

```text
The patient has fever and severe headache.
The doctor prescribed paracetamol 500 mg twice daily for 5 days.
```

### Extracted Information

| Text            | Entity Type |
| --------------- | ----------- |
| fever           | SYMPTOM     |
| severe headache | SYMPTOM     |
| paracetamol     | MEDICINE    |
| 500 mg          | DOSAGE      |
| twice daily     | FREQUENCY   |
| 5 days          | DURATION    |

The actual output may vary depending on the trained NER model and configured dictionaries/rules.

---

## Data Sources

The project uses structured CSV files containing predefined medical terminology.

Example:

```text
data/
├── symptoms.csv
├── medicines.csv
├── diseases.csv
└── medical_terms.csv
```

These dictionaries supplement the machine-learning NER model and help identify known medical terms that may not be detected by the trained model.

---

## Model Architecture

The system follows a **hybrid NLP architecture**:

```text
                 Input Medical Text
                         │
                         ▼
                  spaCy Processing
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
        Custom NER   Dictionary    Rule Engine
                     Matching
            │            │            │
            └────────────┼────────────┘
                         ▼
                 Entity Resolution
                         │
                         ▼
                Final Entity Output
```

This approach combines the flexibility of machine learning with the reliability of predefined dictionaries and rules.

---

## Advantages

* Combines multiple NLP extraction techniques
* Supports domain-specific medical entities
* Can be extended with additional medical terminology
* Provides a REST API for integration
* Includes automated API testing
* Provides model evaluation metrics
* Supports structured JSON output
* Suitable for educational NLP projects and experimentation

---

## Limitations

* The model depends on the quality and size of its training dataset.
* Dictionary matching can only identify terms present in the configured dictionaries.
* Rule-based extraction depends on predefined patterns.
* Medical language can be highly complex and ambiguous.
* The system is not intended for clinical diagnosis or medical decision-making.

---

## Future Scope

Possible improvements include:

* Expanding the medical training dataset
* Adding more medical entity types
* Improving NER model accuracy
* Adding context-aware entity extraction
* Handling medical abbreviations
* Supporting multiple languages
* Integrating transformer-based medical language models
* Adding confidence scores for extracted entities
* Improving the web dashboard
* Adding database-based extraction history
* Deploying the application as a cloud service

---

## Disclaimer

MedExtract is an **educational Natural Language Processing project** developed for academic and research purposes.

The system does **not** provide medical diagnosis, treatment recommendations, prescriptions, or clinical advice.

The extracted information should not be used as a substitute for consultation with a qualified healthcare professional.

---

## Author

**Abhijit Munghate**

Developed as an academic project on:

**Medical Text Information Extraction using Natural Language Processing**
