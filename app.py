from flask import Flask, render_template, request, redirect
import json
import os
import boto3
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Then override with .env.local if it exists
load_dotenv(dotenv_path=".env.local", override=True)

# AWS S3 Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_REGION = os.getenv('AWS_REGION')
S3_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_JSON_FILE = 'pets.json'

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION
)


app = Flask(__name__, template_folder='views')

def load_pets():
    try:
        obj = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_JSON_FILE)
        data = obj['Body'].read().decode('utf-8')
        return json.loads(data)
    except s3_client.exceptions.NoSuchKey:
        return []
    except Exception as e:
        print(f"Error loading pets.json from S3: {e}")
        return []

def save_pets(pets):
    try:
        json_data = json.dumps(pets, indent=2)
        s3_client.put_object(Bucket=S3_BUCKET, Key=S3_JSON_FILE, Body=json_data)
    except Exception as e:
        print(f"Error saving pets.json to S3: {e}")

@app.route('/')
def index():
    pets = load_pets()
    return render_template('index.html', pets=pets)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['photo']
        filename = secure_filename(file.filename)

        # Upload to S3
        s3_client.upload_fileobj(
            file,
            S3_BUCKET,
            filename,
            ExtraArgs={'ContentType': file.content_type}
        )

        # Generate S3 URL
        s3_url = f'https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}'

        pet = {
            'name': request.form['name'],
            'age': request.form['age'],
            'breed': request.form['breed'],
            'image': s3_url
        }

        pets = load_pets()
        # Append new pet to the list
        pets.append(pet)
        save_pets(pets)

        return redirect('/')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
