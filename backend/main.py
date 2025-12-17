from fastapi import FastAPI
from routers import connections, profiling, metrics, dashboards

app = FastAPI(title="Decision Intelligence Platform")

app.include_router(connections.router, prefix="/connections")
app.include_router(profiling.router, prefix="/profiling")
app.include_router(metrics.router, prefix="/metrics")
app.include_router(dashboards.router, prefix="/dashboards")

@app.get("/")
def health():
    return {"status": "running"}
