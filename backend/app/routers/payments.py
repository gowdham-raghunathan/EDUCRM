import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMPayment, CRMLeadActivity
from app.schemas import PaymentCreate, PaymentRead, PaymentUpdate

router = APIRouter(prefix='/api/payments', tags=['Payments'])


def _gen_payment_ref() -> str:
    return 'PAY-' + uuid.uuid4().hex[:10].upper()


@router.get('/', response_model=list[PaymentRead])
def list_payments(
    lead_id: int = None,
    application_id: int = None,
    payment_status: str = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    query = db.query(CRMPayment).filter(CRMPayment.deleted == False)
    if lead_id:
        query = query.filter(CRMPayment.lead_id == lead_id)
    if application_id:
        query = query.filter(CRMPayment.application_id == application_id)
    if payment_status:
        query = query.filter(CRMPayment.payment_status == payment_status)
    return query.order_by(CRMPayment.created_at.desc()).all()


@router.get('/stats')
def payment_stats(db: Session = Depends(get_db), _=Depends(get_current_user)):
    all_payments = db.query(CRMPayment).filter(CRMPayment.deleted == False).all()
    total_collected = sum(p.amount for p in all_payments if p.payment_status == 'Paid')
    total_pending = sum(p.amount for p in all_payments if p.payment_status == 'Pending')
    total_overdue = sum(
        p.amount for p in all_payments
        if p.payment_status == 'Pending' and p.due_date and p.due_date < datetime.now(timezone.utc)
    )
    return {
        'total_collected': total_collected,
        'total_pending': total_pending,
        'total_overdue': total_overdue,
        'total_transactions': len(all_payments),
        'paid_count': sum(1 for p in all_payments if p.payment_status == 'Paid'),
        'pending_count': sum(1 for p in all_payments if p.payment_status == 'Pending'),
    }


@router.get('/{payment_id}', response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    payment = db.query(CRMPayment).filter(CRMPayment.id == payment_id, CRMPayment.deleted == False).first()
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    return payment


@router.post('/', response_model=PaymentRead)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    payment = CRMPayment(
        payment_reference=_gen_payment_ref(),
        **data.model_dump(),
    )
    db.add(payment)
    if data.lead_id:
        db.add(CRMLeadActivity(
            lead_id=data.lead_id,
            activity_type='Payment Created',
            description=f'Payment of ₹{data.amount} created for {data.fee_type}',
            performed_by=user.id,
        ))
    db.commit()
    db.refresh(payment)
    return payment


@router.put('/{payment_id}', response_model=PaymentRead)
def update_payment(payment_id: int, data: PaymentUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    payment = db.query(CRMPayment).filter(CRMPayment.id == payment_id, CRMPayment.deleted == False).first()
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(payment, field, value)

    if data.payment_status == 'Paid' and not payment.paid_at:
        payment.paid_at = datetime.now(timezone.utc)
        if payment.lead_id:
            db.add(CRMLeadActivity(
                lead_id=payment.lead_id,
                activity_type='Payment Received',
                description=f'Payment of ₹{payment.amount} received for {payment.fee_type}',
                performed_by=user.id,
            ))

    db.commit()
    db.refresh(payment)
    return payment


@router.delete('/{payment_id}')
def delete_payment(payment_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    payment = db.query(CRMPayment).filter(CRMPayment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    payment.deleted = True
    db.commit()
    return {'message': 'Payment deleted'}
