#!/bin/bash

# Stop on error
set -e

echo "🚀 Starting deployment..."

# Check if .env exists, if not create from example or ask user
if [ ! -f backend/.env ]; then
    echo "⚠️  backend/.env file not found!"
    echo "Please create it with your TMDB_API_KEY."
    exit 1
fi

# Load env vars to pass to docker-compose if needed (though compose reads .env usually)
# But here we are using a separate .env file in backend/
# We should probably move .env to root or tell compose where it is.
# For now, let's assume user has .env in root or we copy it.

# Build and start containers
echo "📦 Building and starting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

echo "⏳ Waiting for services to be ready..."
sleep 10

# Run database migrations/population if needed
echo "🎬 Populating database (this might take a while)..."
docker-compose -f docker-compose.prod.yml exec -T backend python scripts/populate_db.py

echo "✅ Deployment complete! Your app should be running on port 80."
