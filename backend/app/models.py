from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class CRMTeam(Base):
    __tablename__ = 'crm_teams'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(Text)
    parent_team_id = Column(Integer, ForeignKey('crm_teams.id'), nullable=True)
    team_lead_id = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    members = relationship('CRMTeamMember', back_populates='team')


class CRMTeamMember(Base):
    __tablename__ = 'crm_team_members'
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('crm_teams.id'))
    user_id = Column(Integer, ForeignKey('crm_users.id'))
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    team = relationship('CRMTeam', back_populates='members')


class CRMUser(Base):
    __tablename__ = 'crm_users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(150), unique=True, index=True)
    full_name = Column(String(150))
    role = Column(String(50), default='counselor')
    mobile = Column(String(20))
    department = Column(String(100))
    employee_id = Column(String(50))
    is_active = Column(Boolean, default=True)
    password_hash = Column(String(255), nullable=False)
    two_fa_enabled = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMLead(Base):
    __tablename__ = 'crm_leads'
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(String(50), unique=True, index=True)
    student_name = Column(String(150), nullable=False)
    mobile_number = Column(String(20), nullable=False, index=True)
    email = Column(String(150))
    parent_name = Column(String(150))
    course_interested = Column(String(150))
    department = Column(String(150))
    lead_status = Column(String(50), default='New')
    lead_sub_status = Column(String(100))
    lead_source = Column(String(100))
    lead_score = Column(Integer, default=0)
    lead_strength = Column(String(50), default='Cold')
    admission_probability = Column(Integer, default=0)
    assigned_to = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    assigned_team_id = Column(Integer, ForeignKey('crm_teams.id'), nullable=True)
    remarks = Column(Text)
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    utm_content = Column(String(100))
    utm_term = Column(String(100))
    city = Column(String(100))
    state = Column(String(100))
    gender = Column(String(20))
    qualification = Column(String(100))
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    followups = relationship('CRMFollowUp', back_populates='lead')
    applications = relationship('CRMApplication', back_populates='lead')
    activities = relationship('CRMLeadActivity', back_populates='lead')
    assigned_user = relationship('CRMUser', foreign_keys=[assigned_to])


class CRMFollowUp(Base):
    __tablename__ = 'crm_followups'
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey('crm_leads.id'))
    follow_up_date = Column(DateTime(timezone=True))
    follow_up_type = Column(String(50))
    follow_up_status = Column(String(50), default='Pending')
    remarks = Column(Text)
    next_follow_up_date = Column(DateTime(timezone=True), nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship('CRMLead', back_populates='followups')


class CRMApplication(Base):
    __tablename__ = 'crm_applications'
    id = Column(Integer, primary_key=True, index=True)
    application_number = Column(String(50), unique=True, index=True)
    lead_id = Column(Integer, ForeignKey('crm_leads.id'))
    program = Column(String(150))
    department = Column(String(150))
    batch_year = Column(String(20))
    application_status = Column(String(50), default='Draft')
    application_fee_paid = Column(Boolean, default=False)
    token_fee_paid = Column(Boolean, default=False)
    documents_submitted = Column(Boolean, default=False)
    documents_verified = Column(Boolean, default=False)
    form_data = Column(Text)
    counselor_id = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    withdrawn_at = Column(DateTime(timezone=True), nullable=True)
    withdrawal_reason = Column(Text)
    notes = Column(Text)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    lead = relationship('CRMLead', back_populates='applications')
    documents = relationship('CRMDocument', back_populates='application')
    payments = relationship('CRMPayment', back_populates='application')


class CRMDocument(Base):
    __tablename__ = 'crm_documents'
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey('crm_applications.id'))
    document_type = Column(String(100))
    document_name = Column(String(200))
    document_url = Column(String(500))
    file_size = Column(Integer, default=0)
    verification_status = Column(String(50), default='Pending')
    verification_notes = Column(Text)
    verified_by = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship('CRMApplication', back_populates='documents')


