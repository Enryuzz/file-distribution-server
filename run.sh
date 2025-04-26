#!/bin/sh
set -e

# Run bootstrap script if database doesn't exist
if [ ! -f "instance/app.sqlite" ]; then
    echo "Bootstrapping application..."
    python bootstrap.py
fi

# Run the application
echo "[+] Starting application..."
exec flask run --host=0.0.0.0 --port=5000 