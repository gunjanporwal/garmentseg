# -----------------------------------------------------------
# Segmentation API
# Author: Gunjan Porwal
# Creation date: 30/01/2025
# version: 1.0
# Changelog: First version
# Source library: https://huggingface.co/sayeed99/segformer-b3-fashion
# -----------------------------------------------------------

import requests
import json
import os
import base64
import sys
import io
from PIL import Image
from io import BytesIO

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

# Add path to sys.path so that backend files can get called
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_segmentation.segformer import segformerInputFromAPI, segformerInputBatchFromAPI

app = Flask(__name__)
cors = CORS(app, resources={r"/segmentation/*": {"origins": "*"}})


##############################################################
# Perform segmentation on an image using SegFormer model 
# Input: Image as an input (through a URL)
# Output: Output is base64 encoding of the image
##############################################################
@app.route("/segmentation/garment", methods=['POST'])
@cross_origin(origin='*', methods=['POST'],\
        allow_headers=['Content-Type', 'Authorization'])
def segformerModel():
    
    try: 
        # Extract JSON data from the request
        json_data = request.get_json()
        
        # Validate and extract the image URL
        if not json_data or "image_url" not in json_data:
            return jsonify({"Error": "Image URL is required in the request payload."}), 400
        
        image_url = json_data["image_url"]

        # Check URL format for correctness
        if not isinstance(image_url, str) or not image_url.startswith(("http://", "https://")):
            return jsonify({"Error": "Invalid URL format. Provide a valid image URL."}), 400

        # Additional checks for URL
        try:
            # Check if URL is valid and content type is an image
            response = requests.head(image_url, allow_redirects=True)
            
            # Return if URL is not accessible
            if response.status_code != 200:
                return jsonify({"Error": "Unable to access the image URL. Ensure the URL is correct and the image is publicly accessible."}), 400
            
            # Check the content type to ensure it is an image
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                return jsonify({"Error": "The URL does not point to a valid image. Enter another URL"}), 400

        except requests.exceptions.RequestException as e:
            # Handle other errors if any
            return jsonify({"Error": "Error occurred while accessing image URL.", "details": str(e)}), 400

        # Call the segmentation backend
        segmented_image = segformerInputFromAPI(image_url)

        # The backend is directly returning converted base64 string, so that is assigned directly to return value
        base64_image = segmented_image

        # Return the base64 image in the JSON response
        return jsonify({"image": base64_image}), 200

    except Exception as e:
        # Handle unexpected errors
        print("Error occurred:", str(e))
        return jsonify({"Error": "An unexpected error occurred.", "details": str(e)}), 500


##############################################################
# Perform segmentation on a batch of images using SegFormer model 
# Input: None (input is taken from /inputdata directory)
# Please note inputdata directory must be present in the 
# folder in which the API is run
# Output: Output files are saved in /outputdata directory
##############################################################
@app.route("/segmentation/garment-batch", methods=['POST'])
@cross_origin(origin='*', methods=['POST'], allow_headers=['Content-Type', 'Authorization'])
def segformerModelBatch():
    try:
        # Get all image files from the inputdata directory
        input_dir = './inputdata'
        output_dir = './outputdata'

        # Check if the input and output directories exist
        if not os.path.exists(input_dir):
            return jsonify({"Error": "Input directory does not exist."}), 400
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  

        # Get a list of image files in the input directory
        image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

        # If there are no image files, return an error
        if not image_files:
            return jsonify({"Error": "No images found in the input directory."}), 400

        # Process each image in the input directory
        processed_images = []
        for image_name in image_files:
            image_path = os.path.join(input_dir, image_name)
            try:
                # Open the image
                image = Image.open(image_path)
                print("Processing image: ", image_name)

                # Call the segmentation backend and pass image as parameter
                segmented_image = segformerInputBatchFromAPI(image)  

                # Save the segmented image as PNG in the output directory
                output_image_path = os.path.join(output_dir, f"output_{image_name}")
                
                image_data = base64.b64decode(segmented_image)

                # Convert the binary data to an image object
                output_image = Image.open(io.BytesIO(image_data))

                # Save the image
                output_image.save(output_image_path)
                
                # Convert the segmented image to base64 encoding
                buffered = BytesIO()
                segmented_image.save(buffered, format="PNG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

                # Collect the result (image and output file path)
                processed_images.append({
                    "image": base64_image,
                    "output_image": output_image_path
                })
            except Exception as e:
                # Handle errors for each individual image
                processed_images.append({
                    "image_name": image_name,
                    "error": str(e)
                })

        # Return the results as a JSON response
        return jsonify({"processed_images": processed_images}), 200

    except Exception as e:
        # Handle unexpected errors
        print("Error occurred:", str(e))
        return jsonify({"Error": "An unexpected error occurred.", "details": str(e)}), 500

# Run the code on Flask server on port 9000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
