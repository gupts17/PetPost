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

## Installation (Local)

```bash
pip install flask boto3
python app.py