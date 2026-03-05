# dataset link: https://www.kaggle.com/datasets/shantanudhakadd/email-spam-detection-dataset-classification

import pandas as pd
from pathlib import Path

base_path = Path(__file__).parent
train_data = base_path / "spam.csv"

def data_analysis():
    df = pd.read_csv(train_data)
    # df.info()

    # print(df["Category"].value_counts())

    #  ==================================== balancing the class manually =============================================
    
    # Metrix balancing class manually :- 
        # LogisticRegression
        # Accuracy:  0.9331103678929766
        # Precision:  0.9652777777777778
        # Recall:  0.9025974025974026
        # F1 score:  0.9328859060402684
        
    # spam = df[df["Category"]=="spam"]
    # not_spam = df[df["Category"] == "ham"]

    # sampling_not_spam = not_spam.sample(n=747)

    # concatnated_data = pd.concat([sampling_not_spam,spam],axis=0)

    # print("data: ",concatnated_data["Category"].value_counts())

    # concatnated_data["Category"] = concatnated_data["Category"].map({"spam": 1, "ham": 0})
    # features = concatnated_data["Messages"]
    # labels = concatnated_data["Category"]

    #  ==================================== balancing the class manually =============================================


    df["Category"] = df["Category"].map({"spam": 1, "ham": 0})

    labels = df["Category"]
    features = df["Messages"]

    return features, labels

if __name__ == "__main__":
    data_analysis()