from fastapi import APIRouter, HTTPException
from sqlalchemy import inspect
from routers.connections import CONNECTIONS, build_engine

router = APIRouter(prefix="/schemas", tags=["Schemas"])

@router.get("/{connection_id}/tables")
def list_tables(connection_id: str):
    conn = CONNECTIONS.get(connection_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")

    engine = build_engine(conn)
    inspector = inspect(engine)
    return {
        "tables": inspector.get_table_names()
    }

@router.get("/{connection_id}/tables/{table_name}/columns")
def list_columns(connection_id: str, table_name: str):
    conn = CONNECTIONS.get(connection_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")

    engine = build_engine(conn)
    inspector = inspect(engine)

    columns = inspector.get_columns(table_name)
    return {
        "table": table_name,
        "columns": [
            {
                "name": col["name"],
                "type": str(col["type"])
            }
            for col in columns
        ]
    }
