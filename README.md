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