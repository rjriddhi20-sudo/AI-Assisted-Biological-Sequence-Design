import pandas as pd
from pathlib import Path

AMINO_ACIDS = list("ACDEFGHIKLMNPQRSTVWY")

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def extract_features(df):
    sequences = df["sequence"].astype(str)

    features = {}

    for aa in AMINO_ACIDS:
        features[f"aa_{aa}"] = sequences.str.count(aa) / sequences.str.len()

    features["length"] = df["length"].astype(int)

    feature_df = pd.DataFrame(features)

    feature_df["ec_class"] = df["ec_class"].astype(int).values

    return feature_df


def process_file(input_name, output_name):
    input_path = PROCESSED_DIR / input_name
    output_path = PROCESSED_DIR / output_name

    print(f"Reading: {input_name}")

    df = pd.read_csv(input_path)

    print(f"Sequences: {len(df):,}")

    feature_df = extract_features(df)

    feature_df.to_csv(output_path, index=False)

    print(f"Saved: {output_name}")
    print(f"Rows: {len(feature_df):,}")
    print(f"Features: {len(feature_df.columns) - 1}")
    print()


def main():
    process_file("train.csv", "features_train.csv")
    process_file("validation.csv", "features_validation.csv")
    process_file("test.csv", "features_test.csv")

    print("FEATURE EXTRACTION COMPLETE")


if __name__ == "__main__":
    main()
