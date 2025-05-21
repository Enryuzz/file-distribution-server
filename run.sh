#!/bin/sh
set -e

# Run bootstrap script if database doesn't exist
if [ ! -f "instance/app.sqlite" ]; then
    echo "Bootstrapping application..."
    python bootstrap.py
fi

# Generate SSL certificates if they don't exist and HTTPS is enabled
if [ "$USE_HTTPS" = "true" ]; then
    echo "[+] Starting application with HTTPS..."
    exec flask run --host=0.0.0.0 --port=5000 --cert=ssl/fullchain.pem --key=ssl/privkey.pem
else
    # Run the application without HTTPS
    echo "[+] Starting application with HTTP..."
    exec flask run --host=0.0.0.0 --port=5000 
fi

# sudo apt install nginx
# sudo mkdir -p /var/www/html/.well-known/acme-challenge

# 
# SSL_DOMAIN=fnd.idcyberskills.com ./ssl/generate_letsencrypt.sh
# sudo SSL_DOMAIN=fnd.idcyberskills.com USE_HTTPS=true docker compose up --build -d
