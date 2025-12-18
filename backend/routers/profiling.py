from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.database import SessionLocal
from backend.schemas.profiling import ProfilingSummary

router = APIRouter(
    prefix="/profiling",
    tags=["Profiling"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/summary", response_model=ProfilingSummary)
def profiling_summary(db: Session = Depends(get_db)):
    total = db.execute(text("SELECT COUNT(*) FROM records")).scalar()

    rows = db.execute(
        text("""
            SELECT category, COUNT(*) AS count
            FROM records
            GROUP BY category
        """)
    ).fetchall()

    return {
        "total_records": total,
        "breakdown": [
            {"category": r[0], "count": r[1]}
            for r in rows
        ]
    }
