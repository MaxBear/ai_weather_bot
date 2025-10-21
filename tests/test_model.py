import pandas as pd
import pytest

from modules.model import bot


@pytest.fixture(params=["data/weather_data_2024-10-21_2025-10-21.csv"])
def csv(request):
    return request.param


# Each datum used for test is composed of a tuple with the following fields
#     [
#         "wind_kph",
#         "pressure_mb",
#         "precip_mm",
#         "snow_cm",
#         "avghumidity",
#         "gust_kph",
#         "day_of_year",
#     ]
@pytest.mark.parametrize(
    "data",  # names of arguments
    [
        [10, 1001, 0, 1, 0, 25, 1],  # winter
        [10, 1001, 10, 0, 0, 25, 150],  # summer
        [10, 1001, 30, 0, 0, 0, 1],  # outlier
        [0, 0, 0, 0, 0, 0, 1],  # prediction based on day of year only
        [0, 0, 0, 0, 0, 0, 90],
        [0, 0, 0, 0, 0, 0, 180],
        [0, 0, 0, 0, 0, 0, 270],
        [0, 0, 0, 0, 0, 0, 350],
    ],
)
def test_train(csv, data):
    wbot = bot(csv)
    wbot.load_data()
    assert wbot.data is not None
    wbot.train()
    assert wbot.model is not None
    temp_pred = wbot.predict(data)
    print(f"Predicted temperature: {temp_pred:.2f}°C")
