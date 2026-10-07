import sys
from pathlib import Path

import streamlit as st
import pandas as pd

# Allow Python to find the project's src folder
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.prediction import predict_sequence
from src.ranking import rank_predictions
from src.candidate_selection import select_top_candidates
from visualization.plots import (
    plot_class_probabilities,
    plot_candidate_scores
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI-Assisted Biological Sequence Design",
    page_icon="🧬",
    layout="wide"
)


# --------------------------------------------------
# Project information
# --------------------------------------------------

EC_CLASSES = {
    1: "Oxidoreductases",
    2: "Transferases",
    3: "Hydrolases",
    4: "Lyases",
    5: "Isomerases",
    6: "Ligases",
    7: "Translocases",
}


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🧬 AI-Assisted Biological Sequence Design")

st.markdown(
    """
    ### Protein Sequence Classification and Candidate Ranking

    This application uses a trained **Random Forest classifier**
    to classify protein sequences into one of seven top-level
    Enzyme Commission (EC) classes.

    The application also displays prediction probabilities and
    ranks candidate sequences using model confidence.
    """
)

st.divider()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Project Overview",
        "Protein Prediction",
        "Candidate Ranking",
        "Methodology"
    ]
)


# ==================================================
# PROJECT OVERVIEW
# ==================================================

if page == "Project Overview":

    st.header("Project Overview")

    st.write(
        "The project develops an AI-assisted methodology for "
        "analysing and computationally classifying biological "
        "protein sequences."
    )

    st.subheader("Sequence Type")

    st.info("Protein amino-acid sequences")

    st.subheader("Prediction Task")

    st.write(
        "Given a protein sequence, predict its top-level "
        "Enzyme Commission (EC) class."
    )

    st.subheader("EC Classes")

    class_table = pd.DataFrame(
        {
            "EC Class": [
                "EC 1",
                "EC 2",
                "EC 3",
                "EC 4",
                "EC 5",
                "EC 6",
                "EC 7",
            ],
            "Category": list(EC_CLASSES.values()),
        }
    )

    st.dataframe(
        class_table,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("AI/ML Model")

    st.write("Random Forest Classifier")

    st.subheader("Model Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Test Accuracy", "80.85%")
    col2.metric("Macro F1", "81.39%")
    col3.metric("Weighted F1", "80.86%")


# ==================================================
# PROTEIN PREDICTION
# ==================================================

elif page == "Protein Prediction":

    st.header("Protein Sequence Prediction")

    st.write(
        "Enter a protein amino-acid sequence below to obtain "
        "an EC-class prediction."
    )

    sequence = st.text_area(
        "Protein Sequence",
        height=180,
        placeholder="Example: MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAN"
    )

    if st.button("Predict EC Class", type="primary"):

        if not sequence.strip():

            st.error("Please enter a protein sequence.")

        else:

            try:

                result = predict_sequence(sequence)

                st.success("Prediction completed successfully.")

                # ------------------------------
                # Main prediction
                # ------------------------------

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Predicted EC Class",
                    f"EC {result['predicted_class']}"
                )

                col2.metric(
                    "Class",
                    result["class_name"]
                )

                col3.metric(
                    "Confidence",
                    f"{result['confidence'] * 100:.2f}%"
                )

                st.divider()

                # ------------------------------
                # Sequence information
                # ------------------------------

                st.subheader("Sequence Information")

                st.write(
                    f"Sequence length: **{result['sequence_length']} "
                    f"amino acids**"
                )

                # ------------------------------
                # Probability distribution
                # ------------------------------

                st.subheader("Prediction Probabilities")

                probability_df = pd.DataFrame(
                    {
                        "EC Class": [
                            f"EC {class_id}"
                            for class_id in result["probabilities"]
                        ],
                        "Category": [
                            EC_CLASSES[class_id]
                            for class_id in result["probabilities"]
                        ],
                        "Probability": [
                            probability
                            for probability
                            in result["probabilities"].values()
                        ],
                    }
                )

                probability_df["Probability (%)"] = (
                    probability_df["Probability"] * 100
                ).round(2)

                st.dataframe(
                    probability_df,
                    use_container_width=True,
                    hide_index=True
                )

                # ------------------------------
                # Probability chart
                # ------------------------------

                fig = plot_class_probabilities(
                    result["probabilities"]
                )

                st.pyplot(fig)

            except ValueError as error:

                st.error(str(error))

            except Exception as error:

                st.error(
                    f"Prediction failed: {error}"
                )


# ==================================================
# CANDIDATE RANKING
# ==================================================

