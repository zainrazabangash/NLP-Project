# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Copy project files
COPY 22I-0513_22I-0520.ipynb .
COPY 22I-0513_22I-0520.py .
COPY fairy_tales.txt .
COPY config.env .

# Expose ports
# 7860 for Gradio
# 8888 for Jupyter
EXPOSE 7860 8888

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Command to run the main application
CMD ["python", "22I-0513_22I-0520.py"] 