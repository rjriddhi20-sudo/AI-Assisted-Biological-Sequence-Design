import os
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

FILES = {
    "TRAIN": "features_train.csv",
    "VALIDATION": "features_validation.csv",
    "TEST": "features_test.csv",
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_label_column(df):
    """
    Find the target/label column.
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

    for name in possible_names:
        if name in df.columns:
            return name

    return None


def inspect_dataset(name, filename):
    """
    Load and inspect one processed dataset.
    """

    filepath = os.path.join(PROCESSED_DIR, filename)

    print("\n" + "=" * 70)
    print(f"{name} DATASET")
    print("=" * 70)

    print(f"File: {filepath}")

    if not os.path.exists(filepath):
        print("ERROR: File not found.")
        return None

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"ERROR while reading file: {e}")
        return None

    print(f"\nRows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    missing_total = int(df.isnull().sum().sum())

    print("\nMissing values:")

    if missing_total == 0:
        print("  None")
    else:
        missing = df.isnull().sum()
        missing = missing[missing > 0]

        for column, count in missing.items():
            print(f"  {column}: {count:,}")

    # --------------------------------------------------------
    # Target column
    # --------------------------------------------------------

    label_column = find_label_column(df)

    if label_column is None:
        print("\nWARNING: Target column not found.")
        return df

    print(f"\nTarget column: {label_column}")

    print("\nTarget distribution:")

    distribution = df[label_column].value_counts().sort_index()

    for label, count in distribution.items():
        percentage = (count / len(df)) * 100

        print(
            f"  Class {label}: "
            f"{count:,} "
            f"({percentage:.2f}%)"
        )

    # --------------------------------------------------------
    # Duplicate rows
    # --------------------------------------------------------

    duplicates = int(df.duplicated().sum())

    print(f"\nDuplicate rows: {duplicates:,}")

    # --------------------------------------------------------
    # Numeric feature information
    # --------------------------------------------------------

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    print(f"\nNumeric columns: {len(numeric_columns)}")

    if numeric_columns:
        print("Numeric features:")
        for column in numeric_columns:
            print(f"  - {column}")

    return df


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("PROCESSED DATASET / TRAIN-VALIDATION-TEST INSPECTION")
    print("=" * 70)

    datasets = {}

    for name, filename in FILES.items():

        df = inspect_dataset(name, filename)

        if df is not None:
            datasets[name] = df

    # --------------------------------------------------------
    # Compare feature columns
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("FEATURE CONSISTENCY CHECK")
    print("=" * 70)

    if len(datasets) == 3:

        train_columns = set(datasets["TRAIN"].columns)
        validation_columns = set(datasets["VALIDATION"].columns)
        test_columns = set(datasets["TEST"].columns)

        if (
            train_columns
            == validation_columns
            == test_columns
        ):
            print("✓ Train / Validation / Test columns are identical.")
        else:
            print("WARNING: Dataset columns are different.")

            print("\nTrain only:")
            print(sorted(train_columns - validation_columns - test_columns))

            print("\nValidation only:")
            print(
                sorted(
                    validation_columns
                    - train_columns
                    - test_columns
                )
            )

            print("\nTest only:")
            print(
                sorted(
                    test_columns
                    - train_columns
                    - validation_columns
                )
            )

    # --------------------------------------------------------
    # Compare target classes
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("CLASS CONSISTENCY CHECK")
    print("=" * 70)

    class_sets = {}

    for name, df in datasets.items():

        label_column = find_label_column(df)

        if label_column:

            class_sets[name] = set(
                df[label_column].dropna().astype(str)
            )

            print(
                f"{name} classes: "
                f"{sorted(class_sets[name])}"
            )

    if len(class_sets) == 3:

        if (
            class_sets["TRAIN"]
            == class_sets["VALIDATION"]
            == class_sets["TEST"]
        ):
            print("\n✓ All datasets contain the same classes.")
        else:
            print(
                "\nWARNING: Train/Validation/Test "
                "contain different classes."
            )

    # --------------------------------------------------------
    # Final message
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("INSPECTION COMPLETE")
    print("=" * 70)

    print("\nNext stage:")
    print("  1. Verify class balance")
    print("  2. Prepare X and y")
    print("  3. Train baseline ML model")
    print("  4. Evaluate on validation set")
    print("  5. Final evaluation on test set")
    print("=" * 70)


if __name__ == "__main__":
    main()