from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import CRMLead, CRMUser, CRMLeadActivity
from app.schemas import LeadCreate, LeadRead, LeadUpdate, LeadActivityRead

router = APIRouter(prefix='/api/leads', tags=['Leads'])


@router.get('', response_model=list[LeadRead])
def list_leads(
    status: str = None,
    source: str = None,
    assigned_to: int = None,
    db: Session = Depends(get_db),
    current_user: CRMUser = Depends(get_current_user),
):
    query = db.query(CRMLead).filter(CRMLead.deleted.is_(False))
    if status:
        query = query.filter(CRMLead.lead_status == status)
    if source:
        query = query.filter(CRMLead.lead_source == source)
    if assigned_to:
        query = query.filter(CRMLead.assigned_to == assigned_to)
    return query.order_by(CRMLead.created_at.desc()).all()


@router.get('/{lead_id}', response_model=LeadRead)
def get_lead(lead_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    lead = db.query(CRMLead).filter(CRMLead.id == lead_id, CRMLead.deleted.is_(False)).first()
    if not lead:
        raise HTTPException(status_code=404, detail='Lead not found')
    return lead


@router.get('/{lead_id}/profile')
def get_lead_profile(lead_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    lead = db.query(CRMLead).filter(CRMLead.id == lead_id, CRMLead.deleted.is_(False)).first()
    if not lead:
        raise HTTPException(status_code=404, detail='Lead not found')
    activities = db.query(CRMLeadActivity).filter(CRMLeadActivity.lead_id == lead_id).order_by(CRMLeadActivity.created_at.desc()).limit(20).all()
    return {
        'lead': lead,
        'activities': activities,
        'applications_count': len([a for a in lead.applications if not a.deleted]),
        'followups_count': len([f for f in lead.followups if not f.deleted]),
    }


@router.post('', response_model=LeadRead)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db), current_user: CRMUser = Depends(get_current_user)):
    # Deduplication: check if mobile number already exists
    existing = db.query(CRMLead).filter(CRMLead.mobile_number == payload.mobile_number, CRMLead.deleted.is_(False)).first()
    if existing:
        # Update existing record with new source info and return
        for key in ('email', 'course_interested', 'lead_source', 'utm_source', 'utm_medium', 'utm_campaign'):
            new_val = getattr(payload, key, None)
            if new_val:
                setattr(existing, key, new_val)
        db.add(CRMLeadActivity(
            lead_id=existing.id,
            activity_type='Lead Re-registered',
            description=f'Lead re-registered with same mobile. Source: {payload.lead_source or "Unknown"}',
            performed_by=current_user.id,
        ))
        db.commit()
        db.refresh(existing)
        return existing

    lead = CRMLead(**payload.model_dump())
    db.add(lead)
    db.flush()
    db.add(CRMLeadActivity(
        lead_id=lead.id,
        activity_type='Lead Created',
        description=f'Lead created. Source: {payload.lead_source or "Unknown"}',
        performed_by=current_user.id,
    ))
    db.commit()
    db.refresh(lead)
    return lead


@router.put('/{lead_id}', response_model=LeadRead)
def update_lead(lead_id: int, payload: LeadUpdate, db: Session = Depends(get_db), current_user: CRMUser = Depends(get_current_user)):
    lead = db.query(CRMLead).filter(CRMLead.id == lead_id, CRMLead.deleted.is_(False)).first()
    if not lead:
        raise HTTPException(status_code=404, detail='Lead not found')

    old_status = lead.lead_status
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(lead, key, value)

    if payload.lead_status and payload.lead_status != old_status:
        db.add(CRMLeadActivity(
            lead_id=lead_id,
            activity_type='Stage Changed',
            description=f'Lead status changed from {old_status} to {payload.lead_status}',
            performed_by=current_user.id,
        ))

    db.commit()
    db.refresh(lead)
    return lead


@router.post('/{lead_id}/allocate')
def allocate_lead(lead_id: int, body: dict, db: Session = Depends(get_db), current_user: CRMUser = Depends(get_current_user)):
    lead = db.query(CRMLead).filter(CRMLead.id == lead_id, CRMLead.deleted.is_(False)).first()
    if not lead:
        raise HTTPException(status_code=404, detail='Lead not found')

    counselor_id = body.get('counselor_id')
    team_id = body.get('team_id')

    if counselor_id:
        counselor = db.query(CRMUser).filter(CRMUser.id == counselor_id, CRMUser.deleted.is_(False)).first()
        if not counselor:
            raise HTTPException(status_code=404, detail='Counselor not found')
        lead.assigned_to = counselor_id

    if team_id:
        lead.assigned_team_id = team_id

    db.add(CRMLeadActivity(
        lead_id=lead_id,
        activity_type='Lead Allocated',
        description=f'Lead allocated to counselor ID {counselor_id}',
        performed_by=current_user.id,
    ))
    db.commit()
    return {'message': 'Lead allocated successfully', 'lead_id': lead_id, 'counselor_id': counselor_id}


@router.post('/{lead_id}/score')
def update_lead_score(lead_id: int, body: dict, db: Session = Depends(get_db), current_user: CRMUser = Depends(get_current_user)):
    lead = db.query(CRMLead).filter(CRMLead.id == lead_id, CRMLead.deleted.is_(False)).first()
    if not lead:
        raise HTTPException(status_code=404, detail='Lead not found')

    delta = body.get('delta', 0)
    lead.lead_score = max(0, min(100, (lead.lead_score or 0) + delta))

    if lead.lead_score >= 70:
        lead.lead_strength = 'Hot'
    elif lead.lead_score >= 40:
        lead.lead_strength = 'Warm'
    else:
        lead.lead_strength = 'Cold'

    db.add(CRMLeadActivity(
        lead_id=lead_id,
        activity_type='Score Updated',
        description=f'Lead score updated to {lead.lead_score} ({lead.lead_strength})',
        performed_by=current_user.id,
    ))
    db.commit()
    return {'lead_id': lead_id, 'score': lead.lead_score, 'strength': lead.lead_strength}


@router.delete('/{lead_id}')
def delete_lead(lead_id: int, db: Session = Depends(get_db), current_user: CRMUser = Depends(get_current_user)):
    lead = db.query(CRMLead).filter(CRMLead.id == lead_id, CRMLead.deleted.is_(False)).first()
    if not lead:
        raise HTTPException(status_code=404, detail='Lead not found')
    lead.deleted = True
    db.commit()
    return {'message': 'Lead deleted'}
