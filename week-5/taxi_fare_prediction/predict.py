import joblib
from data_analysis import data_analysis

# For prediction use the test.csv file (take 10 datapoints from main dataset and put it in new file and update in data_analysis)
def predict():
    model = joblib.load("taxi_fare_prediction.pkl")

    features, labels = data_analysis()

    # Only can check for position: 0 - 8
    test_pos = 2
    sample = features.iloc[[test_pos]]

    prediction = model.predict(sample)
    actual = labels.iloc[test_pos]

    error = abs(prediction[0] - actual)

    print(f"Predicted Fare: {prediction[0]: .2f}")
    print(f"Actual Fare: {actual: .2f}")
    print(f"Error: {error: .2f}")

if __name__ == "__main__":
    predict()