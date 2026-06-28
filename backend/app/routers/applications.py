import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMApplication, CRMLead, CRMLeadActivity
from app.schemas import ApplicationCreate, ApplicationRead, ApplicationUpdate

router = APIRouter(prefix='/api/applications', tags=['Applications'])


def _gen_app_number() -> str:
    return 'APP-' + uuid.uuid4().hex[:8].upper()


@router.get('/', response_model=list[ApplicationRead])
def list_applications(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMApplication).filter(CRMApplication.deleted == False).order_by(CRMApplication.created_at.desc()).all()


@router.get('/{app_id}', response_model=ApplicationRead)
def get_application(app_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    app = db.query(CRMApplication).filter(CRMApplication.id == app_id, CRMApplication.deleted == False).first()
    if not app:
        raise HTTPException(status_code=404, detail='Application not found')
    return app


@router.post('/', response_model=ApplicationRead)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    lead = db.query(CRMLead).filter(CRMLead.id == data.lead_id, CRMLead.deleted == False).first()
    if not lead:
        raise HTTPException(status_code=404, detail='Lead not found')

    app = CRMApplication(
        application_number=_gen_app_number(),
        lead_id=data.lead_id,
        program=data.program,
        department=data.department,
        batch_year=data.batch_year,
        counselor_id=data.counselor_id,
        notes=data.notes,
        form_data=data.form_data,
    )
    db.add(app)

    # Update lead status
    lead.lead_status = 'Application Started'
    db.add(CRMLeadActivity(
        lead_id=data.lead_id,
        activity_type='Application Created',
        description=f'Application {app.application_number} created',
        performed_by=user.id,
    ))
    db.commit()
    db.refresh(app)
    return app


@router.put('/{app_id}', response_model=ApplicationRead)
def update_application(app_id: int, data: ApplicationUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    app = db.query(CRMApplication).filter(CRMApplication.id == app_id, CRMApplication.deleted == False).first()
    if not app:
        raise HTTPException(status_code=404, detail='Application not found')

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(app, field, value)

    if data.application_status == 'Submitted' and not app.submitted_at:
        app.submitted_at = datetime.now(timezone.utc)
        lead = db.query(CRMLead).filter(CRMLead.id == app.lead_id).first()
        if lead:
            lead.lead_status = 'Application Submitted'

    if data.application_status == 'Withdrawn':
        app.withdrawn_at = datetime.now(timezone.utc)

    db.add(CRMLeadActivity(
        lead_id=app.lead_id,
        activity_type='Application Updated',
        description=f'Application {app.application_number} status updated to {app.application_status}',
        performed_by=user.id,
    ))
    db.commit()
    db.refresh(app)
    return app


@router.delete('/{app_id}')
def delete_application(app_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    app = db.query(CRMApplication).filter(CRMApplication.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail='Application not found')
    app.deleted = True
    db.commit()
    return {'message': 'Application deleted'}


@router.get('/lead/{lead_id}', response_model=list[ApplicationRead])
def get_applications_by_lead(lead_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMApplication).filter(
        CRMApplication.lead_id == lead_id,
        CRMApplication.deleted == False
    ).all()
