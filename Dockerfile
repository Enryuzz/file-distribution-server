FROM python:3.9-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt update 
RUN apt install -y sqlite3
RUN apt install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directories
RUN mkdir -p data/readme data/vpn data/sshkeys

# Make the entrypoint script executable
RUN chmod +x /app/run.sh

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Use the entrypoint script
ENTRYPOINT ["/app/run.sh"] 