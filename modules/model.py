from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import pandas as pd


def train(pf):
    pd.to_datetime(pf["datetime"])

    # Define features and target
    X = pf[
        [
            "wind_kph",
            "gust_kph",
            "pressure_mb",
            "precip_mm",
            "snow_cm",
            "avghumidity",
            "epoc",
        ]
    ]
    y = pf["temp_c"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Test model
    predictions = model.predict(X_test)
    print("MSE:", mean_squared_error(y_test, predictions))

    return model
