#!/bin/bash
set -e

# Use the provided domain name or default to localhost
DOMAIN=${SSL_DOMAIN:-localhost}
echo "Generating SSL certificate for domain: $DOMAIN"

# Create self-signed certificate with domain name in CN and SAN
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN" \
  -addext "subjectAltName = DNS:$DOMAIN,DNS:www.$DOMAIN,IP:127.0.0.1"

echo "SSL certificates generated successfully!"
echo "privkey.pem and cert.pem are now available in the ssl directory."
echo "Certificate generated for domain: $DOMAIN" 