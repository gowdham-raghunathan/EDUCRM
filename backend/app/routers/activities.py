from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMLeadActivity, CRMLead
from app.schemas import LeadActivityRead

router = APIRouter(prefix='/api/activities', tags=['Activities'])


@router.get('/lead/{lead_id}', response_model=list[LeadActivityRead])
def get_lead_activities(lead_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    lead = db.query(CRMLead).filter(CRMLead.id == lead_id, CRMLead.deleted == False).first()
    if not lead:
        raise HTTPException(status_code=404, detail='Lead not found')
    return db.query(CRMLeadActivity).filter(
        CRMLeadActivity.lead_id == lead_id
    ).order_by(CRMLeadActivity.created_at.desc()).all()


@router.post('/lead/{lead_id}/note')
def add_note(lead_id: int, note: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    lead = db.query(CRMLead).filter(CRMLead.id == lead_id, CRMLead.deleted == False).first()
    if not lead:
        raise HTTPException(status_code=404, detail='Lead not found')
    activity = CRMLeadActivity(
        lead_id=lead_id,
        activity_type='Note Added',
        description=note.get('note', ''),
        performed_by=user.id,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return {'message': 'Note added', 'activity_id': activity.id}
