from fastapi import FastAPI, Request
from fastapi.responses import Response
import httpx, os

app = FastAPI(title="API Gateway")

FRONTEND_URL    = os.getenv("FRONTEND_URL",    "http://frontend:3000")
HELLO_SVC_URL   = os.getenv("HELLO_SVC_URL",   "http://hello-service:5000")


async def _proxy(client: httpx.AsyncClient, url: str, request: Request) -> Response:
    params = dict(request.query_params)
    resp = await client.get(url, params=params)
    return Response(content=resp.content, status_code=resp.status_code,
                    media_type=resp.headers.get("content-type"))


@app.get("/")
async def root(request: Request):
    async with httpx.AsyncClient() as client:
        return await _proxy(client, f"{FRONTEND_URL}/", request)


@app.get("/api/hello")
async def api_hello(request: Request):
    async with httpx.AsyncClient() as client:
        return await _proxy(client, f"{HELLO_SVC_URL}/hello", request)


@app.get("/health")
async def health():
    results = {}
    async with httpx.AsyncClient(timeout=3) as client:
        for name, url in [("frontend", FRONTEND_URL), ("hello-service", HELLO_SVC_URL)]:
            try:
                r = await client.get(f"{url}/health")
                results[name] = r.json()
            except Exception as e:
                results[name] = {"status": "unreachable", "error": str(e)}
    return {"service": "api-gateway", "status": "ok", "dependencies": results}
