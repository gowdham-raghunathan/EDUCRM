from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import CRMDocument, CRMApplication, CRMLeadActivity
from app.schemas import DocumentCreate, DocumentRead, DocumentVerify

router = APIRouter(prefix='/api/documents', tags=['Documents'])


@router.get('/', response_model=list[DocumentRead])
def list_documents(application_id: int = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    query = db.query(CRMDocument).filter(CRMDocument.deleted == False)
    if application_id:
        query = query.filter(CRMDocument.application_id == application_id)
    return query.order_by(CRMDocument.created_at.desc()).all()


@router.get('/{doc_id}', response_model=DocumentRead)
def get_document(doc_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    doc = db.query(CRMDocument).filter(CRMDocument.id == doc_id, CRMDocument.deleted == False).first()
    if not doc:
        raise HTTPException(status_code=404, detail='Document not found')
    return doc


@router.post('/', response_model=DocumentRead)
def upload_document(data: DocumentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    app = db.query(CRMApplication).filter(CRMApplication.id == data.application_id, CRMApplication.deleted == False).first()
    if not app:
        raise HTTPException(status_code=404, detail='Application not found')

    doc = CRMDocument(**data.model_dump())
    db.add(doc)
    db.add(CRMLeadActivity(
        lead_id=app.lead_id,
        activity_type='Document Uploaded',
        description=f'Document "{data.document_name}" uploaded for application {app.application_number}',
        performed_by=user.id,
    ))
    db.commit()
    db.refresh(doc)
    return doc


@router.put('/{doc_id}/verify', response_model=DocumentRead)
def verify_document(doc_id: int, data: DocumentVerify, db: Session = Depends(get_db), user=Depends(get_current_user)):
    doc = db.query(CRMDocument).filter(CRMDocument.id == doc_id, CRMDocument.deleted == False).first()
    if not doc:
        raise HTTPException(status_code=404, detail='Document not found')

    doc.verification_status = data.verification_status
    doc.verification_notes = data.verification_notes
    doc.verified_by = data.verified_by or user.id
    if data.verification_status in ('Verified', 'Rejected'):
        doc.verified_at = datetime.now(timezone.utc)

    app = db.query(CRMApplication).filter(CRMApplication.id == doc.application_id).first()
    if app:
        db.add(CRMLeadActivity(
            lead_id=app.lead_id,
            activity_type='Document Verified',
            description=f'Document "{doc.document_name}" marked as {data.verification_status}',
            performed_by=user.id,
        ))
    db.commit()
    db.refresh(doc)
    return doc


@router.delete('/{doc_id}')
def delete_document(doc_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    doc = db.query(CRMDocument).filter(CRMDocument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail='Document not found')
    doc.deleted = True
    db.commit()
    return {'message': 'Document deleted'}
