from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMEmailTemplate, CRMEmailCampaign
from app.schemas import (
    EmailTemplateCreate, EmailTemplateRead, EmailTemplateUpdate,
    EmailCampaignCreate, EmailCampaignRead, EmailCampaignUpdate,
)

router = APIRouter(prefix='/api/email', tags=['Email'])

# ─── Templates ─────────────────────────────────────────────────────────────────

@router.get('/templates', response_model=list[EmailTemplateRead])
def list_templates(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMEmailTemplate).filter(CRMEmailTemplate.deleted == False).order_by(CRMEmailTemplate.created_at.desc()).all()


@router.post('/templates', response_model=EmailTemplateRead)
def create_template(data: EmailTemplateCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    tpl = CRMEmailTemplate(**data.model_dump(), created_by=user.id)
    db.add(tpl)
    db.commit()
    db.refresh(tpl)
    return tpl


@router.put('/templates/{template_id}', response_model=EmailTemplateRead)
def update_template(template_id: int, data: EmailTemplateUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    tpl = db.query(CRMEmailTemplate).filter(CRMEmailTemplate.id == template_id, CRMEmailTemplate.deleted == False).first()
    if not tpl:
        raise HTTPException(status_code=404, detail='Template not found')
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(tpl, field, value)
    db.commit()
    db.refresh(tpl)
    return tpl


@router.delete('/templates/{template_id}')
def delete_template(template_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    tpl = db.query(CRMEmailTemplate).filter(CRMEmailTemplate.id == template_id).first()
    if not tpl:
        raise HTTPException(status_code=404, detail='Template not found')
    tpl.deleted = True
    db.commit()
    return {'message': 'Template deleted'}


# ─── Campaigns ─────────────────────────────────────────────────────────────────

@router.get('/campaigns', response_model=list[EmailCampaignRead])
def list_campaigns(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMEmailCampaign).filter(CRMEmailCampaign.deleted == False).order_by(CRMEmailCampaign.created_at.desc()).all()


@router.get('/campaigns/{campaign_id}', response_model=EmailCampaignRead)
def get_campaign(campaign_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    campaign = db.query(CRMEmailCampaign).filter(CRMEmailCampaign.id == campaign_id, CRMEmailCampaign.deleted == False).first()
    if not campaign:
        raise HTTPException(status_code=404, detail='Campaign not found')
    return campaign


@router.post('/campaigns', response_model=EmailCampaignRead)
def create_campaign(data: EmailCampaignCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    campaign = CRMEmailCampaign(**data.model_dump(), created_by=user.id)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.put('/campaigns/{campaign_id}', response_model=EmailCampaignRead)
def update_campaign(campaign_id: int, data: EmailCampaignUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    campaign = db.query(CRMEmailCampaign).filter(CRMEmailCampaign.id == campaign_id, CRMEmailCampaign.deleted == False).first()
    if not campaign:
        raise HTTPException(status_code=404, detail='Campaign not found')
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(campaign, field, value)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.post('/campaigns/{campaign_id}/send')
def send_campaign(campaign_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    campaign = db.query(CRMEmailCampaign).filter(CRMEmailCampaign.id == campaign_id, CRMEmailCampaign.deleted == False).first()
    if not campaign:
        raise HTTPException(status_code=404, detail='Campaign not found')
    if campaign.status not in ('Draft', 'Scheduled'):
        raise HTTPException(status_code=400, detail='Campaign cannot be sent in current status')
    campaign.status = 'Sent'
    campaign.sent_at = datetime.now(timezone.utc)
    db.commit()
    return {'message': 'Campaign sent', 'campaign_id': campaign_id}


@router.delete('/campaigns/{campaign_id}')
def delete_campaign(campaign_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    campaign = db.query(CRMEmailCampaign).filter(CRMEmailCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail='Campaign not found')
    campaign.deleted = True
    db.commit()
    return {'message': 'Campaign deleted'}
