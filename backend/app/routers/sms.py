from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMSMSLog, CRMLead, CRMLeadActivity
from app.schemas import SMSSend, SMSRead

router = APIRouter(prefix='/api/sms', tags=['SMS'])


@router.get('/', response_model=list[SMSRead])
def list_sms(lead_id: int = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    query = db.query(CRMSMSLog).filter(CRMSMSLog.deleted == False)
    if lead_id:
        query = query.filter(CRMSMSLog.lead_id == lead_id)
    return query.order_by(CRMSMSLog.created_at.desc()).all()


@router.post('/send', response_model=SMSRead)
def send_sms(data: SMSSend, db: Session = Depends(get_db), user=Depends(get_current_user)):
    mobile = data.mobile_number
    if not mobile and data.lead_id:
        lead = db.query(CRMLead).filter(CRMLead.id == data.lead_id, CRMLead.deleted == False).first()
        if lead:
            mobile = lead.mobile_number

    # Calculate credits (160 chars = 1 credit, each additional 153 = 1 more)
    msg_len = len(data.message)
    credits = 1 + max(0, (msg_len - 160 + 152) // 153) if msg_len > 160 else 1

    log = CRMSMSLog(
        lead_id=data.lead_id,
        mobile_number=mobile or '',
        message=data.message,
        template_id=data.template_id,
        status='queued',
        credits_used=credits,
    )
    db.add(log)

    if data.lead_id:
        db.add(CRMLeadActivity(
            lead_id=data.lead_id,
            activity_type='SMS Sent',
            description=f'SMS sent to {mobile}',
            performed_by=user.id,
        ))

    db.commit()
    db.refresh(log)
    return log


@router.get('/stats')
def sms_stats(db: Session = Depends(get_db), _=Depends(get_current_user)):
    all_sms = db.query(CRMSMSLog).filter(CRMSMSLog.deleted == False).all()
    return {
        'total_sent': len(all_sms),
        'delivered': sum(1 for s in all_sms if s.status == 'delivered'),
        'failed': sum(1 for s in all_sms if s.status == 'failed'),
        'queued': sum(1 for s in all_sms if s.status == 'queued'),
        'total_credits_used': sum(s.credits_used for s in all_sms),
    }
