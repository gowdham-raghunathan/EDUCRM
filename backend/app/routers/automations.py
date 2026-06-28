from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMAutomation, CRMAutomationLog
from app.schemas import AutomationCreate, AutomationRead, AutomationUpdate

router = APIRouter(prefix='/api/automations', tags=['Automations'])

TRIGGER_EVENTS = [
    'Lead Created', 'Lead Stage Changed', 'Application Created',
    'Application Stage Changed', 'Payment Received', 'Follow-up Due',
    'Document Uploaded', 'Query Ticket Created',
]

ACTION_TYPES = [
    'Send Email', 'Send SMS', 'Send WhatsApp', 'Assign Counselor',
    'Update Lead Stage', 'Create Follow-up', 'Update Lead Score',
    'Send Notification', 'Trigger Webhook',
]


@router.get('/triggers')
def get_trigger_events(_=Depends(get_current_user)):
    return {'triggers': TRIGGER_EVENTS, 'actions': ACTION_TYPES}


@router.get('/', response_model=list[AutomationRead])
def list_automations(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMAutomation).filter(CRMAutomation.deleted == False).order_by(CRMAutomation.created_at.desc()).all()


@router.get('/{automation_id}', response_model=AutomationRead)
def get_automation(automation_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    auto = db.query(CRMAutomation).filter(CRMAutomation.id == automation_id, CRMAutomation.deleted == False).first()
    if not auto:
        raise HTTPException(status_code=404, detail='Automation not found')
    return auto


@router.post('/', response_model=AutomationRead)
def create_automation(data: AutomationCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    auto = CRMAutomation(**data.model_dump(), created_by=user.id)
    db.add(auto)
    db.commit()
    db.refresh(auto)
    return auto


@router.put('/{automation_id}', response_model=AutomationRead)
def update_automation(automation_id: int, data: AutomationUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    auto = db.query(CRMAutomation).filter(CRMAutomation.id == automation_id, CRMAutomation.deleted == False).first()
    if not auto:
        raise HTTPException(status_code=404, detail='Automation not found')
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(auto, field, value)
    db.commit()
    db.refresh(auto)
    return auto


@router.post('/{automation_id}/toggle')
def toggle_automation(automation_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    auto = db.query(CRMAutomation).filter(CRMAutomation.id == automation_id, CRMAutomation.deleted == False).first()
    if not auto:
        raise HTTPException(status_code=404, detail='Automation not found')
    auto.is_active = not auto.is_active
    db.commit()
    return {'automation_id': automation_id, 'is_active': auto.is_active}


@router.post('/{automation_id}/execute')
def execute_automation(automation_id: int, trigger_data: dict = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    auto = db.query(CRMAutomation).filter(CRMAutomation.id == automation_id, CRMAutomation.deleted == False).first()
    if not auto:
        raise HTTPException(status_code=404, detail='Automation not found')
    if not auto.is_active:
        raise HTTPException(status_code=400, detail='Automation is not active')

    import json
    log = CRMAutomationLog(
        automation_id=automation_id,
        trigger_data=json.dumps(trigger_data or {}),
        status='success',
    )
    db.add(log)
    auto.execution_count += 1
    auto.last_executed_at = datetime.now(timezone.utc)
    db.commit()
    return {'message': 'Automation executed', 'automation_id': automation_id}


@router.get('/{automation_id}/logs')
def get_automation_logs(automation_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    logs = db.query(CRMAutomationLog).filter(CRMAutomationLog.automation_id == automation_id).order_by(CRMAutomationLog.executed_at.desc()).limit(50).all()
    return logs


@router.delete('/{automation_id}')
def delete_automation(automation_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    auto = db.query(CRMAutomation).filter(CRMAutomation.id == automation_id).first()
    if not auto:
        raise HTTPException(status_code=404, detail='Automation not found')
    auto.deleted = True
    db.commit()
    return {'message': 'Automation deleted'}
