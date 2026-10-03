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

The raw dataset contains seven FASTA files corresponding to EC classes 1 through 7.

The files are stored under:

data/raw/

Exact filenames can be inspected using the dataset inspection scripts.

The raw dataset contains:

| EC Class | Raw Sequences |
|---|---:|
| EC 1 | 34,349 |
| EC 2 | 94,618 |
| EC 3 | 62,148 |
| EC 4 | 24,608 |
| EC 5 | 15,942 |
| EC 6 | 28,253 |
| EC 7 | 14,978 |
| **Total** | **274,896** |

---

### 5. Initial Dataset Statistics

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

The dataset inspection report is stored in:

dataset_info.csv

---

### 6. Preprocessing

The preprocessing pipeline performs quality filtering and duplicate removal while leaving the original raw files unchanged.

The preprocessing results were:

| EC Class | Original | Invalid Removed | Short Removed | Valid |
|---|---:|---:|---:|---:|
| EC 1 | 34,349 | 275 | 93 | 33,981 |
| EC 2 | 94,618 | 223 | 27 | 94,368 |
| EC 3 | 62,148 | 212 | 145 | 61,791 |
| EC 4 | 24,608 | 120 | 19 | 24,469 |
| EC 5 | 15,942 | 36 | 8 | 15,898 |
| EC 6 | 28,253 | 20 | 3 | 28,230 |
| EC 7 | 14,978 | 68 | 4 | 14,906 |

Across all classes:

- Raw sequences: 274,896
- Invalid sequences removed: 954
- Short sequences removed: 299
- Sequences before deduplication: 273,643
- Duplicate sequences removed: 41,716
- Final processed sequences: 231,927

The preprocessing pipeline requires valid sequences to use the standard 20 amino-acid alphabet and to have a minimum length of 20.

---

### 7. Final Processed Dataset

The final processed dataset contains:

**231,927 unique protein sequences**

Final class distribution:

| EC Class | Sequences | Percentage |
|---|---:|---:|
| EC 1 | 29,546 | 12.74% |
| EC 2 | 79,603 | 34.32% |
| EC 3 | 52,685 | 22.72% |
| EC 4 | 20,369 | 8.78% |
| EC 5 | 13,265 | 5.72% |
| EC 6 | 23,993 | 10.35% |
| EC 7 | 12,466 | 5.37% |
| **Total** | **231,927** | **100%** |

Final sequence length statistics:

| Statistic | Value |
|---|---:|
| Minimum length | 20 |
| Maximum length | 35,213 |
| Average length | 420.99 |

The final processed dataset contains no duplicate sequences and no cross-label conflicts.

---

### 8. Processed Dataset Format

The processed dataset uses the following columns:

| Column | Description |
|---|---|
| sequence | Protein amino-acid sequence |
| ec_class | Top-level EC class label from 1 to 7 |
| length | Protein sequence length |

The main processed dataset is:

data/processed/protein_sequences.csv

Additional processed files are:

data/processed/train.csv

data/processed/validation.csv

data/processed/test.csv

---

### 9. Dataset Quality Checks

The processed dataset analysis confirmed:

- Total sequences: 231,927
- Unique sequences: 231,927
- Duplicate sequences: 0
- Sequences with multiple EC labels: 0
- Minimum sequence length: 20
- All seven EC classes are present.

These checks were performed using the dataset analysis and inspection scripts.

---

### 10. Train / Validation / Test Split

The processed dataset was divided using a stratified split with random seed 42.

| Dataset | Sequences | Percentage |
|---|---:|---:|
| Training | 162,347 | 70.00% |
| Validation | 34,784 | 15.00% |
| Testing | 34,796 | 15.00% |
| **Total** | **231,927** | **100%** |

The class distribution was preserved across the three datasets.

Generated files:

data/processed/train.csv

data/processed/validation.csv

data/processed/test.csv

---

### 11. Split Quality Checks

The train, validation and test datasets were inspected after splitting.

All three datasets contain the same columns:

- sequence
- ec_class
- length

No missing values were found.

All seven EC classes are present in each dataset.

Sequence overlap checks produced:

| Comparison | Overlapping Sequences |
|---|---:|
| Train and Validation | 0 |
| Train and Test | 0 |
| Validation and Test | 0 |

