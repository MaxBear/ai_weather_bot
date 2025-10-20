import requests
import pandas as pd
from datetime import date, timedelta, datetime
import time

api_key = ""
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
    print(f"Getting weather data for {dt} to {end_dt} at {loc}")
    last_epoch = None
    try:
        r = requests.get(
            "http://api.weatherapi.com/v1/history.json",
            params={"key": api_key, "q": loc, "dt": dt, "end_dt": end_dt},
        )
        res = r.json()
        for day in res.get("forecast", {}).get("forecastday", []):
            for hour in day.get("hour", []):
                for h in header_int:
                    d = hour.get(h)
                    if d == None:
                        d = "0"
                    data[h].append(int(d))
                    if h == "time_epoch":
                        data["datetime"].append(
                            datetime.fromtimestamp(d).strftime("%Y-%m-%d %H:%M:%S")
                        )
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
        print("\nResponse is not in JSON format.")
    return last_epoch


# Documentation for weather API schema
# https://www.weatherapi.com/docs/
def read(num_days_from_now=-30):
    data = {"datetime": []}
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
    dt = current_date + timedelta(days=num_days_from_now)

    # keep reading until will have num_days_from_now days of data
    while last_dt == None or last_dt < int(time.time()):
        last_dt = getWeatherForecast(
            data, dt.strftime("%Y-%m-%d"), date.today().strftime("%Y-%m-%d"), "L6E0S5"
        )
        dt = datetime.fromtimestamp(last_dt) + timedelta(days=1)

    df = pd.DataFrame(data)
    print(
        df.groupby(df["time_epoch"].map(lambda x: datetime.fromtimestamp(x).date()))[
            "time_epoch"
        ].agg("count")
    )

    df.to_csv("weather_data.csv", index=False)
