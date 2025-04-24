#!/bin/bash

# Check if an environment argument is provided
ENV=${1:-dev}

if [ "$ENV" = "prod" ] || [ "$ENV" = "production" ]; then
    echo "Starting in PRODUCTION mode..."
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo "Warning: .env file not found. Using default values."
        echo "For production, it's recommended to create a .env file with a secure SECRET_KEY."
        echo "You can copy .env.example to .env and modify it."
    fi
    
    docker compose -f docker-compose.prod.yml up --build -d
else
    echo "Starting in DEVELOPMENT mode..."
    docker compose up --build -d
fi

echo "Containers are starting. You can access the application at http://localhost:5000"
echo "Default admin credentials: admin/admin" 