import pandas as pd


def select_top_candidates(ranked_predictions, top_n=5):
    """
    Select the highest-ranked protein candidates.

    Parameters
    ----------
    ranked_predictions : pandas.DataFrame
        DataFrame produced by rank_predictions().

    top_n : int
        Number of candidates to select.

    Returns
    -------
    pandas.DataFrame
        Top-ranked candidates.
    """

    if ranked_predictions.empty:
        raise ValueError("No ranked predictions available.")

    if top_n <= 0:
        raise ValueError("top_n must be greater than 0.")

    return ranked_predictions.head(top_n).copy()
