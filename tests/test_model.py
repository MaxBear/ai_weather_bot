import pandas as pd
import pytest

from modules.model import bot


@pytest.fixture(params=["data/weather_data_2024-10-21_2025-10-21.csv"])
def csv(request):
    return request.param


def test_train(csv):
    wbot = bot(csv)
    wbot.load_data()
    assert wbot.data is not None
    wbot.train()
    assert wbot.model is not None
    data = [5.1, 998, 0, 0, 0, 4.1, 150]
    temp_pred = wbot.predict(data)
    print(f"Predicted temperature: {temp_pred:.2f}°C")
