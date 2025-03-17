# Use official Python image
FROM python:3.10

# Install PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Set up PostgreSQL
RUN service postgresql start && \
    sudo -u postgres psql -c "CREATE USER hakon WITH PASSWORD 'secretpassword123';" && \
    sudo -u postgres psql -c "CREATE DATABASE teaeverythingapp OWNER hakon;"

# Set environment variables
ENV POSTGRES_DB=teaeverythingapp
ENV POSTGRES_USER=hakon
ENV POSTGRES_PASSWORD=secretpassword123
ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose FastAPI's default port
EXPOSE 8000

# Start the database and FastAPI app
CMD service postgresql start && uvicorn main:app --host 0.0.0.0 --port 8000
