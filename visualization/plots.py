import matplotlib.pyplot as plt
import pandas as pd


def plot_class_probabilities(probabilities):
    """
    Create a bar chart showing the model probability
    for each EC class.
    """

    classes = [f"EC {class_id}" for class_id in probabilities.keys()]
    values = list(probabilities.values())

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(classes, values)

    ax.set_title("EC Class Prediction Probabilities")
    ax.set_xlabel("EC Class")
    ax.set_ylabel("Probability")
    ax.set_ylim(0, 1)

    for index, value in enumerate(values):
        ax.text(
            index,
            value + 0.02,
            f"{value:.2f}",
            ha="center"
        )

    fig.tight_layout()

    return fig


def plot_candidate_scores(ranked_predictions):
    """
    Create a bar chart showing candidate scores.
    """

    if ranked_predictions.empty:
        raise ValueError("No ranked predictions available.")

    df = ranked_predictions.copy()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        df["sequence_id"].astype(str),
        df["score"]
    )

    ax.set_title("Candidate Ranking Scores")
    ax.set_xlabel("Candidate")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 100)

    fig.tight_layout()

    return fig