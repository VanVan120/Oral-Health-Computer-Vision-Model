---
title: Oral AI Cancer Disease Detection
emoji: 🦷
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 7860
---

# 🦷 Oral AI: Advanced Disease Detection System

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/IvanJun/Oral_AI_Cancer_Disease_Detection)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)

> **Experience the Live App:** [Click here to visit the deployed application](https://ivanjun-oral-ai-cancer-disease-detection.hf.space)

---

## 📖 Project Overview

**Oral AI** is a cutting-edge medical diagnostic tool designed to assist in the early detection of oral diseases. Leveraging the power of **Deep Learning (PyTorch)** and **Computer Vision**, this system provides real-time analysis of oral cavity images.

The system operates on a sophisticated **Multi-Stage Pipeline**:

1.  **🛡️ Triage Model (The Gatekeeper)**
    *   First, the system verifies if the uploaded image is actually an oral cavity photo.
    *   Filters out irrelevant images to ensure analysis quality.

2.  **🔍 Diagnostic Models (The Specialists)**
    *   **Model A (Disease Detection)**: Identifies potential cancerous lesions and specific oral diseases.
    *   **Model B (Hygiene Assessment)**: Evaluates overall oral hygiene and detects conditions like gingivitis or plaque.

3.  **📧 Smart Reporting**
    *   Generates detailed PDF reports.
    *   Sends results directly to your email (powered by Brevo).

---

## 🚀 Key Features

*   **Real-time Inference**: Instant analysis of uploaded images.
*   **Interactive UI**: Clean, responsive web interface built with HTML5/CSS3.
*   **AI Chatbot**: Integrated assistant to answer your oral health questions.
*   **Secure & Private**: HIPAA-compliant design considerations.
*   **Cloud Native**: Dockerized and ready for deployment on Hugging Face Spaces.

---

## 🛠️ Manual Installation & Usage

Want to run this locally? Follow these steps to compile and run the server on your machine.

### Prerequisites
*   **Python 3.10+**
*   **Git** (with [Git LFS](https://git-lfs.com/) installed for model files)

### 1. Clone the Repository
```bash
git clone https://github.com/VanVan120/Backend-Development.git
cd Backend-Development
git lfs pull
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory or set the variable in your terminal. You need a Brevo API key for email features.
```bash
# Windows (PowerShell)
$env:BREVO_API_KEY="your_brevo_api_key_here"

# Linux/Mac
export BREVO_API_KEY="your_brevo_api_key_here"
```

### 4. Run the Application
You can start the server using the provided batch script (Windows) or directly via Python.

**Option A: Using the Batch Script (Windows)**
```bash
start_server.bat
```

**Option B: Using Command Line**
```bash
python main.py
```
*The server will start at `http://localhost:8000`*

---

## 🐳 Docker Deployment

This project is fully containerized. To run it using Docker:

1.  **Build the Image**
    ```bash
    docker build -t oral-ai-backend .
    ```

2.  **Run the Container**
    ```bash
    docker run -p 7860:7860 -e BREVO_API_KEY="your_key" oral-ai-backend
    ```
    *Access the app at `http://localhost:7860`*

---

## 📂 Project Structure

```
├── Model A/            # Disease Detection Model & Training
├── Model B/            # Hygiene Assessment Model
├── Model Triage/       # Input Validation Model
├── static/             # Frontend Assets (HTML, CSS, JS)
├── main.py             # FastAPI Application Entry Point
├── Dockerfile          # Container Configuration
└── requirements.txt    # Python Dependencies
```

---
*Developed for SEGP - Backend Development*
