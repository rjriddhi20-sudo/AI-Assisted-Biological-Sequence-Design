import csv
import os
import random
from collections import Counter

INPUT_FILE = "data/processed/protein_sequences.csv"
OUTPUT_DIR = "data/processed"

TRAIN_FILE = os.path.join(OUTPUT_DIR, "train.csv")
VALIDATION_FILE = os.path.join(OUTPUT_DIR, "validation.csv")
TEST_FILE = os.path.join(OUTPUT_DIR, "test.csv")

RANDOM_SEED = 42

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15


def load_dataset():
    data = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data.append({
                "sequence": row["sequence"],
                "ec_class": row["ec_class"],
                "length": row["length"]
            })

    return data


def stratified_split(data):

    # Group sequences by EC class
    class_data = {}

    for row in data:
        label = row["ec_class"]

        if label not in class_data:
            class_data[label] = []

        class_data[label].append(row)

    train = []
    validation = []
    test = []

    random.seed(RANDOM_SEED)

    for label in sorted(class_data):

        samples = class_data[label]

        random.shuffle(samples)

        total = len(samples)

        train_end = int(total * TRAIN_RATIO)
        validation_end = train_end + int(total * VALIDATION_RATIO)

        train.extend(samples[:train_end])
        validation.extend(samples[train_end:validation_end])
        test.extend(samples[validation_end:])

    # Shuffle each final dataset
    random.shuffle(train)
    random.shuffle(validation)
    random.shuffle(test)

    return train, validation, test


def save_dataset(filename, data):

    with open(
        filename,
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

        for row in data:
            writer.writerow([
                row["sequence"],
                row["ec_class"],
                row["length"]
            ])


def print_distribution(name, data):

    counts = Counter(
        row["ec_class"]
        for row in data
    )

    print(f"\n{name}")
    print("-" * 40)

    print(f"Total: {len(data):,}")

    for label in sorted(counts):

        percentage = (
            counts[label] / len(data) * 100
        )

        print(
            f"EC {label}: "
            f"{counts[label]:,} "
            f"({percentage:.2f}%)"
        )


def main():

    print("=" * 70)
    print("STRATIFIED DATASET SPLIT")
    print("=" * 70)

    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: File not found: {INPUT_FILE}")
        return

    data = load_dataset()

    print(f"\nTotal dataset: {len(data):,}")

    train, validation, test = stratified_split(data)

    print_distribution("TRAINING SET", train)
    print_distribution("VALIDATION SET", validation)
    print_distribution("TEST SET", test)

    save_dataset(TRAIN_FILE, train)
    save_dataset(VALIDATION_FILE, validation)
    save_dataset(TEST_FILE, test)

    print("\n" + "=" * 70)
    print("SPLIT COMPLETE")
    print("=" * 70)

    print(f"\nTraining   : {len(train):,}")
    print(f"Validation : {len(validation):,}")
    print(f"Testing    : {len(test):,}")

    print("\nFiles created:")

    print(f"  {TRAIN_FILE}")
    print(f"  {VALIDATION_FILE}")
    print(f"  {TEST_FILE}")

    print("\nRandom seed:", RANDOM_SEED)

    print("=" * 70)


if __name__ == "__main__":
    main()