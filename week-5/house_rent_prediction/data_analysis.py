# dataset link: https://www.kaggle.com/datasets/iamsouravbanerjee/house-rent-prediction-dataset?resource=download&select=House_Rent_Dataset.csv

import pandas as pd
import numpy as np

data_file_path = "House_Rent_Dataset.csv"

def data_analysis():
    df = pd.read_csv(data_file_path)

    # print(f"\nDataset Info:-\n{df.head()}")
    # print(f"\nOverall dataset null values info:-\n")
    # print(f"{df.isnull().sum()}")

    # df.info()

    # print("\nThe label (Rent) want to predict info:-\n")
    # print(f"Min Rent: {df['Rent'].min()}")
    # print(f"Max Rent: {df['Rent'].max()}\n")

    # print(f"Min BHK: {df['BHK'].min()}\n")
    # print(f"Max BHK: {df['BHK'].max()}\n")

    # print(f"{df.isnull().sum()}")

    #  ==================================== Removed the Col =============================================

    # Model Performance:- (removing the POC and PO column)
    #     Mean Average Error : 4042.8185
    #     Mean Squared Error : 46828831.6216
    #     Root Mean Squared Error : 6843.1595
    #     R2 : 0.8977

    df = df.drop(
        columns=["Point of Contact", "Posted On"],
        errors="ignore"
    )

    #  ==================================== Removed the Col =============================================

    #  ==================================== Keeping the Col =============================================

    # Model Performance: (Keeping the POC and PO column)
    #     Mean Average Error : 4114.2782
    #     Mean Squared Error : 50655521.3733
    #     Root Mean Squared Error : 7117.2692
    #     R2 : 0.8893

    # df["Posted On"] = pd.to_datetime(df['Posted On'])
    # df['year'] = df['Posted On'].dt.year
    # df['month'] = df['Posted On'].dt.month
    # df['day'] = df['Posted On'].dt.day
    # df['day_of_week'] = df['Posted On'].dt.dayofweek
    # df.drop('Posted On', axis=1, inplace=True)

    # # print(df["Point of Contact"].value_counts())
    # df = pd.get_dummies(
    #     df,
    #     columns=["Point of Contact"],
    #     drop_first=True
    # )

    #  ==================================== Keeping the Col =============================================

    # print((df["Area Locality"].value_counts() > 2).sum())
    counts = df["Area Locality"].value_counts()
    rare_localities = counts[counts <= 2].index

    df["Area Locality"] = df["Area Locality"].replace(rare_localities, "Other")
    # locality_mean = df.groupby("Area Locality")["Rent"].mean()

    # df["Locality_encoded"] = df["Area Locality"].map(locality_mean)

    # df = df.drop("Area Locality", axis=1)

    def extract_floor(floor_str):
        if "Ground" in floor_str:
            return 0.0
        try:
            parts = floor_str.split(" out of ")
            current = int(parts[0].split(" ")[0])
            total = int(parts[1])
            return current / total
        except Exception:
            return 0.0

    df["Floor"] = df["Floor"].apply(extract_floor)

    df = pd.get_dummies(
        df,
        columns=["Area Type", "City", "Furnishing Status", "Tenant Preferred", "Area Locality"],
        drop_first=True
    )

    # print(df["Rent"].min())
    # print(df["Rent"].mean())
    # print(df["Rent"].max())
    df = df[df['Rent'] < df['Rent'].quantile(0.90)]

    # print(df.columns)
    # print("Correlation matrix for features:-\n")
    # corr_with_rent = df.corr(numeric_only=True)["Rent"].sort_values(ascending=False)
    # print(corr_with_rent)

    features = df.drop("Rent", axis=1)
    label = df['Rent']

    return features,label

if __name__ == "__main__":
    data_analysis()