import pandas as pd
import matplotlib.pyplot as plt

# Load feature importance
df = pd.read_csv("data/processed/feature_importance.csv")

# Top 20 features
top20 = df.head(20).sort_values("importance")

# Plot
plt.figure(figsize=(10, 8))

plt.barh(
    top20["feature"],
    top20["importance"]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 20 Feature Importance - Random Forest")

plt.tight_layout()

# Save graph
plt.savefig(
    "data/processed/feature_importance_top20.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Feature importance graph saved.")