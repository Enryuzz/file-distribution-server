FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN apt update 
RUN apt install -y sqlite3 openssl
RUN apt install -y curl certbot && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directories
RUN mkdir -p data/readme data/vpn data/sshkeys
RUN mkdir -p ssl

# Make the scripts executable
RUN chmod +x /app/run.sh
RUN chmod +x /app/ssl/generate_cert.sh

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose ports for HTTP and HTTPS
EXPOSE 5000

# Use the entrypoint script
ENTRYPOINT ["/app/run.sh"] 