from fastapi import FastAPI
import os, socket

app = FastAPI(title="Hello Service")

SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")


@app.get("/hello")
def hello(name: str = "World"):
    return {
        "message": f"Hello, {name}!",
        "service": "hello-service",
        "version": SERVICE_VERSION,
        "host": socket.gethostname(),   # shows which pod/container replied
    }


@app.get("/health")
def health():
    return {"service": "hello-service", "status": "ok"}
