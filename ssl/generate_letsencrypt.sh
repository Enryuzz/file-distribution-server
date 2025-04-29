#!/bin/bash

# # Check if domain is provided
# if [ -z "$1" ]; then
#     echo "Usage: $0 <domain>"
#     echo "Example: $0 example.com"
#     exit 1
# fi

DOMAIN=${SSL_DOMAIN:-localhost}
EMAIL=${2:-admin@$DOMAIN}  # Use provided email or default to admin@domain

# Generate certificates using standalone mode
echo "Generating Let's Encrypt certificates for $DOMAIN..."
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email $EMAIL \
    -d $DOMAIN 

# Copy certificates to our certs directory
echo "Copying certificates to certs directory..."
cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem ssl/fullchain.pem
cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ssl/privkey.pem
cp /etc/letsencrypt/live/$DOMAIN/cert.pem ssl/cert.pem
cp /etc/letsencrypt/live/$DOMAIN/chain.pem ssl/chain.pem

# Set proper permissions
echo "Setting proper permissions..."
chown -R $(id -u):$(id -g) certs/letsencrypt
