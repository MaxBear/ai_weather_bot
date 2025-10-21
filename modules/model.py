import logging

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


class bot:

    cols = [
        "wind_kph",
        "pressure_mb",
        "precip_mm",
        "snow_cm",
        "avghumidity",
        "gust_kph",
    ]

    relevant_cols = cols + [
        "temp_c",
        "time_epoch",
    ]

    features = cols + [
        "day_of_year",
    ]

    def __init__(self, csv):
        self.csv = csv
        self.data = None
        self.model = None

    def load_data(self):
        # Load data
        data = pd.read_csv(self.csv)

        # Keep relevant columns
        data = data[bot.relevant_cols]

        data["date"] = pd.to_datetime(data["time_epoch"].astype("datetime64[s]"))
        data["wind_kph"] = pd.to_numeric(data["wind_kph"])

        # Example: use day of year as feature
        data["day_of_year"] = data["date"].dt.dayofyear

        self.data = data

    def train(self):
        self.load_data()
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() before training.")

        X = self.data[bot.features]
        y = self.data["temp_c"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Test model
        predictions = model.predict(X_test)
        logging.info(f"MSE: {mean_squared_error(y_test, predictions)}")

        self.model = model

    def predict(self, data):
        if self.model is None:
            raise ValueError("Model not trained. Call train() before prediction.")

        temp_pred = self.model.predict([data])[0]
        return temp_pred

    def plot(self):
        df = pd.DataFrame(self.data)

        df.plot(
            x="day_of_year",
            y=[
                "temp_c",
                "wind_kph",
                "pressure_mb",
                "precip_mm",
                "snow_cm",
                "avghumidity",
                "gust_kph",
            ],
            kind="line",
            marker="o",
            title="Weather observations over past 365 days, Markham, ON",
            markersize=1,
            subplots=True,
            figsize=(8, 10),
        )
        plt.tight_layout()
        plt.show()
