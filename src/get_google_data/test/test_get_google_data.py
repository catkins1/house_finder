import pytest
from datetime import datetime, timedelta
from src.get_google_data import get_google_data

arrival_time = None
today = datetime.now().replace(hour=8, minute=45, second=0)
for i in range(1, 8):
    candidate_date = today + timedelta(i)
    if candidate_date.weekday() == 2:
        arrival_time = int(datetime.timestamp(candidate_date))


# "SW5 0AD", "EC4A 2AH"

@pytest.mark.parametrize("mode", ["transit", "driving"])
def test_get_directions_data_null_origin(mode):
    result = get_google_data.get_directions_data(
        origin=None,
        destination="EC4A 2AH",
        mode=mode,
        arrival_time=arrival_time
    )
    assert result["status"] == 'INVALID_REQUEST'


@pytest.mark.parametrize("mode", ["transit", "driving"])
def test_get_directions_data_null_destination(mode):
    result = get_google_data.get_directions_data(
        origin="EC4A 2AH",
        destination=None,
        mode=mode,
        arrival_time=arrival_time
    )
    assert result["status"] == 'INVALID_REQUEST'


def test_get_directions_data_unlikely_time():
    result = get_google_data.get_directions_data(
        origin="EC4A 2AH",
        destination="SW5 0AD",
        mode="transit",
        arrival_time=4
    )
    print(result)
    assert result["status"] == 'ZERO_RESULTS'


def test_get_directions_data():
    result = get_google_data.get_directions_data(
        origin="EC4A 2AH",
        destination="SW5 0AD",
        mode="transit",
        arrival_time=arrival_time
    )
    print(result)
    assert result["status"] == 'OK'
