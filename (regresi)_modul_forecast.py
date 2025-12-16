import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_ml(df, col, days):
    X = df['timestamp'].map(pd.Timestamp.toordinal).values.reshape(-1,1)
    y = df[col].values

    model = LinearRegression()
    model.fit(X, y)

    future_dates = pd.date_range(df['timestamp'].max(), periods=days+1, freq='D')[1:]
    X_future = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1,1)

    return future_dates, model.predict(X_future), model.predict(X)
