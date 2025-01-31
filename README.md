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

4. Run flask app: 
   flask run --host=0.0.0.0 --port=9000

5. Test functionality using Postman:

   ![image](https://github.com/user-attachments/assets/c5507b54-47c7-41ab-bb6f-86fb371b9c7d)


## Results

Here are the results generated from the project:

Input: ![image](https://github.com/user-attachments/assets/435cad6c-9ceb-4e8a-b21b-6a8ab7a91daa)

Output: ![output_image](https://github.com/user-attachments/assets/95b08238-0422-4b3d-860f-b133330774d8)

Output in Matlab colormap format: ![test_color](https://github.com/user-attachments/assets/9685953a-157c-47cb-94d6-175f5b1fd44c)

Input: ![image001](https://github.com/user-attachments/assets/8f46fa5a-e04a-4f87-af93-cb27b2d3d38e)

Output: ![output_image001](https://github.com/user-attachments/assets/e5b64b7a-a63b-42cb-9d0c-944cb027b35e)

Input: ![image005](https://github.com/user-attachments/assets/179a84d1-ce08-4ca6-85a9-b9abe422c392)

Output: ![output_image005](https://github.com/user-attachments/assets/f5f01d4d-413f-481f-8632-03402599ac60)








