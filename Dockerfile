# Use the official Python 3.10 image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for OpenCV (cv2)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ["main.py", "./"]
COPY ["core", "core/"]
COPY ["services", "services/"]
COPY ["utils", "utils/"]
COPY ["ml_models", "ml_models/"]
COPY ["static", "static/"]
COPY ["database", "database/"]

# Create the temp directories (since they're ignored in git)
RUN mkdir -p temp_uploads temp_reports

# Expose port 7860 (Standard for Hugging Face Spaces)
EXPOSE 7860

# Command to run the application
# We use the uvicorn command directly to override the local settings in main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
