"""
An original version of this project wrote the google transit results to the file system. I will write a pipe
to get them into MongoDB
"""
import os
import json
from src.get_google_data import database_connect
from tqdm import tqdm
import time

db = database_connect.db_connect()
google_transit_collection = db["google_transit"]

raw_file_directory = os.environ["backup_file_path"]

for file_name in tqdm(os.listdir(raw_file_directory)):
    try:
        if not google_transit_collection.find_one({"destination_postcode": file_name}):
            with open(os.path.join(raw_file_directory, file_name), "r") as f:
                original_data = json.loads(f.read())

            for destination_postcode in original_data.keys():
                if original_data[destination_postcode]["status"] != "ZERO_RESULTS":
                    original_data[destination_postcode]["origin_postcode"] = file_name
                    original_data[destination_postcode]["destination_postcode"] = destination_postcode

                    travel_modes = {step["travel_mode"] for step in (
                        original_data[destination_postcode]
                        ["routes"]
                        [0]
                        ["legs"]
                        [0]
                        ["steps"]
                    )}

                    original_data[destination_postcode]["mode"] = "TRANSIT" if "TRANSIT" in travel_modes else "DRIVING"

                    journey_detail = (
                        original_data[destination_postcode]
                        ["routes"]
                        [0]
                        ["legs"]
                        [0]
                    )

                    original_data[destination_postcode]["arrival_time"] = (journey_detail["arrival_time"]["value"]
                                                                           if "arrival_time" in journey_detail.keys()
                                                                           else None
                                                                           )

                    google_transit_collection.insert_one(original_data[destination_postcode])
                    # time.sleep(1)
    # except OSError:
    #     # print("IO Error", file_name)
    except:
        pass