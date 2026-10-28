import joblib
import pandas as pd


ml = joblib.load('D:/vacancy-analytics/models/rf_model_100.joblib')
names =joblib.load('D:/vacancy-analytics/models/feature_names.joblib')

def predict_salary(input_data: dict) -> float:
    df = pd.DataFrame.from_dict([input_data])
    df = df[names]
    prediction = ml.predict(df)
    return prediction[0]


