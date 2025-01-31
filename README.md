# garmentseg
API for segmentation of garments, mainly useful in fashion industry

This project is an API extension of clothes segmentation using SegFormer model. 

The API allows users to pass an image URL as input and post processing, the user would get a base64 string of the output image file which can be saved or used for further processing. 

## Files

The following is the folder structure of the project:

-- api: This folder contains the API interface for passing input data as either a URL or gives the option for the user to do batch processing by putting all input images in inputdata folder. 

-- backend_segmentation: This folder contains the backend processing code that runs the SegFormer model. 

-- test: This folder contains a functional test file. 

## Installation

To install the project, the following are the steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/gunjanporwal/garmentseg.git

2. Install dependencies:
   pip install -r requirements.txt  # For Python projects

3. Set environment variables:

   cd api
   
   export FLASK_APP=cloth_segmentation_api.py

5. Run flask app: 
   flask run --host=0.0.0.0 --port=9000

6. Test functionality using Postman:

   ![image](https://github.com/user-attachments/assets/c5507b54-47c7-41ab-bb6f-86fb371b9c7d)

   You can provide either http://127.0.0.1:9000/segmentation/garment or http://<generated_ip_address>:9000/segmentation/garment

   This is the sample request:

      {
       "image_url": "https://plus.unsplash.com/premium_photo-1673210886161-bfcc40f54d1f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8cGVyc29uJTIwc3RhbmRpbmd8ZW58MHx8MHx8&w=1000&q=80"
   }

   Please note that the URL has http, not https since SSL certificates are not installed. 

## Results

The result would be a base64 string that is returned in JSON format. Along with that, the output images are saved in the api folder, namely output_segmented_image.png and output_colormap_image.png. 

Here are few inputs and results generated from the project:

<p align="center">
   Input: <img src="https://github.com/user-attachments/assets/435cad6c-9ceb-4e8a-b21b-6a8ab7a91daa" alt="image" height="450px">
   Output: <img src="https://github.com/user-attachments/assets/95b08238-0422-4b3d-860f-b133330774d8" alt="image" height="450px">
   Output in Matlab colormap format: <img src="https://github.com/user-attachments/assets/9685953a-157c-47cb-94d6-175f5b1fd44c" alt="image" height="450px">
</p>

<p align="center">
   Input: <img src="https://github.com/user-attachments/assets/8f46fa5a-e04a-4f87-af93-cb27b2d3d38e" alt="image" height="450px">
   Output: <img src="https://github.com/user-attachments/assets/e5b64b7a-a63b-42cb-9d0c-944cb027b35e" alt="image" height="450px">
</p>

<p align="center">
   Input: <img src="https://github.com/user-attachments/assets/179a84d1-ce08-4ca6-85a9-b9abe422c392" alt="image" height="450px">
   Output: <img src="https://github.com/user-attachments/assets/f5f01d4d-413f-481f-8632-03402599ac60" alt="image" height="450px">
</p>







