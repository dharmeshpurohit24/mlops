from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

import mlflow
import mlflow.sklearn

from data_analysis import data_analysis

def evaluate_model(model, train_x, train_y, test_x, test_y):
    pipeline = Pipeline([
        ("vectorizer", CountVectorizer()),
        ("model", model)
    ])
    pipeline.fit(train_x, train_y)
    predictions = pipeline.predict(test_x)

    metrics = {
        "accuracy": accuracy_score(test_y, predictions),
        "precision": precision_score(test_y, predictions),
        "recall": recall_score(test_y, predictions),
        "f1_score": f1_score(test_y, predictions)
    }
    return pipeline, metrics

def model_training(experiment_name):
    mlflow.set_experiment(experiment_name)

    features, labels = data_analysis()

    train_x, test_x, train_y, test_y = train_test_split(
        features, labels, test_size=0.2, random_state=42
    )

    models = {
        "LogisticRegression": LogisticRegression(class_weight="balanced", random_state=42),
        "SVM": SVC(kernel="linear", class_weight="balanced", probability=True, random_state=42),
        "NaiveBayes": MultinomialNB()
    }

    best_accuracy = 0
    best_run_id = None

    for model_name, model in models.items():
        with mlflow.start_run(run_name=model_name) as run:
            mlflow.log_param("model_name", model_name)
            for param, value in model.get_params().items():
                mlflow.log_param(param, value)

            pipeline, metrics = evaluate_model(model, train_x, train_y, test_x, test_y)

            for metric_name, value in metrics.items():
                mlflow.log_metric(metric_name, value)

            mlflow.sklearn.log_model(pipeline, name="model")

            if metrics["accuracy"] > best_accuracy:
                best_accuracy = metrics["accuracy"]
                best_run_id = run.info.run_id

            print(f"\n{model_name}")
            for metric_name, value in metrics.items():
                print(f"{metric_name}: {value}")

    if best_run_id:
        model_uri = f"runs:/{best_run_id}/model"
        mlflow.register_model(model_uri, experiment_name)

if __name__ == "__main__":
    model_training(experiment_name = "Spam_detection")