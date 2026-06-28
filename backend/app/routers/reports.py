from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMReport, CRMLead, CRMApplication, CRMPayment, CRMFollowUp, CRMQueryTicket
from app.schemas import ReportCreate, ReportRead, ReportUpdate

router = APIRouter(prefix='/api/reports', tags=['Reports'])


@router.get('/', response_model=list[ReportRead])
def list_reports(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMReport).filter(CRMReport.deleted == False).order_by(CRMReport.created_at.desc()).all()


@router.get('/run/{entity}')
def run_report(entity: str, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if entity == 'leads':
        rows = db.query(CRMLead).filter(CRMLead.deleted == False).all()
        data = [{'id': r.id, 'name': r.student_name, 'mobile': r.mobile_number, 'status': r.lead_status,
                 'source': r.lead_source, 'score': r.lead_score, 'created': str(r.created_at)} for r in rows]
    elif entity == 'applications':
        rows = db.query(CRMApplication).filter(CRMApplication.deleted == False).all()
        data = [{'id': r.id, 'number': r.application_number, 'program': r.program, 'status': r.application_status,
                 'fee_paid': r.application_fee_paid, 'created': str(r.created_at)} for r in rows]
    elif entity == 'payments':
        rows = db.query(CRMPayment).filter(CRMPayment.deleted == False).all()
        data = [{'id': r.id, 'reference': r.payment_reference, 'fee_type': r.fee_type, 'amount': r.amount,
                 'status': r.payment_status, 'mode': r.payment_mode, 'created': str(r.created_at)} for r in rows]
    elif entity == 'followups':
        rows = db.query(CRMFollowUp).filter(CRMFollowUp.deleted == False).all()
        data = [{'id': r.id, 'lead_id': r.lead_id, 'type': r.follow_up_type, 'status': r.follow_up_status,
                 'date': str(r.follow_up_date)} for r in rows]
    elif entity == 'tickets':
        rows = db.query(CRMQueryTicket).filter(CRMQueryTicket.deleted == False).all()
        data = [{'id': r.id, 'ticket': r.ticket_number, 'subject': r.subject, 'status': r.status,
                 'priority': r.priority, 'created': str(r.created_at)} for r in rows]
    else:
        raise HTTPException(status_code=400, detail=f'Unknown entity: {entity}')

    return {'entity': entity, 'total': len(data), 'data': data}


@router.get('/dashboard-summary')
def dashboard_summary(db: Session = Depends(get_db), _=Depends(get_current_user)):
    leads = db.query(CRMLead).filter(CRMLead.deleted == False).all()
    applications = db.query(CRMApplication).filter(CRMApplication.deleted == False).all()
    payments = db.query(CRMPayment).filter(CRMPayment.deleted == False).all()

    status_breakdown = {}
    source_breakdown = {}
    for lead in leads:
        status_breakdown[lead.lead_status] = status_breakdown.get(lead.lead_status, 0) + 1
        src = lead.lead_source or 'Unknown'
        source_breakdown[src] = source_breakdown.get(src, 0) + 1

    return {
        'leads_by_status': status_breakdown,
        'leads_by_source': source_breakdown,
        'applications_by_status': {
            s: sum(1 for a in applications if a.application_status == s)
            for s in set(a.application_status for a in applications)
        } if applications else {},
        'revenue': {
            'total_collected': sum(p.amount for p in payments if p.payment_status == 'Paid'),
            'pending': sum(p.amount for p in payments if p.payment_status == 'Pending'),
        },
    }


@router.get('/{report_id}', response_model=ReportRead)
def get_report(report_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    report = db.query(CRMReport).filter(CRMReport.id == report_id, CRMReport.deleted == False).first()
    if not report:
        raise HTTPException(status_code=404, detail='Report not found')
    return report


@router.post('/', response_model=ReportRead)
def create_report(data: ReportCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    report = CRMReport(**data.model_dump(), created_by=user.id)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.put('/{report_id}', response_model=ReportRead)
def update_report(report_id: int, data: ReportUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    report = db.query(CRMReport).filter(CRMReport.id == report_id, CRMReport.deleted == False).first()
    if not report:
        raise HTTPException(status_code=404, detail='Report not found')
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(report, field, value)
    db.commit()
    db.refresh(report)
    return report


@router.delete('/{report_id}')
def delete_report(report_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    report = db.query(CRMReport).filter(CRMReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail='Report not found')
    report.deleted = True
    db.commit()
    return {'message': 'Report deleted'}
