import pandas as pd


def calculate_candidate_score(confidence):
    """
    Calculate a candidate score from model confidence.

    Confidence is expected as a value between 0 and 1.
    The returned score is expressed from 0 to 100.
    """

    if not 0 <= confidence <= 1:
        raise ValueError("Confidence must be between 0 and 1.")

    return confidence * 100


def rank_predictions(predictions):
    """
    Rank predicted protein candidates by model confidence.

    Parameters
    ----------
    predictions : list of dictionaries
        Prediction results returned by predict_sequence().

    Returns
    -------
    pandas.DataFrame
        Predictions ranked from highest to lowest confidence.
    """

    if not predictions:
        raise ValueError("No predictions were provided.")

    df = pd.DataFrame(predictions)

    if "confidence" not in df.columns:
        raise ValueError("Prediction data must contain 'confidence'.")

    df["score"] = df["confidence"].apply(calculate_candidate_score)

    df = df.sort_values(
        by="score",
        ascending=False
    ).reset_index(drop=True)

    df.insert(0, "rank", range(1, len(df) + 1))

    return df