FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Create Working directory
WORKDIR /app

COPY . /app

# Install required packages
RUN pip install --no-cache-dir -r /app/requirements.txt

# EXPOSE Port
EXPOSE 8080

# Start Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
