import gzip
import glob
import re
from collections import Counter

RAW_DIR = "data/raw"

EXPECTED_CLASSES = {"1", "2", "3", "4", "5", "6", "7"}


def extract_ec_class_from_filename(filepath):
    """
    Extract the top-level EC class from the FASTA filename.

    Example:
    uniprotkb_reviewed_true_AND_ec_1_AND_NO_2026_10_03.fasta.gz
    -> 1
    """

    match = re.search(r"ec_([1-7])(?:_|\.|$)", filepath.lower())

    if match:
        return match.group(1)

    return None


def validate_file(filepath):
    """
    Count protein sequences in one compressed FASTA file.
    The EC class is determined from the filename.
    """

    total = 0
    labels = Counter()

    expected_class = extract_ec_class_from_filename(filepath)

    with gzip.open(filepath, "rt", encoding="utf-8") as handle:
        for line in handle:
            if not line.startswith(">"):
                continue

            total += 1

            if expected_class:
                labels[expected_class] += 1

    return total, labels


def main():
    print("=" * 70)
    print("UniProt EC Top-Level Label Validation")
    print("=" * 70)

    # Find all compressed FASTA files
    files = sorted(glob.glob(f"{RAW_DIR}/*.fasta.gz"))

    if not files:
        print("ERROR: No .fasta.gz files found.")
        return

    overall_labels = Counter()
    overall_total = 0

    print(f"\nFound {len(files)} FASTA files.\n")

    for filepath in files:
        print("-" * 70)
        print(f"File: {filepath}")

        total, labels = validate_file(filepath)

        detected_class = (
            next(iter(labels.keys()))
            if labels
            else "Unknown"
        )

        print(f"EC class         : {detected_class}")
        print(f"Sequences        : {total:,}")

        overall_total += total
        overall_labels.update(labels)

    print("\n" + "=" * 70)
    print("OVERALL VALIDATION")
    print("=" * 70)

    print(f"Total sequences: {overall_total:,}")

    print("\nEC top-level classes found:")

    for label in sorted(overall_labels):
        print(f"  EC {label}: {overall_labels[label]:,}")

    missing = EXPECTED_CLASSES - set(overall_labels.keys())

    print("\nExpected classes: 1, 2, 3, 4, 5, 6, 7")

    if missing:
        print(f"WARNING: Missing classes: {sorted(missing)}")
    else:
        print("All seven EC top-level classes are present.")

    print("=" * 70)


if __name__ == "__main__":
    main()