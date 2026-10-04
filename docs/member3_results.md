# Member 3 - Model Development and Evaluation

## 1. Final Model
Random Forest Classifier

- n_estimators: 300
- max_depth: 25
- min_samples_leaf: 1
- class_weight: balanced
- random_state: 42

## 2. Final Test Performance

- Test Accuracy: 0.8085
- Macro F1: 0.8139
- Weighted F1: 0.8086

## 3. Feature Importance

The Random Forest feature importance analysis was performed
to identify the most influential features.

The most important feature was `length`, followed by amino-acid
features such as `aa_W`, `aa_L`, `aa_C`, `aa_F`, and others.

Feature importance data:
`data/processed/feature_importance.csv`

Feature importance plot:
`data/processed/feature_importance_top20.png`

## 4. Conclusion

The tuned Random Forest model achieved approximately 80.85%
test accuracy and a macro F1-score of 81.39%.

Feature importance analysis provides an interpretable view of
which sequence-derived features contribute most to classification.