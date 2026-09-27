from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_session
from models import Order, OrderCreate, OrderUpdate, StatusLog, OrderStatus
from sqlmodel import Session, select
from datetime import datetime, date, timezone

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    # model_dump() is used to convert the OrderCreate model into a dictionary
    # "**" is used to unpack the order data into the Order model
    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.get("/", response_model=list[Order])
def list_orders(
    status: OrderStatus | None = Query(default=None, description="Filter orders by status"),
    created_date: date | None = Query(default=None, description="Filter orders by creation date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    query = select(Order)
    
    if status:
        query = query.where(Order.status == status)
        
    if created_date:
        start = datetime.combine(created_date, datetime.min.time(), tzinfo=timezone.utc)
        end = datetime.combine(created_date, datetime.max.time(), tzinfo=timezone.utc)
        query = query.where(Order.created_at >= start, Order.created_at <= end)
    
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.patch("/{order_id}", response_model=StatusLog)
def update_status(
    order_id: int,
    order_update: OrderUpdate,
    session: Session = Depends(get_session)
):
    db_order = session.get(Order, order_id)
    
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    old_status = db_order.status
    
    if order_update.status:
        db_order.status = order_update.status
    
    if order_update.delivery_address:
        db_order.delivery_address = order_update.delivery_address
        
    db_order.updated_at = datetime.now(timezone.utc)
    
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return StatusLog(
        order_id=db_order.id,
        old_status=old_status.value,
        new_status=db_order.status.value,
        changed_at=db_order.updated_at
)