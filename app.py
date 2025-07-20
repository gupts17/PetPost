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

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION
)


app = Flask(__name__, template_folder='views')
DATA_FILE = 'pets.json'

def load_pets():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return []
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_pets(pets):
    with open(DATA_FILE, 'w') as f:
        json.dump(pets, f, indent=2)

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
