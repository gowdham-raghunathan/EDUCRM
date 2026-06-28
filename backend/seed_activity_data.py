import os

os.chdir('c:/Users/Gowtham/Desktop/ERP/backend')

from app.database import engine
from app.models import Base
from sqlalchemy import text

Base.metadata.create_all(bind=engine)

with engine.begin() as conn:
    conn.execute(text("DELETE FROM crm_followups"))
    conn.execute(text("DELETE FROM crm_call_logs"))

    lead_ids = conn.execute(text("SELECT id, lead_id FROM crm_leads ORDER BY id")).fetchall()
    if not lead_ids:
        raise SystemExit('No leads found; seed leads first')

    first_lead_id = lead_ids[0][0]
    second_lead_id = lead_ids[1][0]
    third_lead_id = lead_ids[2][0]

    conn.execute(
        text(
            "INSERT INTO crm_followups (lead_id, follow_up_date, follow_up_type, follow_up_status, remarks, deleted) VALUES (:lead_id, :follow_up_date, :follow_up_type, :follow_up_status, :remarks, :deleted)"
        ),
        [
            {
                'lead_id': first_lead_id,
                'follow_up_date': '2026-06-20T10:00:00',
                'follow_up_type': 'Phone Call',
                'follow_up_status': 'Completed',
                'remarks': 'Discussed scholarship options',
                'deleted': False,
            },
            {
                'lead_id': second_lead_id,
                'follow_up_date': '2026-06-21T14:30:00',
                'follow_up_type': 'WhatsApp',
                'follow_up_status': 'Pending',
                'remarks': 'Brochure sent',
                'deleted': False,
            },
            {
                'lead_id': third_lead_id,
                'follow_up_date': '2026-06-22T09:15:00',
                'follow_up_type': 'Email',
                'follow_up_status': 'Completed',
                'remarks': 'Campus tour scheduled',
                'deleted': False,
            },
        ],
    )

    conn.execute(
        text(
            "INSERT INTO crm_call_logs (call_id, lead_id, agent_name, call_type, call_status, duration_seconds, deleted) VALUES (:call_id, :lead_id, :agent_name, :call_type, :call_status, :duration_seconds, :deleted)"
        ),
        [
            {
                'call_id': 'CALL-2001',
                'lead_id': first_lead_id,
                'agent_name': 'Nisha Rao',
                'call_type': 'Inbound',
                'call_status': 'Completed',
                'duration_seconds': 180,
                'deleted': False,
            },
            {
                'call_id': 'CALL-2002',
                'lead_id': second_lead_id,
                'agent_name': 'Karthik',
                'call_type': 'Outbound',
                'call_status': 'Missed',
                'duration_seconds': 0,
                'deleted': False,
            },
            {
                'call_id': 'CALL-2003',
                'lead_id': third_lead_id,
                'agent_name': 'Sonia',
                'call_type': 'Outbound',
                'call_status': 'Completed',
                'duration_seconds': 240,
                'deleted': False,
            },
        ],
    )

with engine.connect() as conn:
    followups = conn.execute(text("SELECT COUNT(*) FROM crm_followups")).fetchone()[0]
    calls = conn.execute(text("SELECT COUNT(*) FROM crm_call_logs")).fetchone()[0]
    print('followups', followups)
    print('calls', calls)
