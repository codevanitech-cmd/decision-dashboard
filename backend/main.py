from fastapi import FastAPI
from backend.routers import health, connections, schemas, profiling, table_profiling     
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="Decision Intelligence Platform",
    version="0.1"
)

app.include_router(health.router)
app.include_router(connections.router)
app.include_router(schemas.router)
app.include_router(profiling.router)
app.include_router(table_profiling.router)

@app.get("/")
def root():
    return {"message": "Decision Intelligence Platform running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






