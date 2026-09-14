# MedExtract NLP Experiments

## Experiment 1

### Model
Custom spaCy NER

### Training Examples
12

### Epochs
30

### Dropout
0.2

### Evaluation Examples
5

### Results

Precision: [1.0000]
Recall: [0.4286]
F1 Score: [0.6000]

### Observations

The initial model was trained using a small manually
annotated dataset. The model requires additional
training examples to improve generalization.




# Experiment Results

| Experiment | Dataset Size | Epochs | Precision | Recall | F1 |
|------------|--------------|--------|-----------|--------|----|
| E1 | 12 | 30 | actual | actual | actual |
| E2 | 30 | 40 | actual | actual | actual |
| E3 | 100 | 40 | actual | actual | actual |

## Observations

E1 used the initial small dataset.

E2 introduced additional variations in sentence
structure and entity contexts.

E3 used a larger dataset and was evaluated on an
independent evaluation set.