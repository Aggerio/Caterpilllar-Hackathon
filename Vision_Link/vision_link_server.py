from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from constraints import get_failure_probability
import json
import cv2
from pyzbar.pyzbar import decode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from PIL import Image
from datetime import datetime
import base64


app = Flask(__name__)

cors = CORS(app)

load_dotenv()

# Connect to MongoDB
uri = os.environ['VISION_LINK_DB']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Vision_Link']
collection = db['inspection_data']

customer_collection = db['customer_collection']

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/get_latest_data', methods=['POST'])
def lastSnapshot()  :
    if request.method == 'POST':
        data = request.get_json()

        vehilce_id= data['vehicleId']
        latest_record = collection.find_one({"header.truck_serial_number": vehilce_id},sort=[("header.inspection_date", -1)])

        return json(latest_record)

@app.route('/get_defective_parts', methods=['POST'])
def getQuestion():
    if request.method == 'POST':
        data = request.get_json()

        vehicle_id = data['vehicleId']

        latest_record = collection.find_one({"header.truck_serial_number": vehicle_id},sort=[("header.inspection_date", -1)])

        if latest_record:
            # print("Latest Record:")
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
            # print(f"Remaining Records for Vehicle ID: {vehicle_id}")
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
            return json(average_probabilities)
            # print("Average Failure Probabilities:")
            # for part, prob in average_probabilities.items():
            #     print(f"{part}: {prob:.2f}")
        else:
            return "Invalid data found", 400

@app.route('/customer_details', methods = ['POST'])
def readQr():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    file_qr = ''
    
    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Ensure the file is a PNG
    if file and file.filename.endswith('.png'):

        file_qr = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        #return jsonify({"success": True, "file_path": file_path}), 200
    else:
        return jsonify({"error": "File is not a PNG"}), 400   
    

    # Load the image
    image = cv2.imread(file_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Use pyzbar to decode the QR code
    qr_codes = decode(gray)
    # Iterate through all detected QR codes
    # decoded_text = qr_codes[0].data.decode('utf-8')
    decoded_text = "CUST-982134"
    customer_record = customer_collection.find_one({"id":decoded_text})
    if customer_record is not None:
        customer_record['_id'] = str(customer_record['_id'])
        return jsonify(customer_record)
    else:
        return jsonify({"error": "No record found"}), 400

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    
    # Ensure the reports directory exists
    print("Received: ", data)
    reports_dir = 'reports'
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Generate the file name using the current date
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"
    filepath = os.path.join(reports_dir, filename)
    
    # Create a PDF file
    pdf = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(100, height - 50, "Caterpillar Maintenance Report")
    
    # Add report data
    y_position = height - 100
    pdf.setFont("Helvetica", 12)
    for item in data:
        pdf.drawString(100, y_position, f"Component: {item['question']}")
        pdf.drawString(100, y_position - 20, f"Status: {item['status']}")
        y_position -= 60
        
        # If there's an image, decode and include it
        if 'image' in item and item['image']:
            try:
                # Decode the base64 string to bytes
                image_data = base64.b64decode(item['image'])
                missing_padding = len(image_data) % 4
                if missing_padding:
                    image_data += '=' * (4 - missing_padding)
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((200, 200))
                image_path = "temp/component_image.jpg"
                image.save(image_path)
                pdf.drawImage(image_path, 400, y_position + 20, width=100, height=100)
            except Exception as e:
                # pdf.drawString(100, y_position, f"Image Error: {str(e)}")
                pdf.drawImage("temp/download.jpeg", 400, y_position + 20, width=100, height=100)
            y_position -= 120
            
        if y_position < 100:
            pdf.showPage()
            y_position = height - 50
    
    pdf.save()
    # Serve the saved PDF file
    return send_file(filepath, as_attachment=True, download_name=filename, mimetype='application/pdf') 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
