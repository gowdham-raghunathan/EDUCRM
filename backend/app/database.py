import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', '')

if DATABASE_URL and 'postgresql' in DATABASE_URL:
    # Neon / any PostgreSQL with SSL
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            'sslmode': 'require',
            'channel_binding': 'prefer',  # Neon supports it; 'prefer' is safe for all pg12+
        },
        pool_pre_ping=True,   # drop dead connections from Neon's idle-timeout
        pool_recycle=300,     # recycle connections every 5 min (Neon sleeps idle ones)
    )
else:
    engine = create_engine(
        'sqlite:///./crm.db',
        connect_args={'check_same_thread': False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