elif page == "Candidate Ranking":

    st.header("Candidate Sequence Ranking")

    st.write(
        "Enter multiple protein sequences to classify and rank "
        "them according to model confidence."
    )

    st.info(
        "Enter one protein sequence per line. "
        "Each sequence must contain at least 20 amino acids."
    )

    sequences_text = st.text_area(
        "Candidate Protein Sequences",
        height=250,
        placeholder=(
            "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAN\n"
            "MKKIGYSAR...\n"
            "MARGKKIG..."
        )
    )

    top_n = st.number_input(
        "Number of Top Candidates",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )

    if st.button("Rank Candidates", type="primary"):

        if not sequences_text.strip():

            st.error("Please enter at least one protein sequence.")

        else:

            # ------------------------------------------
            # Read sequences
            # ------------------------------------------

            sequences = [
                sequence.strip()
                for sequence in sequences_text.splitlines()
                if sequence.strip()
            ]

            predictions = []
            errors = []

            # ------------------------------------------
            # Predict each candidate
            # ------------------------------------------

            for index, sequence in enumerate(sequences, start=1):

                sequence_id = f"Candidate {index}"

                try:

                    result = predict_sequence(sequence)

                    predictions.append(
                        {
                            "sequence_id": sequence_id,
                            "predicted_class": result["predicted_class"],
                            "class_name": result["class_name"],
                            "confidence": result["confidence"],
                            "sequence_length": result["sequence_length"],
                        }
                    )

                except ValueError as error:

                    errors.append(
                        f"{sequence_id}: {error}"
                    )

                except Exception as error:

                    errors.append(
                        f"{sequence_id}: Prediction failed - {error}"
                    )

            # ------------------------------------------
            # Display validation errors
            # ------------------------------------------

            if errors:

                st.warning(
                    "Some candidate sequences could not be processed."
                )

                for error in errors:

                    st.write(f"- {error}")

            # ------------------------------------------
            # Rank valid predictions
            # ------------------------------------------

            if predictions:

                ranked_predictions = rank_predictions(
                    predictions
                )

                selected_candidates = select_top_candidates(
                    ranked_predictions,
                    top_n=int(top_n)
                )

                st.success(
                    f"{len(predictions)} candidate(s) processed successfully."
                )

                st.divider()

                # --------------------------------------
                # Ranking table
                # --------------------------------------

                st.subheader("Candidate Ranking")

                display_df = ranked_predictions[
                    [
                        "rank",
                        "sequence_id",
                        "predicted_class",
                        "class_name",
                        "sequence_length",
                        "confidence",
                        "score",
                    ]
                ].copy()

                display_df["predicted_class"] = (
                    "EC "
                    + display_df["predicted_class"].astype(str)
                )

                display_df["confidence"] = (
                    display_df["confidence"] * 100
                ).round(2)

                display_df["score"] = (
                    display_df["score"]
                ).round(2)

                display_df = display_df.rename(
                    columns={
                        "rank": "Rank",
                        "sequence_id": "Candidate",
                        "predicted_class": "EC Class",
                        "class_name": "Category",
                        "sequence_length": "Length",
                        "confidence": "Confidence (%)",
                        "score": "Score",
                    }
                )

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )

                csv_data = display_df.to_csv(index=False)

st.download_button(
    label="Download Ranking Results",
    data=csv_data,
    file_name="candidate_ranking_results.csv",
    mime="text/csv"
)

                # --------------------------------------
                # Top candidates
                # --------------------------------------

                st.subheader("Top Candidates")

                top_df = selected_candidates[
                    [
                        "rank",
                        "sequence_id",
                        "predicted_class",
                        "class_name",
                        "confidence",
                        "score",
                    ]
                ].copy()

                top_df["predicted_class"] = (
                    "EC "
                    + top_df["predicted_class"].astype(str)
                )

                top_df["confidence"] = (
                    top_df["confidence"] * 100
                ).round(2)

                top_df["score"] = (
                    top_df["score"]
                ).round(2)

                top_df = top_df.rename(
                    columns={
                        "rank": "Rank",
                        "sequence_id": "Candidate",
                        "predicted_class": "EC Class",
                        "class_name": "Category",
                        "confidence": "Confidence (%)",
                        "score": "Score",
                    }
                )

                st.dataframe(
                    top_df,
                    use_container_width=True,
                    hide_index=True
                )

                # --------------------------------------
                # Candidate ranking chart
                # --------------------------------------

                st.subheader("Candidate Ranking Scores")

                ranking_fig = plot_candidate_scores(
                    ranked_predictions
                )

                st.pyplot(ranking_fig)

                # --------------------------------------
                # Explanation
                # --------------------------------------

                st.info(
                    "Candidate score is based on the Random Forest "
                    "model's prediction confidence. It represents "
                    "computational model confidence and does not "
                    "represent experimental biological validity."
                )

            else:

                st.error(
                    "No valid candidate sequences were available "
                    "for prediction."
                )


# ==================================================
# METHODOLOGY
# ==================================================

elif page == "Methodology":

    st.header("Methodology")

    st.subheader("Overall Pipeline")

    st.markdown(
        """
        **Member 1 — Data Collection**

        UniProtKB / Swiss-Prot protein sequences

        ↓

        **Member 2 — Data Processing**

        Sequence preprocessing and amino-acid composition features

        ↓

        **Member 3 — AI/ML Analysis**

        Random Forest classification

        ↓

        **Member 4 — Integration**

        Prediction → probability analysis → candidate scoring →
        ranking → visualization
        """
    )

    st.subheader("Features Used")

    st.write(
        "The model uses 21 sequence-derived features:"
    )

    st.write(
        "20 amino-acid composition features + sequence length."
    )

    st.subheader("Model")

    st.write(
        """
        Random Forest Classifier

        - 300 trees
        - Maximum depth: 25
        - Minimum samples per leaf: 1
        - Balanced class weights
        - Random state: 42
        """
    )

    st.subheader("Important Limitation")

    st.warning(
        "The application provides computational predictions. "
        "These predictions do not constitute experimental biological "
        "validation."
    )