import sys, os

import cv2
from pyzbar.pyzbar import decode

def extract_url_from_qr(image_path):
    # Load the image
    image = cv2.imread(image_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Use pyzbar to decode the QR code
    qr_codes = decode(gray)
    # Iterate through all detected QR codes

    urls = []
    for qr_code in qr_codes:
        # Extract the data from the QR code
        data = qr_code.data.decode('utf-8')
        return data

print(extract_url_from_qr('uploads/hello.png'))