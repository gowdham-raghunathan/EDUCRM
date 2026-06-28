from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.auth import get_current_user
from app.database import get_db
from app.models import CRMLead, CRMApplication, CRMPayment, CRMFollowUp, CRMQueryTicket, CRMCampaign, CRMCallLog
from app.schemas import DashboardRead
from datetime import datetime, timezone, date

router = APIRouter(prefix='/api/dashboard', tags=['Dashboard'])


@router.get('', response_model=DashboardRead)
def get_dashboard(db: Session = Depends(get_db), _=Depends(get_current_user)):
    leads = db.query(CRMLead).filter(CRMLead.deleted.is_(False)).all()
    applications = db.query(CRMApplication).filter(CRMApplication.deleted.is_(False)).all()
    payments = db.query(CRMPayment).filter(CRMPayment.deleted.is_(False)).all()
    followups = db.query(CRMFollowUp).filter(CRMFollowUp.deleted.is_(False), CRMFollowUp.follow_up_status == 'Pending').all()
    tickets = db.query(CRMQueryTicket).filter(CRMQueryTicket.deleted.is_(False), CRMQueryTicket.status.in_(['Open', 'In Progress'])).all()
    campaigns = db.query(CRMCampaign).filter(CRMCampaign.deleted.is_(False), CRMCampaign.is_active.is_(True)).all()

    return DashboardRead(
        total_leads=len(leads),
        new_leads=sum(1 for l in leads if l.lead_status == 'New'),
        contacted_leads=sum(1 for l in leads if l.lead_status == 'Contacted'),
        interested_leads=sum(1 for l in leads if l.lead_status == 'Interested'),
        applications_submitted=sum(1 for a in applications if a.application_status == 'Submitted'),
        confirmed_admissions=sum(1 for l in leads if l.lead_status == 'Admission Confirmed'),
        total_payments=sum(p.amount for p in payments if p.payment_status == 'Paid'),
        pending_follow_ups=len(followups),
        open_tickets=len(tickets),
        active_campaigns=len(campaigns),
    )


@router.get('/analytics')
def get_analytics(db: Session = Depends(get_db), _=Depends(get_current_user)):
    leads = db.query(CRMLead).filter(CRMLead.deleted.is_(False)).all()

    funnel = [
        {'stage': 'New', 'count': sum(1 for l in leads if l.lead_status == 'New')},
        {'stage': 'Contacted', 'count': sum(1 for l in leads if l.lead_status == 'Contacted')},
        {'stage': 'Interested', 'count': sum(1 for l in leads if l.lead_status == 'Interested')},
        {'stage': 'Follow-up', 'count': sum(1 for l in leads if l.lead_status == 'Follow-up')},
        {'stage': 'Application Submitted', 'count': sum(1 for l in leads if l.lead_status == 'Application Submitted')},
        {'stage': 'Admission Confirmed', 'count': sum(1 for l in leads if l.lead_status == 'Admission Confirmed')},
    ]

    source_breakdown = {}
    for lead in leads:
        src = lead.lead_source or 'Direct'
        source_breakdown[src] = source_breakdown.get(src, 0) + 1

    strength_breakdown = {}
    for lead in leads:
        strength = lead.lead_strength or 'Cold'
        strength_breakdown[strength] = strength_breakdown.get(strength, 0) + 1

    return {
        'funnel': funnel,
        'source_breakdown': source_breakdown,
        'strength_breakdown': strength_breakdown,
        'total_leads': len(leads),
    }


@router.get('/monthly-trend')
def get_monthly_trend(db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Returns leads and admissions grouped by month for the current year."""
    current_year = datetime.now(timezone.utc).year
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    leads_by_month = (
        db.query(extract('month', CRMLead.created_at).label('month'), func.count().label('count'))
        .filter(CRMLead.deleted.is_(False), extract('year', CRMLead.created_at) == current_year)
        .group_by(extract('month', CRMLead.created_at))
        .all()
    )
    admissions_by_month = (
        db.query(extract('month', CRMLead.created_at).label('month'), func.count().label('count'))
        .filter(CRMLead.deleted.is_(False),
                CRMLead.lead_status == 'Admission Confirmed',
                extract('year', CRMLead.created_at) == current_year)
        .group_by(extract('month', CRMLead.created_at))
        .all()
    )

    lead_map = {int(r.month): r.count for r in leads_by_month}
    adm_map  = {int(r.month): r.count for r in admissions_by_month}

    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    calls_today = db.query(CRMCallLog).filter(
        CRMCallLog.deleted.is_(False),
        CRMCallLog.created_at >= today_start,
    ).count()

    return {
        'monthly': [
            {'month': MONTHS[i], 'leads': lead_map.get(i + 1, 0), 'admissions': adm_map.get(i + 1, 0)}
            for i in range(12)
        ],
        'calls_today': calls_today,
    }
