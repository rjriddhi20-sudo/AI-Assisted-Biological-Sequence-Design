# P05 — AI-Assisted Biological Sequence Design

## Project Code
P05 — FAIR-AI-P05

## Project Title
AI-Assisted Biological Sequence Design

## Current Phase
Phase 1 — Data Collection

## Team Role
Member 1 — Data Collection

## Scientific Task
Seven-class protein sequence classification using top-level Enzyme Commission (EC) classes.

### Input
Protein amino-acid sequence.

### Output
One of seven EC top-level classes:

1. Oxidoreductases
2. Transferases
3. Hydrolases
4. Lyases
5. Isomerases
6. Ligases
7. Translocases

## Dataset
Source: UniProtKB / Swiss-Prot (Reviewed)

Sequence type: Protein

The original raw FASTA files are intentionally excluded from Git tracking.

See:

- `docs/dataset.md`
- `docs/member1_handoff.md`
- `dataset_info.csv`

## Project Structure

```text
data/
├── raw/
└── processed/

docs/
├── dataset.md
└── member1_handoff.md

src/
├── inspect_dataset.py
├── validate_labels.py
├── preprocess_dataset.py
├── analyze_processed_dataset.py
├── split_dataset.py
└── inspect_splits.py

## Model Development and Evaluation

### Final Model

A Random Forest Classifier was trained using the processed
sequence-derived features.

Model configuration:

- Number of estimators: 300
- Maximum depth: 25
- Minimum samples per leaf: 1
- Class weight: balanced
- Random state: 42

### Final Test Performance

- Test Accuracy: 0.8085
- Macro F1-score: 0.8139
- Weighted F1-score: 0.8086

### Feature Importance

Feature importance was extracted from the trained Random Forest
model to identify the most influential sequence-derived features.

The highest-ranked feature was `length`, followed by amino-acid
composition features including `aa_W`, `aa_L`, `aa_C`, and `aa_F`.

Feature importance data is available in:

`data/processed/feature_importance.csv`

Top-20 feature importance visualization:

`data/processed/feature_importance_top20.png`

### Model Artifact

The trained final model is saved as:

`data/processed/random_forest_final.joblib`