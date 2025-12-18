from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from backend.database import engine

router = APIRouter(
    prefix="/tables",
    tags=["Profiling"]
)

@router.get("/{table_name}/profile")
def profile_table(table_name: str):
    with engine.connect() as conn:
        # total rows
        total_rows = conn.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        ).scalar()

        if total_rows is None:
            raise HTTPException(status_code=404, detail="Table not found")

        # column metadata
        columns = conn.execute(
            text("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = :table
            """),
            {"table": table_name}
        ).fetchall()

        results = []

        for col_name, col_type in columns:
            nulls = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_name} WHERE {col_name} IS NULL")
            ).scalar()

            unique = conn.execute(
                text(f"SELECT COUNT(DISTINCT {col_name}) FROM {table_name}")
            ).scalar()

            samples = conn.execute(
                text(f"""
                    SELECT {col_name}
                    FROM {table_name}
                    WHERE {col_name} IS NOT NULL
                    LIMIT 3
                """)
            ).scalars().all()

            col_profile = {
                "name": col_name,
                "type": col_type,
                "null_percent": round((nulls / total_rows) * 100, 2) if total_rows else 0,
                "unique_count": unique,
                "samples": samples
            }

            if col_type in ["integer", "numeric", "double precision"]:
                minmax = conn.execute(
                    text(f"""
                        SELECT MIN({col_name}), MAX({col_name})
                        FROM {table_name}
                    """)
                ).fetchone()
                col_profile["min"] = minmax[0]
                col_profile["max"] = minmax[1]

            results.append(col_profile)

        return {
            "table": table_name,
            "row_count": total_rows,
            "columns": results
        }
