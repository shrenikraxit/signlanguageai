import requests
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Replace with your actual endpoint and subscription key
subscription_key = '22de4d835cd446b1a259ad43b1f37d60'
vision_endpoint = 'https://imageanalysisshrenik.cognitiveservices.azure.com/'

# Define the features you want to analyze
analyze_url = f'{vision_endpoint}?visualFeatures=Description,Tags'

# Function to send the image data to Azure Computer Vision
def analyze_image_with_azure(image_data):
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream',
    }

    response = requests.post(analyze_url, headers=headers, data=image_data)

    if response.status_code == 200:
        print("Image successfully sent to Azure Computer Vision")
        return response.json()
    else:
        print(f"Failed to analyze image with Azure: {response.status_code}")
        print(response.text)
        return None

@app.route('/process-json', methods=['POST'])
def process_json():
    # Get JSON data from request
    data = request.get_json()

    if not data or 'image' not in data:
        return jsonify({'error': 'No image data received'}), 400

    # Decode the base64 image data to bytes
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)

    # Analyze the image with Azure Computer Vision
    azure_response = analyze_image_with_azure(image_bytes)

    if azure_response:
        return jsonify({'message': 'Image analyzed by Azure', 'response': azure_response}), 200
    else:
        return jsonify({'error': 'Failed to analyze image with Azure'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
