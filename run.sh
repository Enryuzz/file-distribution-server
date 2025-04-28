#!/bin/sh
set -e

# Run bootstrap script if database doesn't exist
if [ ! -f "instance/app.sqlite" ]; then
    echo "Bootstrapping application..."
    python bootstrap.py
fi

# Generate SSL certificates if they don't exist and HTTPS is enabled
if [ "$USE_HTTPS" = "true" ]; then
    echo "HTTPS is enabled"
    echo "Using domain: $SSL_DOMAIN"
    
    # Check if we need to regenerate certificates due to domain change
    REGEN_CERT=false
    
    if [ ! -f "ssl/server.crt" ] || [ ! -f "ssl/server.key" ]; then
        echo "SSL certificates not found"
        REGEN_CERT=true
    else
        # Check if current cert matches the specified domain
        CERT_DOMAIN=$(openssl x509 -in ssl/server.crt -text -noout | grep "Subject: " | grep -o "CN = [^,]*" | cut -d " " -f 3)
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
        cd ssl && SSL_DOMAIN="$SSL_DOMAIN" ./generate_cert.sh && cd ..
    fi
    
    echo "[+] Starting application with HTTPS..."
    exec flask run --host=0.0.0.0 --port=5000 --cert=ssl/server.crt --key=ssl/server.key
else
    # Run the application without HTTPS
    echo "[+] Starting application with HTTP..."
    exec flask run --host=0.0.0.0 --port=5000 
fi