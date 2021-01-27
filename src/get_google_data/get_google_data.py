import logging
import requests
import os
import configparser

config = configparser.ConfigParser()
#todo: This can't be right?
config_path = "../config.ini" if "test" in os.path.abspath(".").lower() else "config.ini"
config.read(config_path)
logging.getLogger(__name__)


def get_directions_data(origin: str, destination: str, mode: str, arrival_time: int) -> dict:
    """
    Dispatches query to google transit API
    Args:
        origin: Google supports many types, prefered is postal code
        destination: Google supports many types, prefered is postal code
        mode: "driving" or "transit"
        arrival_time: unix timestamp for arrival time

    Returns:
        dict: Json response from the google transit API
    """
    api_key = os.environ["GOOGLE_API_KEY"]
    url = config["General"]["google_transit_api_endpoint"]
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "arrival_time": arrival_time,
        "key": api_key,
    }

    req = requests.get(url, params=params)
    return req.json()
