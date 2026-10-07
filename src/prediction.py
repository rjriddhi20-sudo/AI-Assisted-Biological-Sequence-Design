import joblib
import pandas as pd
from pathlib import Path
import streamlit as st


# Standard 20 amino acids used by Member 2
AMINO_ACIDS = list("ACDEFGHIKLMNPQRSTVWY")

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "random_forest_final.joblib"


# EC class names
EC_CLASSES = {
    1: "Oxidoreductases",
    2: "Transferases",
    3: "Hydrolases",
    4: "Lyases",
    5: "Isomerases",
    6: "Ligases",
    7: "Translocases",
}


def validate_sequence(sequence):
    """
    Validate a protein sequence using the same
    standard 20-amino-acid alphabet used in preprocessing.
    """

    sequence = sequence.strip().upper()

    if not sequence:
        raise ValueError("Protein sequence cannot be empty.")

    invalid = sorted(set(sequence) - set(AMINO_ACIDS))

    if invalid:
        raise ValueError(
            f"Invalid amino-acid characters found: {', '.join(invalid)}"
        )

    if len(sequence) < 20:
        raise ValueError(
            "Protein sequence must contain at least 20 amino acids."
        )

    return sequence


def extract_features(sequence):
    """
    Convert a protein sequence into the same
    21 features used by Member 2 and Member 3.
    """

    sequence = validate_sequence(sequence)
    length = len(sequence)

    features = {}

    for aa in AMINO_ACIDS:
        features[f"aa_{aa}"] = sequence.count(aa) / length

    features["length"] = length

    return pd.DataFrame([features])

@st.cache_resource
def load_model():
    """
    Load Member 3's trained Random Forest model.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict_sequence(sequence):
    """
    Predict the top-level EC class for a protein sequence.
    """

    features = extract_features(sequence)

    model = load_model()

    predicted_class = int(model.predict(features)[0])

    probabilities = model.predict_proba(features)[0]

    probability_dict = {
        int(cls): float(prob)
        for cls, prob in zip(model.classes_, probabilities)
    }

    return {
        "predicted_class": predicted_class,
        "class_name": EC_CLASSES[predicted_class],
        "confidence": probability_dict[predicted_class],
        "probabilities": probability_dict,
        "sequence_length": len(sequence),
    }