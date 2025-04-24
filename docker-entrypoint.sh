#!/bin/sh
set -e

# Create required directories
mkdir -p /app/data/readme /app/data/vpn /app/data/sshkeys 

# Initialize the database and create admin user if needed
python bootstrap.py

echo '[+] Starttttttttttttttttttt'

# Start the Flask application
exec flask run --host=0.0.0.0 --port=5000 