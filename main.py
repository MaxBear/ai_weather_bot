import logging

from modules.model import bot

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    wbot = bot("data/weather_data_2024-10-21_2025-10-21.csv")
    wbot.load_data()
    wbot.plot()
