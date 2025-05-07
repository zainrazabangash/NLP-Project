# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the notebook and script
COPY 22I-0513_22I-0520.ipynb .
COPY run_notebook.py .

# Expose port for Gradio
EXPOSE 7860

# Command to run the script
CMD ["python", "run_notebook.py"]   