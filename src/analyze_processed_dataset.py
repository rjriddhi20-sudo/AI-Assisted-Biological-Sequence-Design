import csv
import os
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

FILES = {
    "Train": "features_train.csv",
    "Validation": "features_validation.csv",
    "Test": "features_test.csv",
}


def analyze_file(name, filename):

    path = os.path.join(PROCESSED_DIR, filename)

    print("\n" + "=" * 70)
    print(f"{name.upper()} DATASET")
    print("=" * 70)

    if not os.path.exists(path):
        print(f"ERROR: File not found: {path}")
        return

    rows = []

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("ERROR: File is empty.")
        return

    columns = reader.fieldnames

    print(f"File    : {filename}")
    print(f"Rows    : {len(rows):,}")
    print(f"Columns : {len(columns):,}")

    print("\nColumns:")
    print(", ".join(columns))

    # ---------------------------------------------------------
    # EC class distribution
    # ---------------------------------------------------------

    if "ec_class" in columns:

        print("\n" + "-" * 70)
        print("EC CLASS DISTRIBUTION")
        print("-" * 70)

        labels = [row["ec_class"] for row in rows]

        class_counts = Counter(labels)

        for ec_class in sorted(class_counts):
            count = class_counts[ec_class]
            percentage = count / len(labels) * 100

            print(
                f"EC {ec_class}: "
                f"{count:,} "
                f"({percentage:.2f}%)"
            )

    # ---------------------------------------------------------
    # Sequence length statistics
    # ---------------------------------------------------------

    if "length" in columns:

        print("\n" + "-" * 70)
        print("SEQUENCE LENGTH STATISTICS")
        print("-" * 70)

        lengths = []

        for row in rows:
            try:
                lengths.append(int(float(row["length"])))
            except (ValueError, TypeError):
                pass

        if lengths:
            print(f"Minimum length : {min(lengths):,}")
            print(f"Maximum length : {max(lengths):,}")
            print(f"Average length : {sum(lengths) / len(lengths):.2f}")

    # ---------------------------------------------------------
    # Missing values
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("MISSING VALUE CHECK")
    print("-" * 70)

    missing_found = False

    for column in columns:

        missing = sum(
            1 for row in rows
            if row[column] is None or row[column].strip() == ""
        )

        if missing > 0:
            missing_found = True
            print(f"{column}: {missing:,} missing values")

    if not missing_found:
        print("No missing values found.")

    # ---------------------------------------------------------
    # Final
    # ---------------------------------------------------------

    print("\nAnalysis complete.")


def main():

    print("=" * 70)
    print("FEATURE DATASET ANALYSIS")
    print("=" * 70)

    for name, filename in FILES.items():
        analyze_file(name, filename)

    print("\n" + "=" * 70)
    print("ALL DATASETS ANALYZED")
    print("=" * 70)


if __name__ == "__main__":
    main()