# P05 AI-Assisted Biological Sequence Design
## Dataset Documentation

### 1. Dataset Overview

Project:
AI-Assisted Biological Sequence Design

Project Code:
P05

Sequence Type:
Protein

Dataset Type:
Protein amino-acid sequences

Primary Database:
UniProtKB / Swiss-Prot (Reviewed)

Primary Task:
Seven-class protein sequence classification based on top-level Enzyme Commission (EC) class.

---

### 2. Scientific Task

The project uses protein amino-acid sequences to predict the top-level enzyme class associated with a protein sequence.

The seven target classes are:

| EC Class | Enzyme Class |
|---|---|
| EC 1 | Oxidoreductases |
| EC 2 | Transferases |
| EC 3 | Hydrolases |
| EC 4 | Lyases |
| EC 5 | Isomerases |
| EC 6 | Ligases |
| EC 7 | Translocases |

Input:
Protein amino-acid sequence.

Output:
Predicted top-level EC class from 1 to 7.

This is a seven-class protein sequence classification problem.

---

### 3. Data Source

Database:
UniProtKB / Swiss-Prot

Entry status:
Reviewed

The dataset was obtained from UniProtKB using EC-class-based queries.

The downloaded files are stored in:

data/raw/

The original compressed FASTA files are preserved without modification.

---

### 4. Raw Dataset Files

The current raw dataset contains seven FASTA files:

1. EC 1
2. EC 2
3. EC 3
4. EC 4
5. EC 5
6. EC 6
7. EC 7

Exact filenames are recorded in dataset_info.csv.

---

### 5. Dataset Statistics

The initial inspection produced the following results:

| EC Class | Sequences | Unique Sequences | Minimum Length | Maximum Length | Average Length |
|---|---:|---:|---:|---:|---:|
| EC 1 | 34,349 | 29,906 | 4 | 4,723 | 391.68 |
| EC 2 | 94,618 | 79,849 | 5 | 35,213 | 407.92 |
| EC 3 | 62,148 | 53,036 | 6 | 6,306 | 383.85 |
| EC 4 | 24,608 | 20,507 | 7 | 4,367 | 347.74 |
| EC 5 | 15,942 | 13,309 | 9 | 7,756 | 388.46 |
| EC 6 | 28,253 | 24,244 | 10 | 15,639 | 544.40 |
| EC 7 | 14,978 | 12,565 | 11 | 5,058 | 400.14 |

The complete inspection results are stored in:

src/dataset_info.csv

---

### 6. File Format

The raw files use compressed FASTA format:

.fasta.gz

Each FASTA record contains:

1. A header beginning with `>`
2. A UniProt accession
3. A UniProt entry name
4. Protein name
5. Organism information
6. Additional UniProt metadata
7. Protein amino-acid sequence

Example:

>sp|ACCESSION|ENTRY_NAME Protein name OS=Organism GN=Gene PE=1 SV=1

The sequence consists primarily of one-letter amino-acid symbols.

---

### 7. Important Metadata

The FASTA headers may contain fields including:

- UniProt accession
- Entry name
- Protein name
- Organism
- NCBI taxonomy identifier
- Gene name
- Protein existence evidence
- Sequence version

These fields should be preserved when the processed dataset is created.

---

### 8. Raw Data Policy

The files in:

data/raw/

must not be modified.

No:

- duplicate removal
- character replacement
- sequence trimming
- filtering
- relabeling
- sequence editing

should be performed directly on the raw files.

All preprocessing must produce new files under:

data/processed/

---

### 9. Sequence Quality Observations

The initial inspection detected some sequences containing symbols such as:

B, U, X and Z

These characters must not be removed from the raw dataset.

Their treatment will be decided during the preprocessing phase.

The raw sequences remain unchanged.

---

### 10. Dataset Imbalance

The seven EC classes do not contain equal numbers of sequences.

EC 2 contains substantially more sequences than some of the other classes.

Therefore, the complete raw dataset should not automatically be used directly for model training.

The preprocessing phase should evaluate class balancing and construct an appropriate training dataset.

---

### 11. Proposed Machine Learning Task

The planned model input is:

Protein amino-acid sequence

The planned model output is:

One of seven EC top-level classes:

1, 2, 3, 4, 5, 6 or 7

Possible later approaches include:

- sequence encoding
- pretrained protein embeddings
- classical machine-learning classifiers
- pretrained protein language models

The final model architecture will be selected during the AI/ML analysis phase.

---

### 12. Scientific Scope

The prototype predicts the broad top-level EC class associated with a protein sequence.

It does not claim to:

- experimentally validate protein function
- guarantee biochemical activity
- predict every possible protein function
- replace laboratory experiments
- prove that a generated sequence is biologically functional

The project is a computational prototype for sequence analysis and prediction.

---

### 13. Dataset Limitations

Important limitations include:

1. The EC classes are broad functional categories.
2. The classes are imbalanced.
3. Some sequences contain ambiguous/non-standard amino-acid symbols.
4. Multiple sequences may represent highly similar proteins.
5. Sequence similarity can cause data leakage if train and test sets are not carefully separated.
6. Computational predictions do not constitute experimental biological validation.
7. UniProt annotations depend on available biological evidence and annotation procedures.

---

### 14. Reproducibility

Dataset download date:

2026-10-03

Database:

UniProtKB / Swiss-Prot

Raw files:

data/raw/

Inspection script:

src/inspect_dataset.py

Validation script:

src/validate_labels.py

Inspection report:

src/dataset_info.csv

---

### 15. Member 1 → Member 2 Handoff

Member 2 receives:

1. Original raw FASTA files
2. Dataset inspection report
3. Dataset documentation
4. Sequence type definition
5. EC class definitions
6. Prediction task definition

Member 2 must create processed copies and must not modify the raw files.

---

### 16. Expected Processed Dataset

The processed dataset should contain suitable protein sequences with their corresponding EC class labels.

Expected conceptual format:

| accession | sequence | ec_class |
|---|---|---|
| UniProt ID | amino-acid sequence | 1–7 |

Additional metadata such as protein name, organism and gene may be retained where useful.

---

### 17. Final Prediction Definition

Given a protein amino-acid sequence:

Input:
`protein sequence`

Predict:

`EC top-level class`

Possible outputs:

`1, 2, 3, 4, 5, 6, 7`

This definition is the basis for the subsequent data processing and AI/ML phases.