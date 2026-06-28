import { useEffect, useState } from 'react'
import { Badge, Button, Card, Col, Form, Modal, Row } from 'react-bootstrap'
import { getAutomations, createAutomation, toggleAutomation, executeAutomation } from '../services/api'

const TRIGGERS = [
  'lead_created', 'lead_stage_changed', 'follow_up_due', 'application_submitted',
  'payment_due', 'payment_received', 'ticket_created', 'ticket_overdue',
]
const ACTIONS = [
  'send_whatsapp', 'send_sms', 'send_email', 'assign_counselor',
  'create_follow_up', 'update_lead_stage', 'notify_team',
]

export default function AutomationsPage() {
  const [automations, setAutomations] = useState<any[]>([])
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ name: '', trigger_event: TRIGGERS[0], action_type: ACTIONS[0], action_config: '{}', description: '' })

  const load = () => getAutomations().then((r) => setAutomations(r.data))

  useEffect(() => { load() }, [])

  const save = async () => {
    await createAutomation({ ...form, action_config: JSON.parse(form.action_config || '{}') })
    setShowModal(false)
    load()
  }

  const toggle = async (id: number) => { await toggleAutomation(id); load() }
  const run = async (id: number) => { await executeAutomation(id); load() }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">Automation Engine</h4>
        <Button size="sm" onClick={() => setShowModal(true)}>+ New Automation</Button>
      </div>

      {automations.length === 0 && (
        <Card body className="text-center text-muted py-5">
          No automations configured. Create one to start automating workflows.
        </Card>
      )}

      <Row className="g-3">
        {automations.map((a) => (
          <Col md={6} lg={4} key={a.id}>
            <Card className={`h-100 ${a.is_active ? 'border-success' : ''}`}>
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <div className="fw-semibold">{a.name}</div>
                  <Badge bg={a.is_active ? 'success' : 'secondary'}>{a.is_active ? 'Active' : 'Inactive'}</Badge>
                </div>
                <div className="small text-muted mb-1">
                  <span className="fw-semibold">Trigger:</span> {a.trigger_event}
                </div>
                <div className="small text-muted mb-2">
                  <span className="fw-semibold">Action:</span> {a.action_type}
                </div>
                {a.description && <p className="small text-muted mb-2">{a.description}</p>}
                <div className="d-flex gap-2 mt-2">
                  <Button size="sm" variant={a.is_active ? 'outline-warning' : 'outline-success'} onClick={() => toggle(a.id)}>
                    {a.is_active ? 'Disable' : 'Enable'}
                  </Button>
                  <Button size="sm" variant="outline-primary" onClick={() => run(a.id)}>Run Now</Button>
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton><Modal.Title>New Automation</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-2"><Form.Label>Name</Form.Label><Form.Control value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Description</Form.Label><Form.Control value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Trigger Event</Form.Label>
              <Form.Select value={form.trigger_event} onChange={(e) => setForm({ ...form, trigger_event: e.target.value })}>
                {TRIGGERS.map((t) => <option key={t}>{t}</option>)}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Action Type</Form.Label>
              <Form.Select value={form.action_type} onChange={(e) => setForm({ ...form, action_type: e.target.value })}>
                {ACTIONS.map((a) => <option key={a}>{a}</option>)}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Action Config (JSON)</Form.Label>
              <Form.Control as="textarea" rows={3} value={form.action_config} onChange={(e) => setForm({ ...form, action_config: e.target.value })} placeholder='{"message": "Hello {{name}}"}' />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
          <Button onClick={save}>Create Automation</Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
