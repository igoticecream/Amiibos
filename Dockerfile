FROM python:3.9.16-bullseye

RUN apt update && \
    apt install -y libgl1-mesa-glx

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app

# Copy project files to the container
COPY areas            /app/areas
COPY requirements.txt /app
COPY app.py           /app
COPY unreleased       /app/unreleased

# Install required packages
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Start command
CMD ["python", "app.py"]
