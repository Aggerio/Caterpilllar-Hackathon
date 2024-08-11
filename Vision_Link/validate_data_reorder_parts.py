import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from constraints import get_failure_probability


load_dotenv()

# Connect to MongoDB
uri = os.environ['VISION_LINK_DB']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Vision_Link']
collection = db['inspection_data']

vehicle_id = "735EJBC9723"


latest_record = collection.find_one({"header.truck_serial_number": vehicle_id},sort=[("header.inspection_date", -1)])

if latest_record:
    print("Latest Record:")
    remaining_records = collection.find(
        {
            "header.truck_serial_number": vehicle_id,
            "_id": {"$ne": ObjectId(latest_record['_id'])}
        }
    )
    cumulative_probabilities = {
        "engine_oil_pressure": 0,
        "engine_speed": 0,
        "engine_temperature": 0,
        "brake_control": 0,
        "transmission_pressure": 0,
        "pedal_sensor": 0,
        "water_fuel": 0,
        "fuel_level": 0,
        "fuel_pressure": 0,
        "fuel_temperature": 0,
        "system_voltage": 0,
        "exhaust_gas_temperature": 0,
        "hydraulic_pump_rate": 0,
        "air_filter_pressure_drop": 0
    }
    print(f"Remaining Records for Vehicle ID: {vehicle_id}")
    record_count = 0
    for record in remaining_records:
        parameters = {
            "engine_oil_pressure": record["engine"]["engine_oil_pressure"],
            "engine_speed": record["engine"]["engine_speed"],
            "engine_temperature": record["engine"]["engine_temperature"],
            "brake_control": record["brakes"]["brake_control"],
            "transmission_pressure": record["transmission"]["transmission_pressure"],
            "pedal_sensor": record["brakes"]["pedal_sensor"],
            "water_fuel": record["engine"]["water_fuel"],
            "fuel_level": record["engine"]["fuel_level"],
            "fuel_pressure": record["engine"]["fuel_pressure"],
            "fuel_temperature": record["engine"]["fuel_temperature"],
            "system_voltage": record["battery"]["system_voltage"],
            "exhaust_gas_temperature": record["engine"]["exhaust_gas_temperature"],
            "hydraulic_pump_rate": record["engine"]["hydraulic_pump_rate"],
            "air_filter_pressure_drop": record["engine"]["air_filter_pressure_drop"]
        }
        failure_probs = get_failure_probability(parameters)
        for key, value in failure_probs.items():
            cumulative_probabilities[key] += value

        record_count += 1
    average_probabilities = {key: value / record_count for key, value in cumulative_probabilities.items()}
    print("Average Failure Probabilities:")
    for part, prob in average_probabilities.items():
        print(f"{part}: {prob:.2f}")



else:
    print("No records found.")
