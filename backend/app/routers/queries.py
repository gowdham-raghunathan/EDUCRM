import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMQueryTicket, CRMQueryReply, CRMLeadActivity
from app.schemas import QueryTicketCreate, QueryTicketRead, QueryTicketUpdate, QueryReplyCreate, QueryReplyRead

router = APIRouter(prefix='/api/queries', tags=['Query Manager'])

SLA_HOURS = {'Low': 72, 'Medium': 48, 'High': 24, 'Urgent': 4}


def _gen_ticket_number() -> str:
    return 'TKT-' + uuid.uuid4().hex[:6].upper()


@router.get('/', response_model=list[QueryTicketRead])
def list_tickets(
    status: str = None,
    priority: str = None,
    assigned_to: int = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    query = db.query(CRMQueryTicket).filter(CRMQueryTicket.deleted == False)
    if status:
        query = query.filter(CRMQueryTicket.status == status)
    if priority:
        query = query.filter(CRMQueryTicket.priority == priority)
    if assigned_to:
        query = query.filter(CRMQueryTicket.assigned_to == assigned_to)
    return query.order_by(CRMQueryTicket.created_at.desc()).all()


@router.get('/stats')
def ticket_stats(db: Session = Depends(get_db), _=Depends(get_current_user)):
    tickets = db.query(CRMQueryTicket).filter(CRMQueryTicket.deleted == False).all()
    now = datetime.now(timezone.utc)
    return {
        'total': len(tickets),
        'open': sum(1 for t in tickets if t.status == 'Open'),
        'in_progress': sum(1 for t in tickets if t.status == 'In Progress'),
        'resolved': sum(1 for t in tickets if t.status == 'Resolved'),
        'closed': sum(1 for t in tickets if t.status == 'Closed'),
        'overdue': sum(1 for t in tickets if t.sla_due_at and t.sla_due_at < now and t.status not in ('Resolved', 'Closed')),
        'urgent': sum(1 for t in tickets if t.priority == 'Urgent' and t.status not in ('Resolved', 'Closed')),
    }


@router.get('/{ticket_id}', response_model=QueryTicketRead)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    ticket = db.query(CRMQueryTicket).filter(CRMQueryTicket.id == ticket_id, CRMQueryTicket.deleted == False).first()
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')
    return ticket


@router.post('/', response_model=QueryTicketRead)
def create_ticket(data: QueryTicketCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    sla_hours = SLA_HOURS.get(data.priority, 48)
    ticket = CRMQueryTicket(
        ticket_number=_gen_ticket_number(),
        sla_due_at=datetime.now(timezone.utc) + timedelta(hours=sla_hours),
        **data.model_dump(),
    )
    db.add(ticket)
    if data.lead_id:
        db.add(CRMLeadActivity(
            lead_id=data.lead_id,
            activity_type='Query Ticket Created',
            description=f'Support ticket created: {data.subject}',
            performed_by=user.id,
        ))
    db.commit()
    db.refresh(ticket)
    return ticket


@router.put('/{ticket_id}', response_model=QueryTicketRead)
def update_ticket(ticket_id: int, data: QueryTicketUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ticket = db.query(CRMQueryTicket).filter(CRMQueryTicket.id == ticket_id, CRMQueryTicket.deleted == False).first()
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(ticket, field, value)
    if data.status in ('Resolved', 'Closed') and not ticket.resolved_at:
        ticket.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.post('/{ticket_id}/reply', response_model=QueryReplyRead)
def add_reply(ticket_id: int, data: QueryReplyCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ticket = db.query(CRMQueryTicket).filter(CRMQueryTicket.id == ticket_id, CRMQueryTicket.deleted == False).first()
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')
    reply = CRMQueryReply(ticket_id=ticket_id, message=data.message, replied_by=user.id, is_internal=data.is_internal)
    if ticket.status == 'Open':
        ticket.status = 'In Progress'
    db.add(reply)
    db.commit()
    db.refresh(reply)
    return reply


@router.get('/{ticket_id}/replies', response_model=list[QueryReplyRead])
def get_replies(ticket_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMQueryReply).filter(CRMQueryReply.ticket_id == ticket_id).order_by(CRMQueryReply.created_at.asc()).all()


@router.delete('/{ticket_id}')
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    ticket = db.query(CRMQueryTicket).filter(CRMQueryTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')
    ticket.deleted = True
    db.commit()
    return {'message': 'Ticket deleted'}
