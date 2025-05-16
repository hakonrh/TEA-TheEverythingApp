from fastapi import FastAPI, Request, Response
import httpx
import time
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tea-dofo.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache
cache: Dict[str, Dict] = {}

# Cache lifetime in seconds
CACHE_TTL = 60  # 1 minute

# Address of the actual API server (hosted on Render)
BACKEND_API = "https://tea-theeverythingapp.onrender.com"

def invalidate_cache():
    current_time = time.time()
    expired_keys = [key for key, value in cache.items() if current_time - value["timestamp"] > CACHE_TTL]
    for key in expired_keys:
        del cache[key]

@app.middleware("http")
async def cache_middleware(request: Request, call_next):
    method = request.method.upper()

    # Only cache GET
    if method == "GET":
        invalidate_cache()
        cache_key = str(request.url)

        if cache_key in cache:
            print(f"Cache HIT for {cache_key}")
            return cache[cache_key]["response"]

        print(f"Cache MISS for {cache_key}")

    # Construct backend URL
    backend_url = f"{BACKEND_API}{request.url.path}"
    if request.url.query:
        backend_url += f"?{request.url.query}"

    forward_headers = {
        key: value for key, value in request.headers.items()
        if key.lower() != "host"
    }

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                resp = await client.get(backend_url, headers=forward_headers)
            else:
                body = await request.body()
                resp = await client.request(method, backend_url, headers=forward_headers, content=body)
        except httpx.RequestError as e:
            return Response(
                content=f"Error forwarding request to backend: {str(e)}",
                status_code=502
            )

    response = Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
        media_type=resp.headers.get("content-type", "application/json"),
    )

    if method == "GET":
        cache[str(request.url)] = {
            "response": response,
            "timestamp": time.time()
        }

    return response


@app.get("/")
async def root():
    return {"message": "Cache server is running"}
