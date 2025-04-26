#!/bin/bash

# Check if virtual environment exists, create if it doesn't
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run bootstrap script if database doesn't exist
if [ ! -f "instance/app.sqlite" ]; then
    echo "Bootstrapping application..."
    python bootstrap.py
fi

# Run the application
echo "Starting application..."
flask run --host=0.0.0.0 --port=5000 