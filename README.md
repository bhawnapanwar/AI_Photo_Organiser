# AI_Photo_Organiser


An intelligent Python-based tool that uses **Azure Computer Vision** to automatically categorize and sort image files based on their visual content.

---

## 🚀 Overview
This project solves the problem of messy photo folders. Instead of manual sorting, this script analyzes each image, detects objects and tags, and organizes them into descriptive folders. It also generates a central metadata file for easy searching.

### ✨ Key Features
* **Automated Image Tagging:** Uses Azure's deep learning models to identify objects.
* **Smart Folder Structure:** Automatically creates and moves files into folders named after detected tags.
* **Metadata Extraction:** Exports a `metadata.json` containing captions, confidence scores, and dominant colors.
* **Image Optimization:** Handles EXIF orientation and resizes images on-the-fly for efficient API processing.

## 🛠️ Tech Stack
* **Language:** Python 
* **AI Service:** Azure Cognitive Services (Computer Vision API)
* **Libraries:** `Pillow`, `azure-cognitiveservices-vision-computervision`, `python-dotenv`

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
### 2. Install Dependencies
### 3. Create a file named .env in the root directory and add your Azure credentials
### 4. Finally place your images in a folder named source_photos and run the script.

