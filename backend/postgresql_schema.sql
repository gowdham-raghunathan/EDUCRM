CREATE TABLE crm_leads (
  id SERIAL PRIMARY KEY,
  lead_id VARCHAR(50) UNIQUE NOT NULL,
  student_name VARCHAR(150) NOT NULL,
  mobile_number VARCHAR(20) NOT NULL,
  email VARCHAR(150),
  course_interested VARCHAR(150),
  lead_status VARCHAR(50) DEFAULT 'New',
  admission_probability INTEGER DEFAULT 0,
  remarks TEXT,
  deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_crm_leads_mobile ON crm_leads (mobile_number);
CREATE INDEX idx_crm_leads_status ON crm_leads (lead_status);

CREATE TABLE crm_followups (
  id SERIAL PRIMARY KEY,
  lead_id INTEGER REFERENCES crm_leads(id),
  follow_up_date TIMESTAMP WITH TIME ZONE,
  follow_up_type VARCHAR(50),
  follow_up_status VARCHAR(50) DEFAULT 'Pending',
  remarks TEXT,
  deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crm_call_logs (
  id SERIAL PRIMARY KEY,
  call_id VARCHAR(100) UNIQUE NOT NULL,
  lead_id INTEGER REFERENCES crm_leads(id),
  agent_name VARCHAR(100),
  call_type VARCHAR(50),
  call_status VARCHAR(50),
  duration_seconds INTEGER DEFAULT 0,
  deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crm_recordings (
  id SERIAL PRIMARY KEY,
  recording_id VARCHAR(100) UNIQUE NOT NULL,
  call_id VARCHAR(100) REFERENCES crm_call_logs(call_id),
  lead_name VARCHAR(150),
  agent_name VARCHAR(100),
  duration_seconds INTEGER DEFAULT 0,
  recording_url VARCHAR(255),
  deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crm_whatsapp_logs (
  id SERIAL PRIMARY KEY,
  lead_id INTEGER REFERENCES crm_leads(id),
  message TEXT,
  status VARCHAR(50) DEFAULT 'sent',
  deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crm_users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  full_name VARCHAR(150),
  role VARCHAR(50) DEFAULT 'counselor',
  deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crm_dashboard_metrics (
  id SERIAL PRIMARY KEY,
  metric_name VARCHAR(100),
  metric_value INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
