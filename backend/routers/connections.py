from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine

router = APIRouter(prefix="/connections", tags=["Connections"])

# Temporary in-memory storage (replace with DB later)
CONNECTIONS = {}

class ConnectionPayload(BaseModel):
    name: str
    db_type: str
    host: str
    port: int
    database: str
    username: str
    password: str

def build_engine(conn: ConnectionPayload):
    if conn.db_type == "postgres":
        return create_engine(
            f"postgresql://{conn.username}:{conn.password}"
            f"@{conn.host}:{conn.port}/{conn.database}"
        )
    raise HTTPException(400, "Unsupported DB type")

@router.post("")
def create_connection(payload: ConnectionPayload):
    connection_id = f"conn_{len(CONNECTIONS)+1}"
    CONNECTIONS[connection_id] = payload
    return {"connection_id": connection_id}

@router.post("/test/{connection_id}")
def test_connection(connection_id: str):
    conn = CONNECTIONS.get(connection_id)
    if not conn:
        raise HTTPException(404, "Connection not found")

    try:
        engine = build_engine(conn)
        with engine.connect() as c:
            c.execute("SELECT 1")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(400, str(e))