Therefore, no identical sequence was found across the three dataset splits.

---

### 12. Dataset Imbalance

The seven EC classes do not contain equal numbers of sequences.

EC 2 is the largest class with 79,603 sequences (34.32%).

EC 5 and EC 7 are smaller classes with 13,265 (5.72%) and 12,466 (5.37%) sequences respectively.

This class imbalance should be considered during the AI/ML analysis phase.

---

### 13. File and Data Policy

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

All preprocessing operations produce new files under:

data/processed/

Large raw and generated processed CSV datasets are excluded from Git version control using .gitignore.

---

### 14. Proposed Machine Learning Task

The model input is:

Protein amino-acid sequence

The model output is:

One of seven EC top-level classes:

1, 2, 3, 4, 5, 6 or 7

Possible approaches for the AI/ML stage include:

- sequence encoding
- pretrained protein embeddings
- classical machine-learning classifiers
- pretrained protein language models

The final model architecture will be selected during the AI/ML analysis phase.

---

### 15. Scientific Scope

The prototype predicts the broad top-level EC class associated with a protein sequence.

It does not claim to:

- experimentally validate protein function
- guarantee biochemical activity
- predict every possible protein function
- replace laboratory experiments
- prove that a generated sequence is biologically functional

The project is a computational prototype for sequence analysis and prediction.

---

### 16. Dataset Limitations

Important limitations include:

1. The EC classes are broad functional categories.
2. The classes are imbalanced.
3. The dataset is based on reviewed UniProtKB / Swiss-Prot entries.
4. Sequence similarity may still exist between different proteins even after exact duplicate removal.
5. Computational predictions do not constitute experimental biological validation.
6. UniProt annotations depend on available biological evidence and annotation procedures.
7. The current task predicts top-level EC classes rather than detailed EC subclasses.

---

### 17. Reproducibility

Dataset download date:

2026-10-03

Database:

UniProtKB / Swiss-Prot

Raw data directory:

data/raw/

Processed data directory:

data/processed/

Scripts used during Member 2 processing:

src/validate_labels.py

src/inspect_dataset.py

src/preprocess_dataset.py

src/analyze_processed_dataset.py

src/split_dataset.py

src/inspect_splits.py

src/features.py

Dataset inspection report:

dataset_info.csv

Random seed used for dataset splitting:

42

---

### 18. Member 1 -> Member 2 Handoff

Member 2 received:

1. Original raw FASTA files
2. Dataset inspection information
3. Dataset documentation
4. Sequence type definition
5. EC class definitions
6. Prediction task definition

Member 2 created the processed dataset without modifying the original raw FASTA files.

---

### 19. Member 2 -> Member 3 Handoff

Member 2 data processing and feature extraction are complete.

The AI/ML stage receives the following dataset definition:

Input:
Protein amino-acid sequence

Target:
Top-level EC class

Classes:
1, 2, 3, 4, 5, 6, 7

Training set:
162,347 sequences

Validation set:
34,784 sequences

Test set:
34,796 sequences

The three splits contain no identical sequence overlap.

The final processed dataset contains 231,927 unique sequences.

### Feature representation

Amino Acid Composition (AAC) was used as the baseline sequence representation.

For each protein sequence, the frequency of each of the 20 standard amino acids was calculated:

A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y

Each amino-acid feature is calculated as:

amino-acid count / sequence length

The sequence length is included as an additional numerical input feature.

Therefore, each sequence has:

- 20 amino-acid composition features
- 1 sequence-length feature
- 21 input features in total
- 1 target label: ec_class

Feature files generated:

data/processed/features_train.csv

data/processed/features_validation.csv

data/processed/features_test.csv

The feature datasets contain no missing values, and all seven EC classes are present in the training feature dataset.

The generated feature CSV files are intentionally excluded from Git because of their size. The required feature data should be transferred to the Member 3 environment separately.

The feature extraction implementation is:

src/features.py

---

### 20. Final Prediction Definition

Given a protein amino-acid sequence:

Input:
`protein sequence`

Predict:

`EC top-level class`

Possible outputs:

`1, 2, 3, 4, 5, 6, 7`

This definition is the basis for the subsequent AI/ML analysis and sequence prediction/design phases.