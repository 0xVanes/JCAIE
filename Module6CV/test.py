from PIL import Image
import numpy as np
from model import ImageClassifier
import os
import requests

def test_model_local():
    print("Testing model locally...")
    classifier = ImageClassifier()
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype = np.uint8)

    prediction = classifier.predict(test_image)
    print("Local prediction:", prediction)

def test_api_endpoint(api_url="http://localhost:8000"):
    print(f"Testing API endpoint: {api_url}")
    test_image = Image.new('RGB', (224, 224), color='red')

    test_image_path = "test_image.jpg"
    test_image.save(test_image_path)

    try:
        response = requests.get(f"{api_url}/health")
        print("Health check:", response.json())
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test_image.jpg', f, 'image/jpeg')}
            response = requests.post(f"{api_url}/predict", files=files)

        if response.status_code == 200:
            result = response.json()
            print("Prediction result:", result)
        else:
            print("Error:", response.text)

    except requests.exceptions.ConnectionError:
        print("Could not connect to API. Make sure the server is running")
    except Exception as e:
        print("Error testing API:", str(e))
    finally:
        if os.path.exists(test_image_path):
            os.remove(test_image_path)

def test_with_sample_image(image_path):
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return
    print(f"Testing with image: {image_path}")

    image = Image.open(image_path)
    image = image.resize((224,224))
    image_array = np.array(image)

    classifier = ImageClassifier()
    prediction = classifier.predict(image_array)
    print("Local prediction:", prediction)

    #Test via API
    api_url = "http://localhost:8000"
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(f"{api_url}/predict", files=files)

        if response.status_code == 200:
            result = response.json()
            print("API prediction:", result)
        else:
            print("API Error:", response.text)
    except requests.exceptions.ConnectionError:
        print("Could not connect to API. Make sure the server is running")

if __name__ == "__main__":
    print("=== Computer Vision Model Testing ===")

    test_model_local()
    print("\n" + "="*50 + "\n")

    test_api_endpoint()
    print("\n" + "="*50 + "\n")

    test_with_sample_image("path/to/your/image.jpg")
    print("Testing completed!")