class CRMPayment(Base):
    __tablename__ = 'crm_payments'
    id = Column(Integer, primary_key=True, index=True)
    payment_reference = Column(String(100), unique=True, index=True)
    application_id = Column(Integer, ForeignKey('crm_applications.id'), nullable=True)
    lead_id = Column(Integer, ForeignKey('crm_leads.id'), nullable=True)
    fee_type = Column(String(100))
    amount = Column(Float, default=0.0)
    currency = Column(String(10), default='INR')
    payment_status = Column(String(50), default='Pending')
    payment_mode = Column(String(50))
    gateway_reference = Column(String(200))
    due_date = Column(DateTime(timezone=True), nullable=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    late_fee = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    notes = Column(Text)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship('CRMApplication', back_populates='payments')


class CRMEmailTemplate(Base):
    __tablename__ = 'crm_email_templates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    subject = Column(String(300))
    body_html = Column(Text)
    body_text = Column(Text)
    category = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMEmailCampaign(Base):
    __tablename__ = 'crm_email_campaigns'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    subject = Column(String(300))
    template_id = Column(Integer, ForeignKey('crm_email_templates.id'), nullable=True)
    body_html = Column(Text)
    status = Column(String(50), default='Draft')
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    target_filter = Column(Text)
    total_recipients = Column(Integer, default=0)
    delivered = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
    bounced = Column(Integer, default=0)
    unsubscribed = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMSMSLog(Base):
    __tablename__ = 'crm_sms_logs'
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey('crm_leads.id'), nullable=True)
    mobile_number = Column(String(20))
    message = Column(Text)
    template_id = Column(String(100))
    status = Column(String(50), default='queued')
    credits_used = Column(Integer, default=1)
    gateway_reference = Column(String(200))
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMCallLog(Base):
    __tablename__ = 'crm_call_logs'
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(String(100), unique=True, index=True)
    lead_id = Column(Integer, ForeignKey('crm_leads.id'), nullable=True)
    agent_id = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    agent_name = Column(String(100))
    call_type = Column(String(50))
    call_status = Column(String(50))
    duration_seconds = Column(Integer, default=0)
    disposition = Column(String(100))
    notes = Column(Text)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMRecording(Base):
    __tablename__ = 'crm_recordings'
    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(String(100), unique=True, index=True)
    call_id = Column(String(100), ForeignKey('crm_call_logs.call_id'))
    lead_name = Column(String(150))
    agent_name = Column(String(100))
    duration_seconds = Column(Integer, default=0)
    recording_url = Column(String(255))
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMWhatsAppLog(Base):
    __tablename__ = 'crm_whatsapp_logs'
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey('crm_leads.id'), nullable=True)
    mobile_number = Column(String(20))
    message = Column(Text)
    template_name = Column(String(100))
    template_category = Column(String(50))
    direction = Column(String(20), default='outbound')
    status = Column(String(50), default='sent')
    waba_message_id = Column(String(200))
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMWhatsAppTemplate(Base):
    __tablename__ = 'crm_whatsapp_templates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    category = Column(String(50))
    language = Column(String(20), default='en')
    body_text = Column(Text)
    header_text = Column(String(200))
    footer_text = Column(String(200))
    approval_status = Column(String(50), default='Pending')
    variables = Column(Text)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMAutomation(Base):
    __tablename__ = 'crm_automations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(Text)
    trigger_event = Column(String(100))
    conditions = Column(Text)
    actions = Column(Text)
    timing = Column(String(50), default='Immediate')
    delay_minutes = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    execution_count = Column(Integer, default=0)
    last_executed_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    logs = relationship('CRMAutomationLog', back_populates='automation')


class CRMAutomationLog(Base):
    __tablename__ = 'crm_automation_logs'
    id = Column(Integer, primary_key=True, index=True)
    automation_id = Column(Integer, ForeignKey('crm_automations.id'))
    trigger_data = Column(Text)
    status = Column(String(50), default='success')
    error_message = Column(Text)
    executed_at = Column(DateTime(timezone=True), server_default=func.now())

    automation = relationship('CRMAutomation', back_populates='logs')


class CRMCampaign(Base):
    __tablename__ = 'crm_campaigns'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    utm_content = Column(String(100))
    utm_term = Column(String(100))
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    budget = Column(Float, default=0.0)
    total_leads = Column(Integer, default=0)
    total_applications = Column(Integer, default=0)
    total_enrollments = Column(Integer, default=0)
    cost_per_lead = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMQueryTicket(Base):
    __tablename__ = 'crm_query_tickets'
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), unique=True, index=True)
    lead_id = Column(Integer, ForeignKey('crm_leads.id'), nullable=True)
    subject = Column(String(300))
    description = Column(Text)
    category = Column(String(100))
    priority = Column(String(50), default='Medium')
    status = Column(String(50), default='Open')
    assigned_to = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    source = Column(String(50))
    resolution_notes = Column(Text)
    sla_due_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    replies = relationship('CRMQueryReply', back_populates='ticket')


class CRMQueryReply(Base):
    __tablename__ = 'crm_query_replies'
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey('crm_query_tickets.id'))
    message = Column(Text)
    replied_by = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    is_internal = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ticket = relationship('CRMQueryTicket', back_populates='replies')


class CRMLeadActivity(Base):
    __tablename__ = 'crm_lead_activities'
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey('crm_leads.id'))
    activity_type = Column(String(100))
    description = Column(Text)
    performed_by = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    extra_data = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship('CRMLead', back_populates='activities')


class CRMNotification(Base):
    __tablename__ = 'crm_notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('crm_users.id'))
    title = Column(String(200))
    message = Column(Text)
    notification_type = Column(String(50))
    related_id = Column(Integer)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMWebhook(Base):
    __tablename__ = 'crm_webhooks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    url = Column(String(500))
    events = Column(Text)
    secret_key = Column(String(200))
    is_active = Column(Boolean, default=True)
    last_triggered_at = Column(DateTime(timezone=True), nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMReport(Base):
    __tablename__ = 'crm_reports'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(Text)
    entity = Column(String(100))
    filters = Column(Text)
    columns = Column(Text)
    group_by = Column(String(100))
    sort_by = Column(String(100))
    sort_order = Column(String(10), default='asc')
    is_scheduled = Column(Boolean, default=False)
    schedule_email = Column(String(150))
    created_by = Column(Integer, ForeignKey('crm_users.id'), nullable=True)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CRMDashboardMetric(Base):
    __tablename__ = 'crm_dashboard_metrics'
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), index=True)
    metric_value = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
