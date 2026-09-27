from datetime import datetime, date, timezone
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from database import get_session
from models import Order, OrderStatus

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/daily")
def get_summary(
    summary_date: date | None = Query(default=None, description="Date for which to get the summary (YYYY-MM-DD)"),
    session: Session = Depends(get_session)
):
    if summary_date is None:
        summary_date = date.today()
        
    start = datetime.combine(summary_date, datetime.min.time(), tzinfo=timezone.utc)
    end = datetime.combine(summary_date, datetime.max.time(), tzinfo=timezone.utc)
    
    summary = {}
    total = 0
    
    for status in OrderStatus:
        count = session.exec(
            select(func.count(Order.id)).where(
                Order.created_at >= start,
                Order.created_at <= end,
                Order.status == status
            )
        ).one()
        summary[status.value] = count
        total += count
        
    return {
        "date": summary_date.isoformat(),
        "total_orders": total,
        "by_status": summary
    }