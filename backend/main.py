import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from app.auth import get_password_hash
from app.database import engine
from app.models import Base, CRMUser
from app.routers import (
    auth, cti, dashboard, followups, leads, whatsapp,
    applications, documents, payments, email_campaigns,
    sms, automations, campaigns, queries, users, reports, activities,
)

load_dotenv()

# PostgreSQL-compatible column type for timestamps
_is_pg = 'postgresql' in str(engine.url)
_TS = 'TIMESTAMP WITH TIME ZONE' if _is_pg else 'DATETIME'

# Map of table → {column: definition} for any column that may be missing
_MIGRATIONS: dict[str, dict[str, str]] = {
    'crm_users': {
        'username':       'VARCHAR(100)',
        'email':          'VARCHAR(150)',
        'full_name':      'VARCHAR(150)',
        'role':           "VARCHAR(50) DEFAULT 'counselor'",
        'mobile':         'VARCHAR(20)',
        'department':     'VARCHAR(100)',
        'employee_id':    'VARCHAR(50)',
        'is_active':      'BOOLEAN DEFAULT TRUE',
        'password_hash':  'VARCHAR(255)',
        'two_fa_enabled': 'BOOLEAN DEFAULT FALSE',
        'deleted':        'BOOLEAN DEFAULT FALSE',
        'created_at':     _TS,
    },
    'crm_leads': {
        'lead_id':               'VARCHAR(50)',
        'parent_name':           'VARCHAR(150)',
        'lead_sub_status':       'VARCHAR(100)',
        'lead_score':            'INTEGER DEFAULT 0',
        'lead_strength':         "VARCHAR(50) DEFAULT 'Cold'",
        'admission_probability': 'INTEGER DEFAULT 0',
        'assigned_team_id':      'INTEGER',
        'remarks':               'TEXT',
        'utm_source':            'VARCHAR(100)',
        'utm_medium':            'VARCHAR(100)',
        'utm_campaign':          'VARCHAR(100)',
        'utm_content':           'VARCHAR(100)',
        'utm_term':              'VARCHAR(100)',
        'city':                  'VARCHAR(100)',
        'state':                 'VARCHAR(100)',
        'gender':                'VARCHAR(20)',
        'qualification':         'VARCHAR(100)',
        'deleted':               'BOOLEAN DEFAULT FALSE',
        'updated_at':            _TS,
    },
    'crm_followups': {
        'next_follow_up_date': _TS,
        'deleted':             'BOOLEAN DEFAULT FALSE',
    },
    'crm_call_logs': {
        'lead_id':           'INTEGER',
        'agent_id':          'INTEGER',
        'agent_name':        'VARCHAR(100)',
        'call_type':         'VARCHAR(50)',
        'call_status':       'VARCHAR(50)',
        'duration_seconds':  'INTEGER DEFAULT 0',
        'disposition':       'VARCHAR(100)',
        'notes':             'TEXT',
        'deleted':           'BOOLEAN DEFAULT FALSE',
        'created_at':        _TS,
    },
}


def run_migrations() -> None:
    """Create all new tables and add any missing columns to existing tables."""
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    with engine.begin() as conn:
        for table, columns in _MIGRATIONS.items():
            if table not in existing_tables:
                continue
            existing_cols = {c['name'] for c in inspector.get_columns(table)}
            for col_name, col_def in columns.items():
                if col_name not in existing_cols:
                    try:
                        conn.execute(text(f'ALTER TABLE {table} ADD COLUMN {col_name} {col_def}'))
                    except Exception:
                        pass  # column may have been added by another process


run_migrations()


def seed_default_user() -> None:
    from sqlalchemy.orm import Session

    default_username = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
    default_email    = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@educrm.local')
    default_password = os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin1234')

    with Session(engine) as session:
        user = session.query(CRMUser).filter(CRMUser.username == default_username).first()
        if user is None:
            session.add(CRMUser(
                username=default_username,
                email=default_email,
                full_name='System Administrator',
                role='admin',
                password_hash=get_password_hash(default_password),
            ))
        else:
            user.email         = default_email
            user.full_name     = 'System Administrator'
            user.role          = 'admin'
            user.password_hash = get_password_hash(default_password)
        session.commit()


seed_default_user()

app = FastAPI(title='EduCRM API', version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(followups.router)
app.include_router(cti.router)
app.include_router(whatsapp.router)
app.include_router(dashboard.router)
app.include_router(applications.router)
app.include_router(documents.router)
app.include_router(payments.router)
app.include_router(email_campaigns.router)
app.include_router(sms.router)
app.include_router(automations.router)
app.include_router(campaigns.router)
app.include_router(queries.router)
app.include_router(users.router)
app.include_router(reports.router)
app.include_router(activities.router)


@app.get('/')
def home():
    return {'message': 'EduCRM Backend is Running', 'version': '2.0.0'}
