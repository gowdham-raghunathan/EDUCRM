from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMCampaign, CRMLead
from app.schemas import CampaignCreate, CampaignRead, CampaignUpdate

router = APIRouter(prefix='/api/campaigns', tags=['Campaigns'])


@router.get('/', response_model=list[CampaignRead])
def list_campaigns(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMCampaign).filter(CRMCampaign.deleted == False).order_by(CRMCampaign.created_at.desc()).all()


@router.get('/stats')
def campaign_stats(db: Session = Depends(get_db), _=Depends(get_current_user)):
    campaigns = db.query(CRMCampaign).filter(CRMCampaign.deleted == False).all()
    leads = db.query(CRMLead).filter(CRMLead.deleted == False).all()

    source_breakdown = {}
    for lead in leads:
        src = lead.utm_source or lead.lead_source or 'Direct'
        source_breakdown[src] = source_breakdown.get(src, 0) + 1

    return {
        'total_campaigns': len(campaigns),
        'active_campaigns': sum(1 for c in campaigns if c.is_active),
        'total_budget': sum(c.budget for c in campaigns),
        'total_leads_from_campaigns': sum(c.total_leads for c in campaigns),
        'source_breakdown': source_breakdown,
    }


@router.get('/{campaign_id}', response_model=CampaignRead)
def get_campaign(campaign_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    campaign = db.query(CRMCampaign).filter(CRMCampaign.id == campaign_id, CRMCampaign.deleted == False).first()
    if not campaign:
        raise HTTPException(status_code=404, detail='Campaign not found')
    return campaign


@router.post('/', response_model=CampaignRead)
def create_campaign(data: CampaignCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    campaign = CRMCampaign(**data.model_dump())
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.put('/{campaign_id}', response_model=CampaignRead)
def update_campaign(campaign_id: int, data: CampaignUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    campaign = db.query(CRMCampaign).filter(CRMCampaign.id == campaign_id, CRMCampaign.deleted == False).first()
    if not campaign:
        raise HTTPException(status_code=404, detail='Campaign not found')
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(campaign, field, value)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.delete('/{campaign_id}')
def delete_campaign(campaign_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    campaign = db.query(CRMCampaign).filter(CRMCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail='Campaign not found')
    campaign.deleted = True
    db.commit()
    return {'message': 'Campaign deleted'}
