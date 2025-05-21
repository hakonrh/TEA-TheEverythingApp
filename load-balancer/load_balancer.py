from fastapi import FastAPI, Request, Response
import httpx
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

CACHE_SERVERS = [
    "https://tea-cache.onrender.com",
    "https://tea-cache-2.onrender.com",
    "https://tea-cache-3.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tea-dofo.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy(path: str, request: Request):
    chosen_backend = random.choice(CACHE_SERVERS)

    # Forward the request URL and query params
    target_url = f"{chosen_backend}/{path}"
    if request.query_params:
        target_url += f"?{request.query_params}"

    # Clone incoming headers
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() != "host"
    }

    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=10
            )
        except httpx.RequestError as e:
            return Response(
                content=f"Backend error: {str(e)}",
                status_code=502
            )

    # Build the proxy response
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers={k: v for k, v in resp.headers.items()},
        media_type=resp.headers.get("content-type")
    )


@app.get("/")
async def root():
    return {"message": "Load balancer is running"}
