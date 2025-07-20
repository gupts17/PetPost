# PetPost – A Simple Pet Listing Website

**PetPost** is a lightweight web application that allows animal shelter volunteers to upload and display adoptable pets. It's designed to be simple, affordable, and hosted on AWS using EC2 and S3, with no database or authentication required.

---

## Features

- 🐶 Upload pet details (name, age, breed, photo)
- 🐱 Display a list of all adoptable pets with images
- ☁️ Image storage in Amazon S3
- 🔒 Data saved in flat JSON file (no DB)
- 💻 Hosted on AWS EC2

---

## Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Python (Flask)
- **Storage**: JSON file for pet data
- **Image Hosting**: Amazon S3
- **Hosting**: Amazon EC2

---

## How It Works

1. Volunteer fills in a form with pet details and uploads an image.
2. The image is uploaded to Amazon S3.
3. Pet data (name, age, breed, image URL) is saved in a local JSON file.
4. Homepage displays all uploaded pets with their information.

---
## Folder Structure

```
PetPost/
│
├── app.py
├── pets.json
├── assets/
│   └── style.css
├── views/
│   ├── index.html
│   └── upload.html
└── ReadMe.md
```

---

## Installation (Local)

1. **Clone the repository** and navigate to the project folder.

2. **Install dependencies**:
   ```bash
   pip install flask boto3 python-dotenv
   ```

3. **Set up environment variables**:  
   Create a `.env` file in the root directory with the following content:
   ```
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_REGION=your-region
   S3_BUCKET_NAME=your-bucket-name
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:  
   Open your browser and go to [http://localhost:5000](http://localhost:5000)

---

## Usage

- Visit the homepage to see all adoptable pets.
- Click "+ Add a New Pet" to upload a new pet's details and photo.
- All images are stored in your configured S3 bucket, and pet data is stored in `pets.json`.

---

## Deployment

- Deploy to AWS EC2 for hosting.
- Ensure your EC2 instance has access to your S3 bucket (IAM permissions).
- Set environment variables on your server as in the `.env` file.

---