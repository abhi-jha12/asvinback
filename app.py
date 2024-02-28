from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import storage
import base64
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Function to upload a file to GCS
def upload_blob(bucket_name, data, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data, content_type='image/jpeg')

# Helper function to generate a unique filename
def generate_filename(camera_id):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    return f"{camera_id}/{timestamp}.jpg"

@app.route('/', methods=['GET'])
def home():
    return "hello"

# Route to handle uploads
@app.route('/upload', methods=['POST'])
def upload():
    content = request.json
    bucket_name = 'asvinimages'

    # Decode and upload image from camera 1
    image_data1 = base64.b64decode(content['imageSrc1'].split(",")[1])
    destination_blob_name1 = generate_filename('camera1')
    upload_blob(bucket_name, image_data1, destination_blob_name1)

    # Decode and upload image from camera 2
    image_data2 = base64.b64decode(content['imageSrc2'].split(",")[1])
    destination_blob_name2 = generate_filename('camera2')
    upload_blob(bucket_name, image_data2, destination_blob_name2)

    return jsonify({"message": "Images received and uploaded successfully"}), 200

if __name__ == '__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../static/asvintech-f07914eac39f.json"
    app.run(debug=True)
