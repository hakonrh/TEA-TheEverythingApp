#!/bin/bash

# Install PostgreSQL
if ! command -v psql > /dev/null; then
  echo "Installing PostgreSQL..."
  sudo apt-get update
  sudo apt-get install -y postgresql postgresql-contrib
fi

# Start PostgreSQL
echo "Starting PostgreSQL..."
sudo service postgresql start

# Create the database if it doesn’t exist
echo "Checking database..."
sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname = 'tea_database'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE DATABASE tea_database"

# Run database migrations (if using Alembic)
alembic upgrade head

# Start FastAPI with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 10000
