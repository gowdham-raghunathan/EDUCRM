from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


# ─── Auth ──────────────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = 'counselor'
    mobile: Optional[str] = None
    department: Optional[str] = None
    employee_id: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    mobile: Optional[str] = None
    department: Optional[str] = None
    employee_id: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    mobile: Optional[str] = None
    department: Optional[str] = None
    employee_id: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── Teams ─────────────────────────────────────────────────────────────────────

class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None
    parent_team_id: Optional[int] = None
    team_lead_id: Optional[int] = None


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_team_id: Optional[int] = None
    team_lead_id: Optional[int] = None


class TeamMemberAdd(BaseModel):
    user_id: int


class TeamRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    parent_team_id: Optional[int] = None
    team_lead_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── Leads ─────────────────────────────────────────────────────────────────────

class LeadBase(BaseModel):
    lead_id: str
    student_name: str
    mobile_number: str
    email: Optional[str] = None
    parent_name: Optional[str] = None
    course_interested: Optional[str] = None
    department: Optional[str] = None
    lead_status: Optional[str] = 'New'
    lead_sub_status: Optional[str] = None
    lead_source: Optional[str] = None
    lead_score: Optional[int] = 0
    lead_strength: Optional[str] = 'Cold'
    admission_probability: Optional[int] = 0
    assigned_to: Optional[int] = None
    assigned_team_id: Optional[int] = None
    remarks: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    gender: Optional[str] = None
    qualification: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    student_name: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[str] = None
    parent_name: Optional[str] = None
    course_interested: Optional[str] = None
    department: Optional[str] = None
    lead_status: Optional[str] = None
    lead_sub_status: Optional[str] = None
    lead_source: Optional[str] = None
    lead_score: Optional[int] = None
    lead_strength: Optional[str] = None
    admission_probability: Optional[int] = None
    assigned_to: Optional[int] = None
    assigned_team_id: Optional[int] = None
    remarks: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    gender: Optional[str] = None
    qualification: Optional[str] = None


