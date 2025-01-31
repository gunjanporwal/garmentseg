# -----------------------------------------------------------
# Script for running segformer model on an input image
# Author: Gunjan Porwal
# Creation date: 31/01/2025
# version: 1.0
# Changelog: First version
# -----------------------------------------------------------

import requests
import base64
from PIL import Image
from io import BytesIO


url = "http://13.60.6.212:9000/segmentation/garment"
payload = {"image_url": "https://plus.unsplash.com/premium_photo-1673210886161-bfcc40f54d1f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8cGVyc29uJTIwc3RhbmRpbmd8ZW58MHx8MHx8&w=1000&q=80"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())

if response.status_code == 200:
    data = response.json()
    
    # Decode base64 string into image
    base64_image = data.get("image")
    if base64_image:
        image_data = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_data))
        
        # Save image locally
        output_path = "segmented_output.png"
        image.save(output_path)
        print(f"Segmented image saved as {output_path}")
        
        # Display the image
        image.show()
    else:
        print("Error: No image data received from API.")
else:
    print("Error:", response.status_code, response.json())