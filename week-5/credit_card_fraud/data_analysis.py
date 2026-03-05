# dataset link: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud?select=creditcard.csv

import pandas as pd

data_file_path = "creditcard.csv"

def data_analysis():
    df = pd.read_csv(data_file_path)

    # print(f"Dataset Info:-\n{df.head()}")
    # print("\nData Info:-\n")
    # df.info()

    # print(f"\nNumeric col info:-\n{df.describe()}")

    # print(f"\nData set info:-\n{df.index}")
    # print(df.isnull().sum())

    # print(f"\nPrediction (label) analysis:-\n{df['Class'].value_counts()}")

    # print("\nThe dataset is unbalanced by a large no so will have to balance it\n")

    not_fraud = df[df['Class'] == 0]
    fraud = df[df['Class'] == 1]

    if len(df) < 100:
        concatenated_label  = df.copy()
    else:
        n_samples = min(len(not_fraud), len(fraud))
        label_not_fraud_trimmed = not_fraud.sample(n=n_samples, random_state=42)
        concatenated_label  = pd.concat([label_not_fraud_trimmed, fraud], axis=0)

    # print("\nBalanced dataset Info:-\n")
    # print(concatenated_label.head())
    # print(concatenated_label.tail())
    # print(f"\nPrediction (label) analysis:-\n{concatenated_label['Class'].value_counts()}")
    # print(concatenated_label.shape)

    features = concatenated_label.drop(columns='Class')
    label = concatenated_label['Class']

    return features,label

if __name__ == "__main__":
    data_analysis()