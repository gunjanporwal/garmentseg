# -----------------------------------------------------------
# Segmentation Backend
# Author: Gunjan Porwal
# Creation date: 30/01/2025
# version: 1.0
# Changelog: First version
# Source library: https://huggingface.co/sayeed99/segformer-b3-fashion
# -----------------------------------------------------------

from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from PIL import Image
import requests
import torch.nn as nn
import numpy as np
import io
import torch
import base64
from io import BytesIO
import matplotlib.cm as cm

# Download the pretrained Segformer model 
processor = SegformerImageProcessor.from_pretrained("sayeed99/segformer-b3-fashion")
model = AutoModelForSemanticSegmentation.from_pretrained("sayeed99/segformer-b3-fashion")

##############################################################
# Backend interface for segmentation model
# Input: Input image URL
# Output: Return the final segmented image post processing 
# in base64 format
##############################################################
def segformerInputFromAPI(input_url):
    
    # Get the image from the URL for segmentation
    image = Image.open(requests.get(input_url, stream=True).raw)
    
    # Do some preprocessing on the image for make it suitable for
    # further processing
    inputs = processor(images=image, return_tensors="pt")
    
    # Pass the image to apply the transform 
    segmented_image = segformerProcessImage(inputs, image)
    
    # Convert the returned data (in tensor format) to an image
    segmented_image = Image.fromarray(segmented_image.numpy().astype(np.uint8))
    
    # Save it as a PNG image locally
    segmented_image.save("./output_segmented_image.png")
    
    # Return the base64 encoded image to calling API
    buffered = BytesIO()
    segmented_image.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return base64_image 

##############################################################
# Backend interface for segmentation model
# Input: Input image
# Output: Return the final segmented image post processing 
# in base64 format
##############################################################
def segformerInputBatchFromAPI(input_image):
    
    # Since input_image is already a PIL Image, no need to open it from a URL
    image = input_image
    
    # Do some preprocessing on the image to make it suitable for further processing
    inputs = processor(images=image, return_tensors="pt")
    
    # Pass the image to apply the transform 
    segmented_image = segformerProcessImage(inputs, image)
    
    # Convert the returned data (in tensor format) to an image
    segmented_image = Image.fromarray(segmented_image.numpy().astype(np.uint8))
    
    # Save it as a PNG image locally
    segmented_image.save("./output_segmented_image.png")
    
    # Return the base64 encoded image to calling API
    buffered = BytesIO()
    segmented_image.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return base64_image 


##############################################################
# Backend interface for segmentation model
# Input: Preprocessed image data,
#        Image obtained as input (through a URL)
# Output: Return the final segmented image post processing 
# in tensor format 
##############################################################
def segformerProcessImage(inputs, image):
    
    # Pass input data to the model 
    outputs = model(**inputs)
    
    logits = outputs.logits.cpu()

    # Use bilinear interpolation to resize image back to original isze
    upsampled_logits = nn.functional.interpolate(
        logits,
        size=image.size[::-1],
        mode="bilinear",
        align_corners=False,
    )

    # Assign which class the pixel belongs to here
    pred_seg = upsampled_logits.argmax(dim=1)[0]  

    # Convert the segmentation tensor/numpy array to a color image using a colormap 
    # This is done just for another viewing option as matlab plots are also of hte same color scheme
    colored_seg = cm.viridis(pred_seg / pred_seg.max()) 
    colored_seg = (colored_seg[:, :, :3] * 255).astype(np.uint8) 

    # Save the image locally
    Image.fromarray(colored_seg).save("./output_colormap_image.png")

    # Return the segmented image
    return pred_seg