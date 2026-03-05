import mlflow
import pandas as pd
from pathlib import Path

base_path = Path(__file__).parent
test_data = base_path / "test.csv"

def predict():
    features = pd.read_csv(test_data)["Messages"]

    model_uri = "runs:/259052adec904356afbcb8166e6345c8/model"
    model = mlflow.sklearn.load_model(model_uri)

    predictions = model.predict(features)
    results = pd.Series(predictions)
    result_label = results.map({1: "Spam", 0:"Ham"})

    print_result = pd.DataFrame({
        "Prediction": result_label,
        "Msg": features
    })

    print(print_result)

if __name__ == "__main__":
    predict()