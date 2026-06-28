from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.models import CRMFollowUp, CRMUser, CRMLeadActivity
from app.schemas import FollowUpCreate, FollowUpRead, FollowUpUpdate

router = APIRouter(prefix='/api/followups', tags=['Follow-ups'])


@router.get('', response_model=list[FollowUpRead])
def list_followups(
    lead_id: int = None,
    status: str = None,
    db: Session = Depends(get_db),
    _: CRMUser = Depends(get_current_user),
):
    query = db.query(CRMFollowUp).filter(CRMFollowUp.deleted.is_(False))
    if lead_id:
        query = query.filter(CRMFollowUp.lead_id == lead_id)
    if status:
        query = query.filter(CRMFollowUp.follow_up_status == status)
    return query.order_by(CRMFollowUp.follow_up_date.asc()).all()


@router.post('', response_model=FollowUpRead)
def create_followup(payload: FollowUpCreate, db: Session = Depends(get_db), user: CRMUser = Depends(get_current_user)):
    followup = CRMFollowUp(**payload.model_dump())
    db.add(followup)
    db.flush()
    db.add(CRMLeadActivity(
        lead_id=payload.lead_id,
        activity_type='Follow-up Scheduled',
        description=f'Follow-up scheduled for {payload.follow_up_date}. Type: {payload.follow_up_type or "Call"}',
        performed_by=user.id,
    ))
    db.commit()
    db.refresh(followup)
    return followup


@router.put('/{followup_id}', response_model=FollowUpRead)
def update_followup(followup_id: int, payload: FollowUpUpdate, db: Session = Depends(get_db), user: CRMUser = Depends(get_current_user)):
    followup = db.query(CRMFollowUp).filter(CRMFollowUp.id == followup_id, CRMFollowUp.deleted.is_(False)).first()
    if not followup:
        raise HTTPException(status_code=404, detail='Follow-up not found')

    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(followup, key, value)

    if payload.follow_up_status == 'Completed':
        db.add(CRMLeadActivity(
            lead_id=followup.lead_id,
            activity_type='Follow-up Completed',
            description=f'Follow-up completed. Notes: {payload.notes or "None"}',
            performed_by=user.id,
        ))

    db.commit()
    db.refresh(followup)
    return followup


@router.delete('/{followup_id}')
def delete_followup(followup_id: int, db: Session = Depends(get_db), _: CRMUser = Depends(get_current_user)):
    followup = db.query(CRMFollowUp).filter(CRMFollowUp.id == followup_id, CRMFollowUp.deleted.is_(False)).first()
    if not followup:
        raise HTTPException(status_code=404, detail='Follow-up not found')
    followup.deleted = True
    db.commit()
    return {'message': 'Follow-up deleted'}
