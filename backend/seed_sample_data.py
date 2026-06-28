import os

os.chdir('c:/Users/Gowtham/Desktop/ERP/backend')

from app.database import engine
from app.models import Base
from sqlalchemy import text

Base.metadata.create_all(bind=engine)

with engine.begin() as conn:
    conn.execute(text("DELETE FROM crm_leads"))
    conn.execute(
        text(
            "INSERT INTO crm_leads (lead_id, student_name, mobile_number, email, course_interested, lead_status, admission_probability, remarks, deleted) VALUES (:lead_id, :student_name, :mobile_number, :email, :course_interested, :lead_status, :admission_probability, :remarks, :deleted)"
        ),
        [
            {
                'lead_id': 'LD-1001',
                'student_name': 'Aarav Sharma',
                'mobile_number': '9876543210',
                'email': 'aarav@example.com',
                'course_interested': 'Computer Science',
                'lead_status': 'New',
                'admission_probability': 25,
                'remarks': 'Interested in scholarship',
                'deleted': False,
            },
            {
                'lead_id': 'LD-1002',
                'student_name': 'Meera Patel',
                'mobile_number': '9123456780',
                'email': 'meera@example.com',
                'course_interested': 'Business Administration',
                'lead_status': 'Follow-up',
                'admission_probability': 60,
                'remarks': 'Asked for brochure',
                'deleted': False,
            },
            {
                'lead_id': 'LD-1003',
                'student_name': 'Rohan Verma',
                'mobile_number': '9988776655',
                'email': 'rohan@example.com',
                'course_interested': 'Mechanical Engineering',
                'lead_status': 'Interested',
                'admission_probability': 80,
                'remarks': 'Wants campus tour',
                'deleted': False,
            },
        ],
    )

with engine.connect() as conn:
    rows = conn.execute(text("SELECT lead_id, student_name, course_interested, lead_status FROM crm_leads ORDER BY id")).fetchall()
    print('seeded_rows', rows)
