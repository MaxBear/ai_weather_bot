import time

import pytest

from modules.data import readAndSave


# only one year historical data is available for free plan
# the amount of time to retrieve one year data is around 0.4301 seconds
@pytest.fixture(params=[-365])
def days(request):
    return request.param


def test_readAndSave(days):
    start_time = time.perf_counter()
    readAndSave(num_days_from_now=days)
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"\nExecution time for readAndSave: {duration:.4f} seconds")
