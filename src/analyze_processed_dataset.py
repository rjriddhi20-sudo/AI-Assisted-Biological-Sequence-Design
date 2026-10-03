import csv
import os
from collections import Counter, defaultdict

PROCESSED_FILE = "data/processed/protein_sequences.csv"


def main():

    print("=" * 70)
    print("Processed Protein Dataset Analysis")
    print("=" * 70)

    if not os.path.exists(PROCESSED_FILE):
        print(f"ERROR: File not found: {PROCESSED_FILE}")
        return

    sequences = []
    labels = []
    lengths = []

    with open(PROCESSED_FILE, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            sequence = row["sequence"]
            label = row["ec_class"]
            length = int(row["length"])

            sequences.append(sequence)
            labels.append(label)
            lengths.append(length)

    print(f"\nTotal sequences: {len(sequences):,}")

    # ---------------------------------------------------------
    # Class distribution
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("EC CLASS DISTRIBUTION")
    print("-" * 70)

    class_counts = Counter(labels)

    for ec_class in sorted(class_counts):
        count = class_counts[ec_class]
        percentage = (count / len(labels)) * 100

        print(
            f"EC {ec_class}: {count:,} "
            f"({percentage:.2f}%)"
        )

    # ---------------------------------------------------------
    # Length statistics
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("SEQUENCE LENGTH STATISTICS")
    print("-" * 70)

    print(f"Minimum length : {min(lengths):,}")
    print(f"Maximum length : {max(lengths):,}")
    print(f"Average length : {sum(lengths) / len(lengths):.2f}")

    # ---------------------------------------------------------
    # Duplicate check
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("DUPLICATE CHECK")
    print("-" * 70)

    unique_sequences = set(sequences)

    duplicate_count = len(sequences) - len(unique_sequences)

    print(f"Total sequences  : {len(sequences):,}")
    print(f"Unique sequences : {len(unique_sequences):,}")
    print(f"Duplicates       : {duplicate_count:,}")

    if duplicate_count == 0:
        print("No duplicate sequences found.")
    else:
        print("WARNING: Duplicate sequences remain.")

    # ---------------------------------------------------------
    # Check conflicting labels
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("CROSS-LABEL CONFLICT CHECK")
    print("-" * 70)

    sequence_labels = defaultdict(set)

    for sequence, label in zip(sequences, labels):
        sequence_labels[sequence].add(label)

    conflicting = {
        sequence: sequence_labels[sequence]
        for sequence in sequence_labels
        if len(sequence_labels[sequence]) > 1
    }

    print(f"Sequences with multiple EC labels: {len(conflicting):,}")

    if conflicting:
        print(
            "WARNING: Some identical sequences have different EC labels."
        )

        shown = 0

        for sequence, conflict_labels in conflicting.items():

            print(
                f"  Labels: {sorted(conflict_labels)} "
                f"| Length: {len(sequence)}"
            )

            shown += 1

            if shown >= 10:
                print("  ... showing first 10 conflicts only")
                break

    else:
        print("No cross-label conflicts found.")

    # ---------------------------------------------------------
    # Final assessment
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATASET ANALYSIS COMPLETE")
    print("=" * 70)

    print("\nDataset is ready for the next preprocessing stage:")
    print("  → Train/validation/test split")
    print("  → Feature/sequence representation")
    print("  → AI/ML model preparation")

    print("=" * 70)


if __name__ == "__main__":
    main()