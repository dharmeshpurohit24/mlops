import joblib
from data_analysis import data_analysis
from model import predict_with_threshold

def predict():
    model = joblib.load("credit_card_fraud.pkl")

    features, labels = data_analysis()

    test_pos = 1
    sample = features.iloc[[test_pos]]
    actual = labels.iloc[test_pos]

    prediction = predict_with_threshold(model, sample, threshold=0.9)

    error = abs(prediction[0] - actual)

    print(f"Predicted : {prediction[0]}")
    print(f"Actual : {actual}")

if __name__ == "__main__":
    predict()