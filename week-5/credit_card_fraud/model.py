# imported libraries

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from data_analysis import data_analysis
import joblib

def predict_with_threshold(model, X, threshold=0.5):
    probs = model.predict_proba(X)[:, 1]
    return (probs >= threshold).astype(int)


def model_creation():
    features, labels = data_analysis()

    train_feature,test_feature,train_label, test_label = train_test_split(
        features, labels, test_size=0.2, stratify=labels ,random_state = 42
    )

    pipeline = Pipeline([
        ("scale", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])

    pipeline.fit(train_feature,train_label)

    joblib.dump(pipeline, "credit_card_fraud.pkl")

    predictions = predict_with_threshold(pipeline, test_feature, threshold=0.9)

    #  ==================================== Checking threshold =============================================

    # probs = pipeline.predict_proba(test_feature)[:,1]

    # for threshold in [0.5, 0.6, 0.7, 0.8, 0.9]:
    #     preds = (probs > threshold).astype(int)
    #     print(f"\nThreshold: {threshold}")
    #     print("Precision:", precision_score(test_label, preds))
    #     print("Recall   :", recall_score(test_label, preds))

    #  ==================================== Checking threshold =============================================

    accuracy = accuracy_score(test_label, predictions)
    precision = precision_score(test_label, predictions)
    recall = recall_score(test_label, predictions)
    f1 = f1_score(test_label, predictions)

    print("\nModel Evaluation Metrics:-\n")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

if __name__ == "__main__":
    model_creation()