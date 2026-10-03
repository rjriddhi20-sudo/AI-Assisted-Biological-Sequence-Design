import gzip
import glob
import os
import csv
from collections import Counter

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

OUTPUT_FILE = os.path.join(PROCESSED_DIR, "protein_sequences.csv")
SUMMARY_FILE = os.path.join(PROCESSED_DIR, "preprocessing_summary.csv")

# Standard 20 amino acids
VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

# Minimum sequence length
MIN_LENGTH = 20


def get_ec_class(filepath):
    """Extract EC top-level class from filename."""
    filename = os.path.basename(filepath)

    for i in range(1, 8):
        if f"ec_{i}" in filename:
            return str(i)

    return None


def process_file(filepath):
    """Read one compressed FASTA file and return processed sequences."""

    ec_class = get_ec_class(filepath)

    if ec_class is None:
        print(f"WARNING: Could not determine EC class: {filepath}")
        return []

    sequences = []
    current_sequence = []

    with gzip.open(filepath, "rt", encoding="utf-8") as handle:

        for line in handle:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):

                if current_sequence:
                    sequence = "".join(current_sequence).upper()
                    sequences.append((sequence, ec_class))

                current_sequence = []

            else:
                current_sequence.append(line)

        # Add final sequence
        if current_sequence:
            sequence = "".join(current_sequence).upper()
            sequences.append((sequence, ec_class))

    return sequences


def main():

    print("=" * 70)
    print("Protein Dataset Preprocessing")
    print("=" * 70)

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    files = sorted(glob.glob(os.path.join(RAW_DIR, "*.fasta.gz")))

    if not files:
        print("ERROR: No .fasta.gz files found.")
        return

    print(f"\nFound {len(files)} FASTA files.\n")

    all_sequences = []
    summary = []

    total_original = 0
    total_invalid = 0
    total_short = 0

    # ---------------------------------------------------------
    # Process each file
    # ---------------------------------------------------------

    for filepath in files:

        filename = os.path.basename(filepath)
        ec_class = get_ec_class(filepath)

        print("-" * 70)
        print(f"Processing: {filename}")
        print(f"EC class  : {ec_class}")

        sequences = process_file(filepath)

        original_count = len(sequences)
        invalid_count = 0
        short_count = 0

        valid_sequences = []

        for sequence, label in sequences:

            # Check amino acid characters
            if not set(sequence).issubset(VALID_AMINO_ACIDS):
                invalid_count += 1
                continue

            # Check minimum length
            if len(sequence) < MIN_LENGTH:
                short_count += 1
                continue

            valid_sequences.append((sequence, label))

        print(f"Original sequences : {original_count:,}")
        print(f"Invalid sequences  : {invalid_count:,}")
        print(f"Short sequences    : {short_count:,}")
        print(f"Valid sequences    : {len(valid_sequences):,}")

        all_sequences.extend(valid_sequences)

        total_original += original_count
        total_invalid += invalid_count
        total_short += short_count

        summary.append({
            "file": filename,
            "ec_class": ec_class,
            "original_sequences": original_count,
            "invalid_sequences": invalid_count,
            "short_sequences": short_count,
            "valid_sequences": len(valid_sequences)
        })

    # ---------------------------------------------------------
    # Remove duplicate sequences
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("Removing duplicate sequences")
    print("=" * 70)

    before_dedup = len(all_sequences)

    unique_sequences = {}
    duplicate_count = 0

    for sequence, label in all_sequences:

        # Keep one copy of each sequence.
        # Label is retained with the first occurrence.
        if sequence not in unique_sequences:
            unique_sequences[sequence] = label
        else:
            duplicate_count += 1

    processed_data = [
        (sequence, label)
        for sequence, label in unique_sequences.items()
    ]

    print(f"Before deduplication : {before_dedup:,}")
    print(f"Duplicates removed   : {duplicate_count:,}")
    print(f"Final sequences      : {len(processed_data):,}")

    # ---------------------------------------------------------
    # Save processed dataset
    # ---------------------------------------------------------

    print("\nSaving processed dataset...")

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "sequence",
            "ec_class",
            "length"
        ])

        for sequence, label in processed_data:
            writer.writerow([
                sequence,
                label,
                len(sequence)
            ])

    # ---------------------------------------------------------
    # Save preprocessing summary
    # ---------------------------------------------------------

    final_counts = Counter(
        label for _, label in processed_data
    )

    with open(
        SUMMARY_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "file",
            "ec_class",
            "original_sequences",
            "invalid_sequences",
            "short_sequences",
            "valid_sequences"
        ])

        for row in summary:
            writer.writerow([
                row["file"],
                row["ec_class"],
                row["original_sequences"],
                row["invalid_sequences"],
                row["short_sequences"],
                row["valid_sequences"]
            ])

    # ---------------------------------------------------------
    # Final report
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("PREPROCESSING COMPLETE")
    print("=" * 70)

    print(f"Original sequences : {total_original:,}")
    print(f"Invalid removed   : {total_invalid:,}")
    print(f"Short removed     : {total_short:,}")
    print(f"Duplicates removed: {duplicate_count:,}")
    print(f"Final sequences    : {len(processed_data):,}")

    print("\nFinal class distribution:")

    for label in sorted(final_counts):
        print(
            f"  EC {label}: {final_counts[label]:,}"
        )

    print("\nOutput files:")
    print(f"  {OUTPUT_FILE}")
    print(f"  {SUMMARY_FILE}")

    print("=" * 70)


if __name__ == "__main__":
    main()