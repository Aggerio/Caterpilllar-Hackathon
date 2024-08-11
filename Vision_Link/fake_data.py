import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from random import randint, choice, uniform
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Connect to MongoDB
uri = os.environ['VISION_LINK_DB']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Vision_Link']
collection = db['inspection_data']
customer_collection = db['customer_collection']

"""
# Define sample data for random selection
tire_conditions = ["Good", "Ok", "Needs Replacement"]
brake_conditions = ["Good", "Ok", "Needs Replacement"]
battery_makes = ["CAT", "ABC", "XYZ"]

# Insert 50 random records
truck_serial_number = "735EJBC9723"
truck_image = 'https://s7d2.scene7.com/is/image/Caterpillar/CM20210526-11e3c-618b2?$cc-s$'
truck_model = "735"
company_name = "CAT"
customer_name = "Ambuja Constructions"
cat_customer_id = "C123456"

start_date = datetime.now() - timedelta(days=5*365)

# collection.delete_many({})
for _ in range(50):
    inspection_date = start_date + timedelta(days=randint(0, 1825))  # Random date in 5 years
    
    # Randomly decide if this record should indicate a breakdown
    is_breakdown = choice([True, False, False, False])  # 25% chance for breakdown
    
    inspection_data = {
        "header": {
            "truck_serial_number": truck_serial_number,
            "truck_model": truck_model,
            "service_meter_hours": randint(1000, 10000),
            "customer_name": customer_name,
            "cat_customer_id": cat_customer_id,
            "inspection_date": inspection_date,
            "truck_image":truck_image
        },
        "tires": {
            "tire_pressure_left_front": uniform(28.0, 35.0),
            "tire_pressure_right_front": uniform(28.0, 35.0),
            "tire_condition_left_front": choice(tire_conditions),
            "tire_condition_right_front": choice(tire_conditions),
            "tire_pressure_left_rear": uniform(28.0, 35.0),
            "tire_pressure_right_rear": uniform(28.0, 35.0),
            "tire_condition_left_rear": choice(tire_conditions),
            "tire_condition_right_rear": choice(tire_conditions),
            "overall_tire_summary": "All tires are in acceptable condition." if not is_breakdown else "Tire breakdown detected.",
            "attached_images": [
                "left_front.jpg",
                "right_front.jpg",
                "left_rear.jpg",
                "right_rear.jpg"
            ]
        },
        "battery": {
            "battery_make": choice(battery_makes),
            "battery_replacement_date": (inspection_date - timedelta(days=randint(0, 365))).strftime('%Y-%m-%d'),
            "battery_voltage": f"{uniform(12.0, 14.0):.1f}V",
            "battery_water_level": choice(["Good", "Ok", "Low"]) if not is_breakdown else "Low",
            "system_voltage": uniform(11.0,30.0)
        },
        "brakes": {
            "brake_fluid_level": choice(["Good", "Ok", "Low"]),
            "brake_condition_front": choice(brake_conditions) if not is_breakdown else "Needs Replacement",
            "brake_condition_rear": choice(brake_conditions) if not is_breakdown else "Needs Replacement",
            "emergency_brake": choice(["Good", "Ok", "Low"]) if not is_breakdown else "Low",
            "brake_control": uniform(0.9,3.0),
            "pedal_sensor": uniform(0.0,1.0)
        },
        "engine": {
            "engine_oil_condition": choice(["Good", "Ok", "Needs Replacement"]) if not is_breakdown else "Needs Replacement",
            "brake_oil_condition": choice(["Good", "Ok", "Needs Replacement"]) if not is_breakdown else "Needs Replacement",
            "engine_oil_pressure": randint(24,70),
            "engine_speed": randint(1000,2000),
            "engine_temperature": randint(60,110),
            "water_fuel": randint(1700,2500),
            "fuel_level": uniform(0.9,10.0),
            "fuel_pressure": randint(30,80),
            "fuel_temperature": randint(300,800),
            "exhaust_gas_temperature": randint(300,800),
            "hydraulic_pump_rate": randint(70,150),
            "air_filter_pressure_drop": randint(300,800)
        },
        "transmission": {
            "transmission_pressure": randint(100,500)
        },
        "breakdown": is_breakdown  # Adding an indicator for breakdown
    }
    
    collection.insert_one(inspection_data)

print("50 records inserted successfully with some breakdowns!")
"""
customer_data = {
    "id": "CUST-982134",
    "customer_name": "Johnathan Engineering Ltd.",
    "contact_name": "Johnathan Doe",
    "contact_email": "johnathan.doe@johneng.com",
    "contact_phone": "+1-555-123-4567",
    "customer_address": "1234 Industrial Ave, Springfield, IL, 62704, USA",
    "customer_machine": "Caterpillar D11T Bulldozer",
    "machine_serial_number": "D11T-873129",
    "machine_weight_tons": 104.6,
    "purchase_date": datetime.strptime("2021-08-15", "%Y-%m-%d"),
    "warranty_expiration": datetime.strptime("2026-08-15", "%Y-%m-%d"),
    "service_plan": "Premium Service Plan - 5 years",
    "last_service_date": datetime.strptime("2024-07-20", "%Y-%m-%d")
}

# Insert the data into the customer_collection
result = customer_collection.insert_one(customer_data)
print(f"Inserted document ID: {result.inserted_id}")
