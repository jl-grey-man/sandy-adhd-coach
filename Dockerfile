FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the entire application
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
