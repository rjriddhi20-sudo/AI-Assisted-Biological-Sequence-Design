import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

train = pd.read_csv("data/processed/features_train.csv")

X_train = train.drop(columns=["ec_class"])
y_train = train["ec_class"]

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=25,
    min_samples_leaf=1,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Feature importance
importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    "importance",
    ascending=False
)

print("\nTOP 20 FEATURES:")
print(importance.head(20))

importance.to_csv(
    "data/processed/feature_importance.csv",
    index=False
)

joblib.dump(
    model,
    "data/processed/random_forest_final.joblib"
)

print("\nFinal model saved.")
print("Feature importance saved.")