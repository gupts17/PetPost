from flask import Flask, render_template, request, redirect
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='views', static_folder='assets')
UPLOAD_FOLDER = 'assets/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        pet = {
            'name': request.form['name'],
            'age': request.form['age'],
            'breed': request.form['breed'],
            'image': f'/assets/uploads/{filename}'  # to be S3 later
        }

        pets = load_pets()
        pets.append(pet)
        save_pets(pets)

        return redirect('/')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