class LeadRead(LeadBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LeadActivityRead(BaseModel):
    id: int
    lead_id: int
    activity_type: str
    description: Optional[str] = None
    performed_by: Optional[int] = None
    extra_data: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Follow-ups ────────────────────────────────────────────────────────────────

class FollowUpBase(BaseModel):
    lead_id: int
    follow_up_date: Optional[datetime] = None
    follow_up_type: Optional[str] = 'Phone Call'
    follow_up_status: Optional[str] = 'Pending'
    remarks: Optional[str] = None
    next_follow_up_date: Optional[datetime] = None


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpUpdate(BaseModel):
    follow_up_date: Optional[datetime] = None
    follow_up_type: Optional[str] = None
    follow_up_status: Optional[str] = None
    remarks: Optional[str] = None
    next_follow_up_date: Optional[datetime] = None


class FollowUpRead(FollowUpBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Applications ──────────────────────────────────────────────────────────────

class ApplicationCreate(BaseModel):
    lead_id: int
    program: Optional[str] = None
    department: Optional[str] = None
    batch_year: Optional[str] = None
    counselor_id: Optional[int] = None
    notes: Optional[str] = None
    form_data: Optional[str] = None


class ApplicationUpdate(BaseModel):
    program: Optional[str] = None
    department: Optional[str] = None
    batch_year: Optional[str] = None
    application_status: Optional[str] = None
    application_fee_paid: Optional[bool] = None
    token_fee_paid: Optional[bool] = None
    documents_submitted: Optional[bool] = None
    documents_verified: Optional[bool] = None
    counselor_id: Optional[int] = None
    notes: Optional[str] = None
    form_data: Optional[str] = None
    withdrawal_reason: Optional[str] = None


class ApplicationRead(BaseModel):
    id: int
    application_number: str
    lead_id: int
    program: Optional[str] = None
    department: Optional[str] = None
    batch_year: Optional[str] = None
    application_status: str
    application_fee_paid: bool
    token_fee_paid: bool
    documents_submitted: bool
    documents_verified: bool
    counselor_id: Optional[int] = None
    notes: Optional[str] = None
    submitted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── Documents ─────────────────────────────────────────────────────────────────

class DocumentCreate(BaseModel):
    application_id: int
    document_type: str
    document_name: str
    document_url: Optional[str] = None
    file_size: Optional[int] = 0


class DocumentVerify(BaseModel):
    verification_status: str
    verification_notes: Optional[str] = None
    verified_by: Optional[int] = None


class DocumentRead(BaseModel):
    id: int
    application_id: int
    document_type: str
    document_name: str
    document_url: Optional[str] = None
    file_size: int
    verification_status: str
    verification_notes: Optional[str] = None
    verified_by: Optional[int] = None
    verified_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Payments ──────────────────────────────────────────────────────────────────

class PaymentCreate(BaseModel):
    application_id: Optional[int] = None
    lead_id: Optional[int] = None
    fee_type: str
    amount: float
    currency: Optional[str] = 'INR'
    payment_mode: Optional[str] = None
    due_date: Optional[datetime] = None
    notes: Optional[str] = None
    discount: Optional[float] = 0.0


class PaymentUpdate(BaseModel):
    payment_status: Optional[str] = None
    payment_mode: Optional[str] = None
    gateway_reference: Optional[str] = None
    paid_at: Optional[datetime] = None
    late_fee: Optional[float] = None
    discount: Optional[float] = None
    notes: Optional[str] = None


class PaymentRead(BaseModel):
    id: int
    payment_reference: str
    application_id: Optional[int] = None
    lead_id: Optional[int] = None
    fee_type: str
    amount: float
    currency: str
    payment_status: str
    payment_mode: Optional[str] = None
    gateway_reference: Optional[str] = None
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    late_fee: float
    discount: float
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Email Templates ───────────────────────────────────────────────────────────

class EmailTemplateCreate(BaseModel):
    name: str
    subject: str
    body_html: str
    body_text: Optional[str] = None
    category: Optional[str] = None


class EmailTemplateUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    body_html: Optional[str] = None
    body_text: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class EmailTemplateRead(BaseModel):
    id: int
    name: str
    subject: str
    body_html: str
    body_text: Optional[str] = None
    category: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Email Campaigns ───────────────────────────────────────────────────────────

class EmailCampaignCreate(BaseModel):
    name: str
    subject: str
    body_html: str
    template_id: Optional[int] = None
    target_filter: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class EmailCampaignUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    body_html: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    target_filter: Optional[str] = None


class EmailCampaignRead(BaseModel):
    id: int
    name: str
    subject: str
    body_html: Optional[str] = None
    template_id: Optional[int] = None
    status: str
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    total_recipients: int
    delivered: int
    opened: int
    clicked: int
    bounced: int
    unsubscribed: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── SMS ───────────────────────────────────────────────────────────────────────

class SMSSend(BaseModel):
    lead_id: Optional[int] = None
    mobile_number: str
    message: str
    template_id: Optional[str] = None


class SMSRead(BaseModel):
    id: int
    lead_id: Optional[int] = None
    mobile_number: str
    message: str
    template_id: Optional[str] = None
    status: str
    credits_used: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── WhatsApp ──────────────────────────────────────────────────────────────────

class WhatsAppSend(BaseModel):
    lead_id: Optional[int] = None
    mobile_number: Optional[str] = None
    message: str
    template: Optional[str] = 'Admission Follow-up'
    template_category: Optional[str] = 'Utility'


class WhatsAppTemplateCreate(BaseModel):
    name: str
    category: str
    language: Optional[str] = 'en'
    body_text: str
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    variables: Optional[str] = None


class WhatsAppTemplateRead(BaseModel):
    id: int
    name: str
    category: str
    language: str
    body_text: str
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    approval_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Automations ───────────────────────────────────────────────────────────────

class AutomationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    trigger_event: str
    conditions: Optional[str] = None
    actions: str
    timing: Optional[str] = 'Immediate'
    delay_minutes: Optional[int] = 0


class AutomationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_event: Optional[str] = None
    conditions: Optional[str] = None
    actions: Optional[str] = None
    timing: Optional[str] = None
    delay_minutes: Optional[int] = None
    is_active: Optional[bool] = None


class AutomationRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    trigger_event: str
    conditions: Optional[str] = None
    actions: str
    timing: str
    delay_minutes: int
    is_active: bool
    execution_count: int
    last_executed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Campaigns ─────────────────────────────────────────────────────────────────

class CampaignCreate(BaseModel):
    name: str
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = 0.0


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    is_active: Optional[bool] = None


class CampaignRead(BaseModel):
    id: int
    name: str
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: float
    total_leads: int
    total_applications: int
    total_enrollments: int
    cost_per_lead: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Query Manager ─────────────────────────────────────────────────────────────

class QueryTicketCreate(BaseModel):
    lead_id: Optional[int] = None
    subject: str
    description: str
    category: Optional[str] = 'General'
    priority: Optional[str] = 'Medium'
    source: Optional[str] = 'Web Form'
    assigned_to: Optional[int] = None


class QueryTicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    resolution_notes: Optional[str] = None


class QueryReplyCreate(BaseModel):
    ticket_id: int
    message: str
    replied_by: Optional[int] = None
    is_internal: Optional[bool] = False


class QueryTicketRead(BaseModel):
    id: int
    ticket_number: str
    lead_id: Optional[int] = None
    subject: str
    description: str
    category: str
    priority: str
    status: str
    assigned_to: Optional[int] = None
    source: Optional[str] = None
    resolution_notes: Optional[str] = None
    sla_due_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class QueryReplyRead(BaseModel):
    id: int
    ticket_id: int
    message: str
    replied_by: Optional[int] = None
    is_internal: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Reports ───────────────────────────────────────────────────────────────────

class ReportCreate(BaseModel):
    name: str
    description: Optional[str] = None
    entity: str
    filters: Optional[str] = None
    columns: Optional[str] = None
    group_by: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = 'asc'
    is_scheduled: Optional[bool] = False
    schedule_email: Optional[str] = None


class ReportUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    filters: Optional[str] = None
    columns: Optional[str] = None
    group_by: Optional[str] = None
    sort_by: Optional[str] = None
    is_scheduled: Optional[bool] = None
    schedule_email: Optional[str] = None


class ReportRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    entity: str
    filters: Optional[str] = None
    columns: Optional[str] = None
    group_by: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: str
    is_scheduled: bool
    schedule_email: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Notifications ─────────────────────────────────────────────────────────────

class NotificationRead(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    related_id: Optional[int] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Webhooks ──────────────────────────────────────────────────────────────────

class WebhookCreate(BaseModel):
    name: str
    url: str
    events: str
    secret_key: Optional[str] = None


class WebhookRead(BaseModel):
    id: int
    name: str
    url: str
    events: str
    is_active: bool
    last_triggered_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── CTI ───────────────────────────────────────────────────────────────────────

class CTIIncomingCall(BaseModel):
    caller_number: str
    caller_name: Optional[str] = None


class CTICallEnded(BaseModel):
    call_id: str
    duration_seconds: int
    status: str
    disposition: Optional[str] = None
    notes: Optional[str] = None


# ─── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardRead(BaseModel):
    total_leads: int
    new_leads: int
    contacted_leads: int
    interested_leads: int
    applications_submitted: int
    confirmed_admissions: int
    total_payments: float
    pending_follow_ups: int
    open_tickets: int
    active_campaigns: int
