#!/bin/sh

sudo apt install -y openssl certbot

echo "HTTPS is enabled"
echo "Using domain: $SSL_DOMAIN"

# Check if we need to regenerate certificates due to domain change
REGEN_CERT=false

if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/privkey.pem" ]; then
    echo "SSL certificates not found"
    REGEN_CERT=true
else
    # Check if current cert matches the specified domain
    CERT_DOMAIN=$(openssl x509 -in ssl/cert.pem -text -noout | grep "Subject: " | grep -o "CN = [^,]*" | cut -d " " -f 3)
    if [ "$CERT_DOMAIN" != "$SSL_DOMAIN" ]; then
        echo "Domain mismatch: Certificate is for $CERT_DOMAIN but $SSL_DOMAIN was requested"
        REGEN_CERT=true
    else
        echo "Using existing certificates for domain $SSL_DOMAIN"
    fi
fi

# Regenerate certificate if needed
if [ "$REGEN_CERT" = "true" ]; then
    echo "Generating SSL certificates for domain: $SSL_DOMAIN"
    ls -la .
    sudo SSL_DOMAIN="$SSL_DOMAIN" sh ./ssl/generate_letsencrypt.sh
fi