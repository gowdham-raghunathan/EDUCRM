import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Dial
from app.auth import get_current_user
from app.database import get_db
from app.models import CRMCallLog, CRMLead, CRMLeadActivity, CRMUser

router = APIRouter(prefix='/api/cti', tags=['CTI / Calls'])

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN  = os.getenv('TWILIO_AUTH_TOKEN')
FROM_NUMBER = os.getenv('TWILIO_FROM_NUMBER', '+15005550006')


def _twilio_client() -> Client:
    if not ACCOUNT_SID or not AUTH_TOKEN:
        raise HTTPException(status_code=503, detail='Twilio credentials not configured')
    return Client(ACCOUNT_SID, AUTH_TOKEN)


# ── Outbound Click-to-Call ────────────────────────────────────────────────────

@router.post('/call')
def make_call(
    body: dict,
    db: Session = Depends(get_db),
    user: CRMUser = Depends(get_current_user),
):
    """
    Initiate an outbound call via Twilio.
    Body: { "to": "+919094422737", "lead_id": 123 (optional) }
    """
    to_number: str = body.get('to', '')
    lead_id: int | None = body.get('lead_id')

    if not to_number:
        raise HTTPException(status_code=400, detail='`to` phone number is required')

    client = _twilio_client()

    try:
        call = client.calls.create(
            to=to_number,
            from_=FROM_NUMBER,
            url=f"{os.getenv('BACKEND_PUBLIC_URL', 'http://localhost:8000')}/api/cti/twiml",
            status_callback=f"{os.getenv('BACKEND_PUBLIC_URL', 'http://localhost:8000')}/api/cti/status-callback",
            status_callback_method='POST',
            record=True,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Twilio error: {str(e)}')

    log = CRMCallLog(
        call_id=call.sid,
        lead_id=lead_id,
        agent_id=user.id,
        agent_name=user.full_name,
        call_type='outbound',
        call_status='initiated',
    )
    db.add(log)

    if lead_id:
        db.add(CRMLeadActivity(
            lead_id=lead_id,
            activity_type='Call Initiated',
            description=f'Outbound call to {to_number} initiated. SID: {call.sid}',
            performed_by=user.id,
        ))

    db.commit()

    return {
        'status': 'initiated',
        'call_sid': call.sid,
        'to': to_number,
        'from': FROM_NUMBER,
        'call_status': call.status,
    }


# ── TwiML Instruction Webhook (Twilio calls this URL) ────────────────────────

@router.post('/twiml', response_class=Response)
async def twiml_response():
    """
    Twilio fetches this URL when the call connects to get instructions.
    Returns TwiML telling Twilio what to do (say a message, then connect).
    """
    vr = VoiceResponse()
    vr.say('Hello, this is a call from EduCRM. Please hold while we connect you.')
    vr.pause(length=1)
    vr.say('Thank you for your time. Goodbye.')
    return Response(content=str(vr), media_type='application/xml')


# ── Status Callback (Twilio posts call events here) ──────────────────────────

@router.post('/status-callback')
async def call_status_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Twilio posts status updates here as the call progresses.
    Updates the call log in real-time.
    """
    form_data = await request.form()
    call_sid    = form_data.get('CallSid', '')
    call_status = form_data.get('CallStatus', '')
    duration    = int(form_data.get('CallDuration', 0) or 0)
    recording_url = form_data.get('RecordingUrl', '')

    log = db.query(CRMCallLog).filter(CRMCallLog.call_id == call_sid).first()
    if log:
        log.call_status = call_status
        log.duration_seconds = duration
        if recording_url:
            log.notes = f'Recording: {recording_url}'
        db.commit()

    return {'received': True}


# ── Incoming Call Webhook ─────────────────────────────────────────────────────

@router.post('/incoming-call', response_class=Response)
async def incoming_call(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Twilio posts here when a call comes in to your Twilio number.
    Logs the call and returns TwiML to greet the caller.
    """
    form_data = await request.form()
    call_sid    = form_data.get('CallSid', str(uuid.uuid4()))
    caller      = form_data.get('From', 'Unknown')
    call_status = form_data.get('CallStatus', 'ringing')

    # Try to match caller to a lead by mobile number
    lead = db.query(CRMLead).filter(
        CRMLead.mobile_number == caller,
        CRMLead.deleted == False,
    ).first()

    log = CRMCallLog(
        call_id=call_sid,
        lead_id=lead.id if lead else None,
        call_type='inbound',
        call_status=call_status,
    )
    db.add(log)
    if lead:
        db.add(CRMLeadActivity(
            lead_id=lead.id,
            activity_type='Inbound Call',
            description=f'Incoming call from {caller}. SID: {call_sid}',
            performed_by=None,
        ))
    db.commit()

    vr = VoiceResponse()
    if lead:
        vr.say(f'Hello {lead.full_name}, thank you for calling EduCRM. Please hold.')
    else:
        vr.say('Thank you for calling EduCRM. Please hold while we connect you to a counselor.')
    vr.pause(length=2)
    vr.say('All our counselors are currently busy. Please leave a message after the tone.')
    vr.record(max_length=60, action='/api/cti/recording-done')
    return Response(content=str(vr), media_type='application/xml')


# ── Recording Done Callback ───────────────────────────────────────────────────

@router.post('/recording-done', response_class=Response)
async def recording_done(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    call_sid      = form_data.get('CallSid', '')
    recording_url = form_data.get('RecordingUrl', '')

    log = db.query(CRMCallLog).filter(CRMCallLog.call_id == call_sid).first()
    if log:
        log.notes = f'Voicemail: {recording_url}'
        db.commit()

    vr = VoiceResponse()
    vr.say('Your message has been recorded. Thank you. Goodbye.')
    vr.hangup()
    return Response(content=str(vr), media_type='application/xml')


# ── Call Logs (REST) ──────────────────────────────────────────────────────────

@router.get('/logs')
def get_call_logs(
    lead_id: int = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    query = db.query(CRMCallLog).filter(CRMCallLog.deleted == False)
    if lead_id:
        query = query.filter(CRMCallLog.lead_id == lead_id)
    return query.order_by(CRMCallLog.created_at.desc()).limit(100).all()


@router.get('/active-calls')
def get_active_calls(_=Depends(get_current_user)):
    """Fetch currently active/in-progress calls from Twilio."""
    try:
        client = _twilio_client()
        calls = client.calls.list(status='in-progress', limit=20)
        return [{'sid': c.sid, 'to': c.to, 'from': c.from_, 'status': c.status, 'duration': c.duration} for c in calls]
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post('/calls/{call_sid}/end')
def end_call(call_sid: str, _=Depends(get_current_user)):
    """Hang up an in-progress call."""
    try:
        client = _twilio_client()
        call = client.calls(call_sid).update(status='completed')
        return {'status': 'ended', 'call_sid': call.sid}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get('/calls/{call_sid}')
def get_call_detail(call_sid: str, _=Depends(get_current_user)):
    """Fetch call detail from Twilio."""
    try:
        client = _twilio_client()
        call = client.calls(call_sid).fetch()
        return {
            'sid': call.sid,
            'to': call.to,
            'from': call.from_,
            'status': call.status,
            'duration': call.duration,
            'start_time': str(call.start_time),
            'end_time': str(call.end_time),
            'price': call.price,
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
