from src.get_google_data import get_google_data, database_connect
from datetime import datetime, timedelta
import logging
import configparser
import random

config = configparser.ConfigParser()
config.read("config.ini")

origin_postcodes_path = config["Locations"]["origin_postcode_path"]
destination_postcodes_path = config["Locations"]["destination_postcode_path"]
postcode_limit = config["General"]["postcode_limit"]

db = database_connect.db_connect()
google_transit_collection = db["google_transit"]

with open(origin_postcodes_path, "r") as f:
    origin_postcodes = [line.strip() for line in f.readlines()]
with open(destination_postcodes_path, "r") as f:
    destination_postcodes = [line.strip() for line in f.readlines()]

arrival_time = None
today = datetime.now().replace(hour=8, minute=45, second=0)
for i in range(1, 8):
    candidate_date = today + timedelta(i)
    if candidate_date.weekday() == 2:
        arrival_time = int(datetime.timestamp(candidate_date))

if arrival_time is None:
    logging.error("arrival_time could not be determined")
    raise ValueError("arrival_time could not be determined")

random.shuffle(origin_postcodes)

for origin_postcode in origin_postcodes[postcode_limit:]:
    if not google_transit_collection.find_one({"origin_postcode": origin_postcode}):
        for destination_postcode in destination_postcodes:
            google_result_json = get_google_data.get_directions_data(
                origin=origin_postcode,
                destination=destination_postcode,
                mode="transit",
                arrival_time=arrival_time
            )
            google_result_json["origin_postcode"] = origin_postcode
            google_result_json["destination_postcode"] = destination_postcode
            google_result_json["mode"] = "transit"
            google_result_json["arrival_time"] = arrival_time

            google_transit_collection.insert_one(google_result_json)
