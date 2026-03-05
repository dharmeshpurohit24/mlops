from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

import matplotlib.pyplot as plt
import numpy as np

from data_analysis import data_analysis
import joblib

def model_creation():
    features, labels = data_analysis()

    train_features,test_features,train_label, test_label = train_test_split(
        features, labels, test_size=0.2 ,random_state = 42
    )

    # n = 100
    # Model Performance:
    #     Mean Average Error : 0.9456
    #     Mean Squared Error : 10.8902
    #     Root Mean Squared Error : 3.3000
    #     R2 : 0.9608

    # n = 200
    # Model Performance:
    #     Mean Average Error : 0.9418
    #     Mean Squared Error : 10.8108
    #     Root Mean Squared Error : 3.2880
    #     R2 : 0.9611

    # n = 300
    # Model Performance:
    #     Mean Average Error : 0.9422
    #     Mean Squared Error : 10.8021
    #     Root Mean Squared Error : 3.2867
    #     R2 : 0.9611

    # n = 400
    # Model Performance:
    #     Mean Average Error : 0.9395
    #     Mean Squared Error : 10.7216
    #     Root Mean Squared Error : 3.2744
    #     R2 : 0.9614

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(n_estimators=400, random_state=42))
    ])

    pipeline.fit(train_features, train_label)

    joblib.dump(pipeline, "taxi_fare_prediction.pkl")

    test_results = pipeline.predict(test_features)

    mean_avg_error = mean_absolute_error(test_label, test_results)
    mean_sq_error = mean_squared_error(test_label, test_results)
    root_mean_sq_error = np.sqrt(mean_sq_error)
    r2 = r2_score(test_label, test_results)

    print(
        f"Model Performance:\n"
        f"Mean Average Error : {mean_avg_error:.4f}\n"
        f"Mean Squared Error : {mean_sq_error:.4f}\n"
        f"Root Mean Squared Error : {root_mean_sq_error:.4f}\n"
        f"R2 : {r2:.4f}"
    )

    plt.scatter(
        test_results, test_label, s=20, alpha=0.5
    )

    plt.title("Taxi Fare Prediction: Actual vs Predicted")
    plt.xlabel("Predicted Fare")
    plt.ylabel("Actual Fare")
    plt.savefig("linear_regression.png")


if __name__ == "__main__":
    model_creation()
