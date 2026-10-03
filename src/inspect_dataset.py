import gzip
import csv
import re
from pathlib import Path
from collections import Counter


# Project folders
RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("dataset_info.csv")

# Standard amino-acid letters
VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def inspect_fasta_gz(file_path):
    """
    Inspect one compressed UniProt FASTA file
    without modifying the original file.
    """

    sequence_count = 0
    sequence_lengths = []
    sequence_ids = []
    organisms = []
    sequences_seen = set()

    invalid_characters = Counter()

    current_sequence = []
    current_id = None

    with gzip.open(file_path, "rt", encoding="utf-8") as handle:

        for line in handle:
            line = line.strip()

            if not line:
                continue

            # FASTA header
            if line.startswith(">"):

                # Save previous sequence
                if current_id is not None:
                    sequence = "".join(current_sequence)

                    sequence_count += 1
                    sequence_lengths.append(len(sequence))
                    sequences_seen.add(sequence)

                    invalid_characters.update(
                        set(sequence) - VALID_AMINO_ACIDS
                    )

                # Start new record
                current_sequence = []

                header = line[1:]

                # UniProt accession
                accession_match = re.search(
                    r"\|([^|]+)\|",
                    header
                )

                if accession_match:
                    current_id = accession_match.group(1)
                else:
                    current_id = header.split()[0]

                sequence_ids.append(current_id)

                # Organism
                organism_match = re.search(
                    r"OS=([^=]+?)(?:\sOX=|\sGN=|\sPE=|\sSV=|$)",
                    header
                )

                if organism_match:
                    organisms.append(
                        organism_match.group(1).strip()
                    )
                else:
                    organisms.append("Unknown")

            else:
                current_sequence.append(line)

        # Save final sequence
        if current_id is not None:
            sequence = "".join(current_sequence)

            sequence_count += 1
            sequence_lengths.append(len(sequence))
            sequences_seen.add(sequence)

            invalid_characters.update(
                set(sequence) - VALID_AMINO_ACIDS
            )

    # Calculate statistics
    minimum_length = min(sequence_lengths) if sequence_lengths else 0
    maximum_length = max(sequence_lengths) if sequence_lengths else 0

    average_length = (
        sum(sequence_lengths) / len(sequence_lengths)
        if sequence_lengths
        else 0
    )

    return {
        "file": file_path.name,
        "sequence_count": sequence_count,
        "unique_sequences": len(sequences_seen),
        "min_length": minimum_length,
        "max_length": maximum_length,
        "average_length": round(average_length, 2),
        "invalid_characters": "".join(
            sorted(invalid_characters.keys())
        ),
        "sample_ids": ", ".join(sequence_ids[:5]),
        "sample_organisms": ", ".join(
            dict.fromkeys(organisms[:5])
        ),
    }


def main():

    print("=" * 70)
    print("UniProt Protein Dataset Inspection")
    print("=" * 70)

    files = sorted(RAW_DIR.glob("*.fasta.gz"))

    if not files:
        print("\nERROR: No .fasta.gz files found in data/raw/")
        return

    print(f"\nFound {len(files)} FASTA files.\n")

    results = []

    for file_path in files:

        print(f"Inspecting: {file_path.name}")

        try:
            result = inspect_fasta_gz(file_path)
            results.append(result)

            print(
                f"  Sequences       : {result['sequence_count']:,}"
            )

            print(
                f"  Unique sequences: {result['unique_sequences']:,}"
            )

            print(
                f"  Min length      : {result['min_length']}"
            )

            print(
                f"  Max length      : {result['max_length']}"
            )

            print(
                f"  Average length  : {result['average_length']}"
            )

            print(
                f"  Invalid chars   : "
                f"{result['invalid_characters'] or 'None'}"
            )

            print()

        except Exception as error:
            print(f"  ERROR: {error}\n")

    # Save CSV
    if results:

        fieldnames = results[0].keys()

        with open(
            OUTPUT_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(results)

        print("=" * 70)
        print(f"Inspection complete.")
        print(f"Results saved to: {OUTPUT_FILE}")
        print("=" * 70)


if __name__ == "__main__":
    main()