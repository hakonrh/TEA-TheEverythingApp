#!/bin/bash

# Run Alembic migrations (if using)
if [ -f "alembic.ini" ]; then
  alembic upgrade head
fi

# Start FastAPI with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 10000
