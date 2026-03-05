from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

import matplotlib.pyplot as plt
import numpy as np

from data_analysis import data_analysis
import joblib

def model_creation():
    features, labels = data_analysis()

    train_features,test_features,train_label, test_label = train_test_split(
        features, labels, test_size=0.2 ,random_state = 42
    )

    model = GradientBoostingRegressor(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=4,
        loss='huber',
        random_state=42
    )

    model.fit(train_features, train_label)

    store = {
        "model": model,
        "features": train_features.columns.to_list()
    }

    joblib.dump(store, "house_rent_model.pkl")

    test_results = model.predict(test_features)

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
        test_label, test_results, s=20, alpha=0.5
    )

    plt.title("House Rent Prediction: Actual vs Predicted")
    plt.xlabel("Actual Rent")
    plt.ylabel("Predicted Rent")
    plt.savefig("Linear_regression.png")


if __name__ == "__main__":
    model_creation()
