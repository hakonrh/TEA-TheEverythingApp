FROM python:3.11-slim

WORKDIR /app
COPY cache_server.py .

RUN pip install fastapi uvicorn httpx

EXPOSE 8000

CMD ["uvicorn", "cache_server:app", "--host", "0.0.0.0", "--port", "8000"]
