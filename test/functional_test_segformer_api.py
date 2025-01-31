# -----------------------------------------------------------
# Segmentation API tests
# Author: Gunjan Porwal
# Creation date: 31/01/2025
# Version: 1.0
# Changelog: First version
# -----------------------------------------------------------

import requests
import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

global image_url

image_url = "https://plus.unsplash.com/premium_photo-1673210886161-bfcc40f54d1f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8cGVyc29uJTIwc3RhbmRpbmd8ZW58MHx8MHx8&w=1000&q=80"


# API URL
API_URL = "http://localhost:9000/segmentation/garment"

# Function to display image using Matlab plot library
def displayImage(image, title="Segmented Image"):
    try:
        plt.imshow(image)
        plt.axis('off')  # Hide axes
        plt.title(title, fontsize=14, fontweight='bold', color='red')  # Add title
        plt.show(block=False)  # Show without blocking code execution
        plt.pause(3)  # Display for 3 seconds
        plt.close()  # Automatically close the window
    except Exception as e:
         print(f"Error while displaying the image: {e}")


# Function to convert base64 image to file
def saveBase64Image(base64_string, output_file):
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        image.save(output_file)
        return image
    except Exception as e:
        print(f"Error while saving base64 image: {e}")
        return None


# Function to display the image using PIL's show method
# def displayImage(image):
#     try:
#         image.show()
#     except Exception as e:
#         print(f"Error while displaying the image: {e}")


# Test case to simulate a POST request with an image URL
def testSuccessfulRequest(image_url):
    print("Running test: testSuccessfulRequest")

    # Prepare the data
    payload = {"image_url": image_url}

    # Send the POST request
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        # If the request was successful, get the base64 image from the response
        response_data = response.json()
        base64_image = response_data.get("image")

        # Generate output file name
        output_file_name = "output_image.png"

        # Save the base64 image to a file
        saved_image = saveBase64Image(base64_image, output_file_name)

        if saved_image:
            # Display the image
            displayImage(saved_image, "testSuccessfulRequest")
            print(f"Test Passed: Image saved and displayed as {output_file_name}")
            return response_data
        else:
            print(f"Test Failed: Unable to save the image.")
            return False
    else:
        print(f"Test Failed: Request failed with status code {response.status_code}. Error: {response.json()}")
        return False


# Test case for invalid image URL format
def testInvalidUrlFormat():
    print("\nRunning test: testInvalidUrlFormat")
    invalid_url = "htp://invalid-url"
    payload = {"image_url": invalid_url}

    response = requests.post(API_URL, json=payload)
    if response.status_code == 400:
        print("Test Passed: Invalid URL format correctly handled.")
        return True
    else:
        print(f"Test Failed: Status code {response.status_code}. Error: {response.json()}")
        return False


# Test case for missing image URL
def testMissingImageUrl():
    print("\nRunning test: testMissingImageUrl")
    payload = {}

    response = requests.post(API_URL, json=payload)
    if response.status_code == 400:
        print("Test Passed: Missing image URL correctly handled.")
        return True
    else:
        print(f"Test Failed: Status code {response.status_code}. Error: {response.json()}")
        return False


# Test case for missing or invalid input (wrong image format)
def testInvalidImageUrl():
    print("\nRunning test: testInvalidImageUrl")
    invalid_url = "http://example.com/invalid-image"
    payload = {"image_url": invalid_url}

    response = requests.post(API_URL, json=payload)
    print("Response code: ", response.status_code)
    if response.status_code == 400:
        print("Test Passed: Invalid image URL correctly handled.")
        return True
    else:
        print(f"Test Failed: Status code {response.status_code}. Error: {response.json()}")
        return False


# Test case for verifying segmentation process success
def testProcessingSuccessful():
    print("\nRunning test: testProcessingSuccessful")
    response_data = testSuccessfulRequest(image_url)

    if response_data and "image" in response_data:
        base64_image = response_data["image"]
        try:
            # Decode Base64 and check if it creates a valid image
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))

            # Save and display the image
            image.save("segmented_output.png")
            #image.show()
            displayImage(image, "testProcessingSuccessful")

            print("Test Passed: Image processing was successful and saved as segmented_output.png")
            return True
        except Exception as e:
            print(f"Test Failed: Unable to decode and process image. Error: {str(e)}")
            return False
    else:
        print("Test Failed: No valid image data in response.")
        return False


# Function to run all tests and summarize the results
def runTests():
    
    print("\n\n___________ Running tests. All tests take less than a minute (in total) to finish. ___________\n\n")
    
    passed_tests = 0
    failed_tests = 0

    # Running all tests
    if testSuccessfulRequest(image_url):
        passed_tests += 1
    else:
        failed_tests += 1

    if testInvalidUrlFormat():
        passed_tests += 1
    else:
        failed_tests += 1

    if testMissingImageUrl():
        passed_tests += 1
    else:
        failed_tests += 1

    if testInvalidImageUrl():
        passed_tests += 1
    else:
        failed_tests += 1

    if testProcessingSuccessful():
        passed_tests += 1
    else:
        failed_tests += 1

    # Summary of the test results
    print("\nTest Summary:")
    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {failed_tests}")

# Run the tests
if __name__ == "__main__":
    runTests()
