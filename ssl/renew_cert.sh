#!/bin/bash

# Check if domain is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <domain>"
    echo "Example: $0 example.com"
    exit 1
fi

DOMAIN=$1

# Stop any running containers that might be using port 80/443

# Renew certificates
echo "Renewing Let's Encrypt certificates for $DOMAIN..."
sudo certbot renew --standalone

echo "Certificate renewal completed successfully!" 