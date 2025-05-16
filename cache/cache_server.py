# cache_server.py
from fastapi import FastAPI, Request, Response
import httpx
import time
from typing import Dict

app = FastAPI()

# In-memory cache
cache: Dict[str, Dict] = {}

# Cache lifetime in seconds
CACHE_TTL = 60  # 1 minute

# Address of the actual API server
BACKEND_API = "https://tea-theeverythingapp.onrender.com"

def invalidate_cache():
    current_time = time.time()
    expired_keys = [key for key, value in cache.items() if current_time - value["timestamp"] > CACHE_TTL]
    for key in expired_keys:
        del cache[key]

@app.middleware("http")
async def cache_middleware(request: Request, call_next):
    url = str(request.url)

    if request.method != "GET":
        return await call_next(request)

    invalidate_cache()

    cache_key = url

    # Check cache
    if cache_key in cache:
        print(f"Cache HIT for {cache_key}")
        return cache[cache_key]["response"]

    # Forward GET to backend
    async with httpx.AsyncClient() as client:
        backend_url = f"{BACKEND_API}{request.url.path}"
        if request.url.query:
            backend_url += f"?{request.url.query}"
        headers = dict(request.headers)
        resp = await client.get(backend_url, headers=headers)

    # Construct response
    response = Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
        media_type=resp.headers.get("content-type", "application/json"),
    )

    # Cache the response
    cache[cache_key] = {
        "response": response,
        "timestamp": time.time()
    }

    return response


@app.get("/")
async def root():
    return {"message": "Cache server is running"}
