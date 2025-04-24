#!/bin/bash

# Check if an environment argument is provided
ENV=${1:-dev}

if [ "$ENV" = "prod" ] || [ "$ENV" = "production" ]; then
    echo "Stopping PRODUCTION services..."
    docker compose -f docker-compose.prod.yml down
else
    echo "Stopping DEVELOPMENT services..."
    docker compose down
fi

echo "Containers have been stopped." 