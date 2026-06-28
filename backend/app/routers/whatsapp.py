from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import CRMWhatsAppLog, CRMWhatsAppTemplate, CRMLead, CRMLeadActivity
from app.schemas import WhatsAppSend, WhatsAppTemplateCreate, WhatsAppTemplateRead

router = APIRouter(prefix='/api/whatsapp', tags=['WhatsApp'])


@router.get('/logs')
def list_logs(lead_id: int = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    query = db.query(CRMWhatsAppLog).filter(CRMWhatsAppLog.deleted == False)
    if lead_id:
        query = query.filter(CRMWhatsAppLog.lead_id == lead_id)
    return query.order_by(CRMWhatsAppLog.created_at.desc()).limit(100).all()


@router.post('/send')
def send_whatsapp(payload: WhatsAppSend, db: Session = Depends(get_db), user=Depends(get_current_user)):
    mobile = payload.mobile_number
    if not mobile and payload.lead_id:
        lead = db.query(CRMLead).filter(CRMLead.id == payload.lead_id, CRMLead.deleted == False).first()
        if lead:
            mobile = lead.mobile_number

    log = CRMWhatsAppLog(
        lead_id=payload.lead_id,
        mobile_number=mobile or '',
        message=payload.message,
        template_name=payload.template,
        template_category=payload.template_category or 'Utility',
        direction='outbound',
        status='sent',
    )
    db.add(log)

    if payload.lead_id:
        db.add(CRMLeadActivity(
            lead_id=payload.lead_id,
            activity_type='WhatsApp Sent',
            description=f'WhatsApp message sent via template "{payload.template}"',
            performed_by=user.id,
        ))

    db.commit()
    db.refresh(log)
    return {'status': 'queued', 'lead_id': payload.lead_id, 'message': payload.message, 'log_id': log.id}


@router.get('/templates', response_model=list[WhatsAppTemplateRead])
def list_templates(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMWhatsAppTemplate).filter(CRMWhatsAppTemplate.deleted == False).all()


@router.post('/templates', response_model=WhatsAppTemplateRead)
def create_template(data: WhatsAppTemplateCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    tpl = CRMWhatsAppTemplate(**data.model_dump())
    db.add(tpl)
    db.commit()
    db.refresh(tpl)
    return tpl


@router.get('/stats')
def whatsapp_stats(db: Session = Depends(get_db), _=Depends(get_current_user)):
    logs = db.query(CRMWhatsAppLog).filter(CRMWhatsAppLog.deleted == False).all()
    return {
        'total_sent': len(logs),
        'delivered': sum(1 for l in logs if l.status == 'delivered'),
        'read': sum(1 for l in logs if l.status == 'read'),
        'failed': sum(1 for l in logs if l.status == 'failed'),
    }
