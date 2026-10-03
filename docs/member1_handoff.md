# Member 1 → Member 2 Dataset Handoff

## Project

P05 — AI-Assisted Biological Sequence Design

## Member 1 Responsibility

Data Collection

## Sequence Type

Protein

The dataset consists of protein amino-acid sequences.

---

## Scientific Task

The project will perform seven-class protein sequence classification.

Given a protein amino-acid sequence, the model will predict its top-level Enzyme Commission (EC) class.

### Target classes

| Label | EC Class |
|---|---|
| 1 | Oxidoreductases |
| 2 | Transferases |
| 3 | Hydrolases |
| 4 | Lyases |
| 5 | Isomerases |
| 6 | Ligases |
| 7 | Translocases |

---

## Raw Dataset Source

Primary source:

UniProtKB / Swiss-Prot

Entry status:

Reviewed

The raw data was collected using EC-class-based UniProtKB queries.

---

## Raw Dataset Location

All original downloaded files are stored under:

data/raw/

The raw files are compressed FASTA files:

.fasta.gz

The raw files must not be modified.

---

## Raw Dataset

Seven files are currently available:

- EC 1
- EC 2
- EC 3
- EC 4
- EC 5
- EC 6
- EC 7

Exact filenames are recorded in:

src/dataset_info.csv

---

## Raw Dataset Size

Initial inspection found approximately 275,000 sequence records across the seven files.

The exact counts are documented in:

src/dataset_info.csv

---

## Initial Dataset Statistics

| EC Class | Sequences | Unique Sequences |
|---|---:|---:|
| EC 1 | 34,349 | 29,906 |
| EC 2 | 94,618 | 79,849 |
| EC 3 | 62,148 | 53,036 |
| EC 4 | 24,608 | 20,507 |
| EC 5 | 15,942 | 13,309 |
| EC 6 | 28,253 | 24,244 |
| EC 7 | 14,978 | 12,565 |

---

## FASTA Header Information

Raw FASTA headers may contain:

- UniProt accession
- UniProt entry name
- Protein name
- Organism
- Taxonomy identifier
- Gene name
- Protein existence evidence
- Sequence version

Example structure:

>sp|ACCESSION|ENTRY_NAME Protein name OS=Organism OX=TaxID GN=Gene PE=1 SV=1

---

## Sequence

The sequence field contains the protein amino-acid sequence represented using one-letter amino-acid symbols.

Some sequences contain ambiguity/non-standard symbols such as:

B, U, X, Z

These must not be modified in the raw dataset.

---

# Processing Requirement

Member 2 should create processed copies.

The original files under:

data/raw/

must remain unchanged.

---

## Proposed Processed Dataset

Target:

3,000 sequences per EC class.

Total target:

21,000 sequences.

| EC Class | Target Sequences |
|---|---:|
| EC 1 | 3,000 |
| EC 2 | 3,000 |
| EC 3 | 3,000 |
| EC 4 | 3,000 |
| EC 5 | 3,000 |
| EC 6 | 3,000 |
| EC 7 | 3,000 |
| Total | 21,000 |

---

## Sampling

Sampling should be performed separately within each EC class.

A fixed random seed should be used for reproducibility.

Recommended seed:

42

Member 2 should not simply take the first 3,000 records from each file.

---

## Recommended Processing Steps

1. Read the raw FASTA files.
2. Parse the FASTA headers.
3. Extract UniProt accession.
4. Extract protein name where available.
5. Extract organism where available.
6. Extract gene name where available.
7. Assign the EC class according to the source file.
8. Remove exact duplicate sequences.
9. Check sequence characters.
10. Apply documented sequence-quality filters.
11. Randomly sample 3,000 sequences per class using seed 42.
12. Save the processed dataset separately.
13. Verify class balance.
14. Check sequence length distribution.
15. Check for possible sequence similarity/data leakage before final train/test splitting.

---

## Expected Processed Dataset Fields

At minimum:

| Field | Description |
|---|---|
| accession | UniProt accession |
| sequence | Protein amino-acid sequence |
| ec_class | Target class 1–7 |

Recommended additional fields:

| Field | Description |
|---|---|
| protein_name | Protein description/name |
| organism | Source organism |
| gene | Gene name |
| sequence_length | Number of amino acids |

---

## Prediction Task

Input:

A protein amino-acid sequence.

Output:

One of:

1, 2, 3, 4, 5, 6, 7

The model therefore performs:

Seven-class protein sequence classification.

---

## Important Data Leakage Warning

Sequence similarity must be considered when creating training and testing sets.

Highly similar protein sequences should not be blindly distributed between training and testing sets because this may produce overly optimistic performance estimates.

The final splitting strategy must be documented.

---

## Raw Data Rule

DO NOT modify:

data/raw/

Do not:

- overwrite raw files
- delete sequences
- replace amino-acid characters
- edit FASTA headers
- relabel raw records
- remove duplicates from raw files
- trim raw sequences

All changes must be made to copies under:

data/processed/

---

## Member 1 Deliverables

Member 1 provides:

- Raw FASTA dataset
- Dataset inspection report
- Dataset documentation
- Sequence type
- Source information
- EC class definitions
- Scientific prediction task
- Processing requirements
- Data leakage warning

---

## Current Scripts

Dataset inspection:

src/inspect_dataset.py

Label validation:

src/validate_labels.py

Dataset inspection report:

src/dataset_info.csv

---

## Dataset Documentation

Full dataset documentation:

docs/dataset.md

---

## Handoff Status

Raw data collection: COMPLETE

Initial dataset inspection: COMPLETE

Label validation: COMPLETE

Dataset documentation: COMPLETE

Final processed dataset: TO BE CREATED BY MEMBER 2

AI/ML modeling: MEMBER 3 / subsequent phase

Sequence prediction/design: MEMBER 4 / subsequent phase