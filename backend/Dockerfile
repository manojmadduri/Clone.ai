# Dockerfile
FROM python:3.10-slim

# Create a working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files
COPY . /app

# Expose port 8000 (FastAPI default in our example)
EXPOSE 8000

CMD ["python", "main.py"]
