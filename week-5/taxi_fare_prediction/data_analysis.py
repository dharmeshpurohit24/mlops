# dataset link: https://download.mlcc.google.com/mledu-datasets/chicago_taxi_train.csv

import pandas as pd

data_file_path = "chicago_taxi_train.csv"
# data_file_path = "test.csv"

def data_analysis():
    df = pd.read_csv(data_file_path)

    # print("\nData Info:-\n")
    # df.info()

    # print(f"Overall dataset null values info:-\n")
    # print(f"{df.isnull().sum()}")

    # features = ('TRIP_MILES', 'TRIP_SECONDS', 'FARE', 'TIP_RATE', 'TRIP_SPEED')
    # feature_selected = df.loc[:, features]

    # print("Features selected for further analysis:-\n")
    # print(f"{feature_selected.head()}")

    # print("The label (Fare) want to predict info:-\n")
    # print(f"{feature_selected['FARE'].describe()}")

    # print("Checking for any null value in selected features:-\n")
    # print(f"{feature_selected.isnull().sum()}")

    # print("Correlation matrix for features (numeric value only):-\n")
    # print(f"{feature_selected.corr(numeric_only=True)}")

    #  ==================================== Keeping the Columns =============================================

    # Model Performance:
    #     Mean Average Error : 1.2395
    #     Mean Squared Error : 11.4478
    #     Root Mean Squared Error : 3.3835
    #     R2 : 0.9588

    label = df['FARE']

    df = df.drop(columns=[
        'FARE',
        'TRIP_TOTAL',
    ])

    df['TRIP_START_TIMESTAMP'] = pd.to_datetime(df['TRIP_START_TIMESTAMP'], format='%m/%d/%Y %I:%M:%S %p')
    df['TRIP_END_TIMESTAMP'] = pd.to_datetime(df['TRIP_END_TIMESTAMP'], format='%m/%d/%Y %I:%M:%S %p')

    df['START_DAY'] = df['TRIP_START_TIMESTAMP'].dt.day
    df['START_MONTH'] = df['TRIP_START_TIMESTAMP'].dt.month
    df['START_WEEKDAY'] = df['TRIP_START_TIMESTAMP'].dt.weekday

    df = df.drop(columns=['TRIP_START_TIMESTAMP', 'TRIP_END_TIMESTAMP'])

    df = pd.get_dummies(df, drop_first=True)
    df = df.fillna(0)
    features = df

    #  ==================================== Keeping the columns =============================================

    #  ==================================== Removing the columns =============================================

    # Model Performance:
    #     Mean Average Error : 1.2064
    #     Mean Squared Error : 12.9929
    #     Root Mean Squared Error : 3.6046
    #     R2 : 0.9561

    # features = df[['TRIP_MILES', 'TRIP_SECONDS']]
    # label = df['FARE']

    #  ==================================== Removing the columns =============================================

    return features,label

if __name__ == "__main__":
    data_analysis()