import os
import pandas as pd

# ============================================================
# Configuration
# ============================================================

PROCESSED_DIR = "data/processed"

FILES = {
    "TRAIN": os.path.join(PROCESSED_DIR, "train.csv"),
    "VALIDATION": os.path.join(PROCESSED_DIR, "validation.csv"),
    "TEST": os.path.join(PROCESSED_DIR, "test.csv"),
}


# ============================================================
# Helper functions
# ============================================================

def find_label_column(df):
    """
    Try to identify the EC class / target column automatically.
    """
    possible_names = [
        "ec_class",
        "EC_class",
        "ec",
        "EC",
        "label",
        "target",
        "class",
    ]

    for column in possible_names:
        if column in df.columns:
            return column

    return None


def find_sequence_column(df):
    """
    Try to identify the protein sequence column automatically.
    """
    possible_names = [
        "sequence",
        "Sequence",
        "protein_sequence",
        "proteinSequence",
        "seq",
    ]

    for column in possible_names:
        if column in df.columns:
            return column

    return None


def print_dataset_info(name, df):
    print("\n" + "=" * 70)
    print(f"{name} DATASET")
    print("=" * 70)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

    # Label distribution
    label_column = find_label_column(df)

    if label_column:
        print(f"\nLabel column: {label_column}")
        print("\nEC Class Distribution:")

        counts = df[label_column].value_counts().sort_index()

        for label, count in counts.items():
            percentage = (count / len(df)) * 100
            print(f"  EC {label}: {count:,} ({percentage:.2f}%)")
    else:
        print("\nWARNING: Could not automatically identify the label column.")

    # Missing values
    print("\nMissing Values:")

    missing = df.isnull().sum()
    missing_found = False

    for column, count in missing.items():
        if count > 0:
            print(f"  {column}: {count:,}")
            missing_found = True

    if not missing_found:
        print("  No missing values found.")


# ============================================================
# Main validation
# ============================================================

def main():

    print("=" * 70)
    print("PROCESSED DATASET / TRAIN-VALIDATION-TEST SPLIT INSPECTION")
    print("=" * 70)

    datasets = {}

    # --------------------------------------------------------
    # Load datasets
    # --------------------------------------------------------

    for name, filepath in FILES.items():

        print(f"\nLoading {name}: {filepath}")

        if not os.path.exists(filepath):
            print(f"ERROR: File not found: {filepath}")
            return

        try:
            df = pd.read_csv(filepath)
            datasets[name] = df
            print(f"Loaded successfully: {len(df):,} rows")

        except Exception as e:
            print(f"ERROR loading {filepath}: {e}")
            return

    # --------------------------------------------------------
    # Display information
    # --------------------------------------------------------

    for name, df in datasets.items():
        print_dataset_info(name, df)

    # --------------------------------------------------------
    # Check columns
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("COLUMN CONSISTENCY CHECK")
    print("=" * 70)

    train_columns = set(datasets["TRAIN"].columns)
    validation_columns = set(datasets["VALIDATION"].columns)
    test_columns = set(datasets["TEST"].columns)

    if (
        train_columns == validation_columns
        and train_columns == test_columns
    ):
        print("All three datasets have identical columns.")
    else:
        print("WARNING: Dataset columns are not identical.")

        print("\nTrain only:")
        print(train_columns - validation_columns - test_columns)

        print("\nValidation only:")
        print(validation_columns - train_columns - test_columns)

        print("\nTest only:")
        print(test_columns - train_columns - validation_columns)

    # --------------------------------------------------------
    # Identify label column
    # --------------------------------------------------------

    label_column = find_label_column(datasets["TRAIN"])

    print("\n" + "=" * 70)
    print("LABEL COLUMN CHECK")
    print("=" * 70)

    if label_column:
        print(f"Detected label column: {label_column}")

        for name, df in datasets.items():
            labels = sorted(df[label_column].dropna().astype(str).unique())

            print(f"{name}: {labels}")

        expected_classes = {str(i) for i in range(1, 8)}

        actual_classes = set(
            datasets["TRAIN"][label_column]
            .dropna()
            .astype(str)
        )

        missing_classes = expected_classes - actual_classes

        if missing_classes:
            print(f"WARNING: Training data is missing: {sorted(missing_classes)}")
        else:
            print("All seven EC classes are present in training data.")

    else:
        print("WARNING: Label column could not be identified.")

    # --------------------------------------------------------
    # Sequence overlap check
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("SEQUENCE OVERLAP CHECK")
    print("=" * 70)

    sequence_column = find_sequence_column(datasets["TRAIN"])

    if sequence_column:

        print(f"Sequence column detected: {sequence_column}")

        train_sequences = set(
            datasets["TRAIN"][sequence_column].dropna().astype(str)
        )

        validation_sequences = set(
            datasets["VALIDATION"][sequence_column].dropna().astype(str)
        )

        test_sequences = set(
            datasets["TEST"][sequence_column].dropna().astype(str)
        )

        train_validation = train_sequences & validation_sequences
        train_test = train_sequences & test_sequences
        validation_test = validation_sequences & test_sequences

        print(f"Train ∩ Validation: {len(train_validation):,}")
        print(f"Train ∩ Test      : {len(train_test):,}")
        print(f"Validation ∩ Test : {len(validation_test):,}")

        if not train_validation and not train_test and not validation_test:
            print("No sequence overlap found.")
        else:
            print("WARNING: Duplicate sequences exist between splits.")

    else:
        print("Sequence column not found.")
        print("Skipping sequence overlap check.")

    # --------------------------------------------------------
    # Dataset sizes
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATASET SIZE SUMMARY")
    print("=" * 70)

    train_count = len(datasets["TRAIN"])
    validation_count = len(datasets["VALIDATION"])
    test_count = len(datasets["TEST"])

    total = train_count + validation_count + test_count

    print(f"Training   : {train_count:,}")
    print(f"Validation : {validation_count:,}")
    print(f"Testing    : {test_count:,}")
    print(f"Total      : {total:,}")

    print("\nSplit percentages:")

    print(f"Training   : {(train_count / total) * 100:.2f}%")
    print(f"Validation : {(validation_count / total) * 100:.2f}%")
    print(f"Testing    : {(test_count / total) * 100:.2f}%")

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL STATUS")
    print("=" * 70)

    print("Dataset inspection completed successfully.")

    print("\nThe train/validation/test datasets are ready for")
    print("the next machine-learning stage.")

    print("=" * 70)


# ============================================================
# Program entry point
# ============================================================

if __name__ == "__main__":
    main()