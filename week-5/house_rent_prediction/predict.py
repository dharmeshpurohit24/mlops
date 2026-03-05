import joblib
from data_analysis import data_analysis


def predict():
    store = joblib.load("house_rent_model.pkl")
    model = store["model"]
    feature_columns = store["features"]

    features, labels = data_analysis()

    test_pos = 2
    sample = features.iloc[[test_pos]]
    actual = labels.iloc[test_pos]

    sample = sample.reindex(columns=feature_columns, fill_value=0)

    prediction = model.predict(sample)

    error = abs(prediction[0] - actual)

    print(f"Predicted Rent: {prediction[0]: .2f}")
    print(f"Actual Rent: {actual: .2f}")
    print(f"Error: {error: .2f}")

if __name__ == "__main__":
    predict()