import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ── Leads ──────────────────────────────────────────────────
export const getLeads = (params?: Record<string, string>) => api.get('/api/leads', { params })
export const getLead = (id: number) => api.get(`/api/leads/${id}`)
export const getLeadProfile = (id: number) => api.get(`/api/leads/${id}/profile`)
export const createLead = (data: object) => api.post('/api/leads', data)
export const updateLead = (id: number, data: object) => api.put(`/api/leads/${id}`, data)
export const deleteLead = (id: number) => api.delete(`/api/leads/${id}`)
export const allocateLead = (id: number, data: object) => api.post(`/api/leads/${id}/allocate`, data)
export const scoreLead = (id: number, delta: number) => api.post(`/api/leads/${id}/score`, { delta })

// ── Follow-ups ────────────────────────────────────────────
export const getFollowUps = (params?: Record<string, string>) => api.get('/api/followups', { params })
export const createFollowUp = (data: object) => api.post('/api/followups', data)
export const updateFollowUp = (id: number, data: object) => api.put(`/api/followups/${id}`, data)
export const deleteFollowUp = (id: number) => api.delete(`/api/followups/${id}`)

// ── Applications ──────────────────────────────────────────
export const getApplications = (params?: Record<string, string>) => api.get('/api/applications', { params })
export const getApplication = (id: number) => api.get(`/api/applications/${id}`)
export const createApplication = (data: object) => api.post('/api/applications', data)
export const updateApplication = (id: number, data: object) => api.put(`/api/applications/${id}`, data)
export const deleteApplication = (id: number) => api.delete(`/api/applications/${id}`)

// ── Documents ─────────────────────────────────────────────
export const getDocuments = (applicationId: number) => api.get('/api/documents', { params: { application_id: applicationId } })
export const createDocument = (data: object) => api.post('/api/documents', data)
export const verifyDocument = (id: number, data: object) => api.post(`/api/documents/${id}/verify`, data)
export const deleteDocument = (id: number) => api.delete(`/api/documents/${id}`)

// ── Payments ──────────────────────────────────────────────
export const getPayments = (params?: Record<string, string>) => api.get('/api/payments', { params })
export const createPayment = (data: object) => api.post('/api/payments', data)
export const updatePayment = (id: number, data: object) => api.put(`/api/payments/${id}`, data)
export const getPaymentStats = () => api.get('/api/payments/stats')

// ── Email Templates & Campaigns ───────────────────────────
export const getEmailTemplates = () => api.get('/api/email/templates')
export const createEmailTemplate = (data: object) => api.post('/api/email/templates', data)
export const updateEmailTemplate = (id: number, data: object) => api.put(`/api/email/templates/${id}`, data)
export const deleteEmailTemplate = (id: number) => api.delete(`/api/email/templates/${id}`)
export const getEmailCampaigns = () => api.get('/api/email/campaigns')
export const createEmailCampaign = (data: object) => api.post('/api/email/campaigns', data)
export const sendEmailCampaign = (id: number) => api.post(`/api/email/campaigns/${id}/send`)

// ── SMS ───────────────────────────────────────────────────
export const sendSMS = (data: object) => api.post('/api/sms/send', data)
export const getSMSLogs = (params?: Record<string, string>) => api.get('/api/sms/logs', { params })
export const getSMSStats = () => api.get('/api/sms/stats')

// ── WhatsApp ──────────────────────────────────────────────
export const sendWhatsApp = (data: object) => api.post('/api/whatsapp/send', data)
export const getWhatsAppLogs = (leadId?: number) => api.get('/api/whatsapp/logs', { params: leadId ? { lead_id: leadId } : {} })
export const getWhatsAppTemplates = () => api.get('/api/whatsapp/templates')
export const createWhatsAppTemplate = (data: object) => api.post('/api/whatsapp/templates', data)
export const getWhatsAppStats = () => api.get('/api/whatsapp/stats')

// ── Automations ───────────────────────────────────────────
export const getAutomations = () => api.get('/api/automations')
export const createAutomation = (data: object) => api.post('/api/automations', data)
export const updateAutomation = (id: number, data: object) => api.put(`/api/automations/${id}`, data)
export const toggleAutomation = (id: number) => api.post(`/api/automations/${id}/toggle`)
export const executeAutomation = (id: number) => api.post(`/api/automations/${id}/execute`)
export const getAutomationLogs = (id: number) => api.get(`/api/automations/${id}/logs`)
export const getAutomationMeta = () => api.get('/api/automations/meta')

// ── UTM Campaigns ─────────────────────────────────────────
export const getCampaigns = () => api.get('/api/campaigns')
export const createCampaign = (data: object) => api.post('/api/campaigns', data)
export const updateCampaign = (id: number, data: object) => api.put(`/api/campaigns/${id}`, data)
export const deleteCampaign = (id: number) => api.delete(`/api/campaigns/${id}`)
export const getCampaignStats = () => api.get('/api/campaigns/stats')

// ── Query Manager ─────────────────────────────────────────
export const getTickets = (params?: Record<string, string>) => api.get('/api/queries', { params })
export const getTicket = (id: number) => api.get(`/api/queries/${id}`)
export const createTicket = (data: object) => api.post('/api/queries', data)
export const updateTicket = (id: number, data: object) => api.put(`/api/queries/${id}`, data)
export const getTicketStats = () => api.get('/api/queries/stats')
export const replyToTicket = (id: number, data: object) => api.post(`/api/queries/${id}/reply`, data)

// ── Users & Teams ─────────────────────────────────────────
export const getUsers = () => api.get('/api/users')
export const createUser = (data: object) => api.post('/api/users', data)
export const updateUser = (id: number, data: object) => api.put(`/api/users/${id}`, data)
export const deleteUser = (id: number) => api.delete(`/api/users/${id}`)
export const getTeams = () => api.get('/api/teams')
export const createTeam = (data: object) => api.post('/api/teams', data)
export const addTeamMember = (teamId: number, userId: number) => api.post(`/api/teams/${teamId}/members`, { user_id: userId })
export const removeTeamMember = (teamId: number, userId: number) => api.delete(`/api/teams/${teamId}/members/${userId}`)

// ── Reports ───────────────────────────────────────────────
export const getReports = () => api.get('/api/reports')
export const createReport = (data: object) => api.post('/api/reports', data)
export const runReport = (entity: string, params?: Record<string, string>) => api.get(`/api/reports/run/${entity}`, { params })
export const getDashboardSummary = () => api.get('/api/reports/dashboard-summary')

// ── Activities ────────────────────────────────────────────
export const getLeadActivities = (leadId: number) => api.get(`/api/activities/lead/${leadId}`)
export const addLeadNote = (leadId: number, note: string) => api.post(`/api/activities/lead/${leadId}/note`, { note })

// ── Dashboard ─────────────────────────────────────────────
export const getDashboard = () => api.get('/api/dashboard')
export const getDashboardAnalytics = () => api.get('/api/dashboard/analytics')

export default api
