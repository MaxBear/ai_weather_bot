import http
import logging
import os
import time
from datetime import date, datetime, timedelta

import pandas as pd
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
api_key = os.getenv("API_KEY")

header_int = ["time_epoch"]
header_float = [
    "temp_c",
    "wind_kph",
    "wind_degree",
    "pressure_mb",
    "precip_mm",
    "snow_cm",
    "avghumidity",
    "gust_kph",
]
header_str = ["wind_dir"]


def getWeatherForecast(data, dt, end_dt, loc):
    logging.debug(f"Getting weather data for {dt} to {end_dt} at {loc}")
    last_epoch = None

    try:
        r = requests.get(
            "http://api.weatherapi.com/v1/history.json",
            params={"key": api_key, "q": loc, "dt": dt, "end_dt": end_dt},
        )
        if r.status_code != http.HTTPStatus.OK:
            logging.error(f"Error fetching data: {r.status_code} - {r.text}")
            return last_epoch
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return last_epoch

    try:
        res = r.json()
        for day in res.get("forecast", {}).get("forecastday", []):
            for hour in day.get("hour", []):
                for h in header_int:
                    d = hour.get(h)
                    logging.debug(
                        f"d: {d} {datetime.fromtimestamp(d).strftime("%Y-%m-%d %H:%M:%S")}"
                    )
                    if d == None:
                        d = "0"
                    data[h].append(int(d))
                    if h == "time_epoch":
                        if last_epoch is None or (
                            last_epoch is not None and d > last_epoch
                        ):
                            last_epoch = d
                for h in header_float:
                    d = hour.get(h)
                    if d == None:
                        d = "0.0"
                    data[h].append(float(d))
                for h in header_str:
                    d = hour.get(h)
                    if d == None:
                        d = ""
                    data[h].append(d)
    except requests.exceptions.JSONDecodeError:
        logging.error("\nResponse is not in JSON format.")

    return last_epoch


# Documentation for weather API schema
# https://www.weatherapi.com/docs/
def readAndSave(num_days_from_now=-365):
    data = {}
    for h in header_int:
        data[h] = []
    for h in header_float:
        data[h] = []
    for h in header_str:
        data[h] = []

    last_dt = None

    # Get the current date
    current_date = date.today()

    # Calculate the start date to read data from
    d0 = current_date + timedelta(days=num_days_from_now)
    dt = d0

    # keep reading until will have num_days_from_now days of data
    while last_dt == None or last_dt < int(time.time()):
        last_dt = getWeatherForecast(
            data, dt.strftime("%Y-%m-%d"), date.today().strftime("%Y-%m-%d"), "L6E0S5"
        )
        if last_dt is None:
            break
        dt = datetime.fromtimestamp(last_dt) + timedelta(days=1)

    if last_dt is None:
        logging.error("No data was retrieved.")
        return

    df = pd.DataFrame(data)
    logging.debug(
        df.groupby(df["time_epoch"].map(lambda x: datetime.fromtimestamp(x).date()))[
            "time_epoch"
        ].agg("count")
    )

    csv_fname = f"data/weather_data_{d0.strftime("%Y-%m-%d")}_{datetime.fromtimestamp(last_dt).strftime("%Y-%m-%d")}.csv"
    df.to_csv(csv_fname, index=False)

    logging.info(f"Data saved to {csv_fname}")

    return df
