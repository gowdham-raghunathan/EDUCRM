import { useEffect, useState } from 'react'
import { Badge, Button, Card, Col, Form, Modal, Row, Table } from 'react-bootstrap'
import { getTickets, createTicket, updateTicket, getTicketStats, replyToTicket } from '../services/api'

const PRIORITIES = ['Low', 'Medium', 'High', 'Urgent']
const STATUSES = ['Open', 'In Progress', 'Resolved', 'Closed']

function priorityBadge(p: string) {
  const map: Record<string, string> = { Low: 'secondary', Medium: 'info', High: 'warning', Urgent: 'danger' }
  return <Badge bg={map[p] || 'secondary'}>{p}</Badge>
}

function statusBadge(s: string) {
  const map: Record<string, string> = { Open: 'primary', 'In Progress': 'warning', Resolved: 'success', Closed: 'dark' }
  return <Badge bg={map[s] || 'secondary'}>{s}</Badge>
}

export default function QueryManagerPage() {
  const [tickets, setTickets] = useState<any[]>([])
  const [stats, setStats] = useState<any>({})
  const [showModal, setShowModal] = useState(false)
  const [showReplyModal, setShowReplyModal] = useState(false)
  const [selectedTicket, setSelectedTicket] = useState<any>(null)
  const [replyText, setReplyText] = useState('')
  const [form, setForm] = useState({ lead_id: '', subject: '', description: '', priority: 'Medium', category: 'General' })

  const load = async () => {
    const [tr, sr] = await Promise.all([getTickets(), getTicketStats()])
    setTickets(tr.data)
    setStats(sr.data)
  }

  useEffect(() => { load() }, [])

  const save = async () => { await createTicket(form); setShowModal(false); load() }

  const changeStatus = async (id: number, status: string) => {
    await updateTicket(id, { status })
    load()
  }

  const submitReply = async () => {
    await replyToTicket(selectedTicket.id, { reply: replyText })
    setShowReplyModal(false)
    setReplyText('')
    load()
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">Query Manager (QMS)</h4>
        <Button size="sm" onClick={() => setShowModal(true)}>+ New Ticket</Button>
      </div>

      <Row className="g-3 mb-4">
        {[
          { label: 'Open', value: stats.open || 0, color: 'primary' },
          { label: 'In Progress', value: stats.in_progress || 0, color: 'warning' },
          { label: 'Resolved', value: stats.resolved || 0, color: 'success' },
          { label: 'Overdue', value: stats.overdue || 0, color: 'danger' },
          { label: 'Urgent', value: stats.urgent || 0, color: 'danger' },
        ].map((s) => (
          <Col key={s.label}>
            <Card border={s.color} className="text-center">
              <Card.Body className="py-2">
                <div className={`h5 text-${s.color} mb-0`}>{s.value}</div>
                <div className="text-muted" style={{ fontSize: '0.75rem' }}>{s.label}</div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Card>
        <Card.Body className="p-0">
          <Table hover responsive className="mb-0">
            <thead className="table-light">
              <tr><th>Ticket #</th><th>Subject</th><th>Category</th><th>Priority</th><th>Status</th><th>SLA</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {tickets.length === 0 && <tr><td colSpan={7} className="text-center text-muted py-4">No tickets found</td></tr>}
              {tickets.map((t) => (
                <tr key={t.id}>
                  <td><code>{t.ticket_number}</code></td>
                  <td>{t.subject}</td>
                  <td>{t.category}</td>
                  <td>{priorityBadge(t.priority)}</td>
                  <td>{statusBadge(t.status)}</td>
                  <td className="small text-muted">{t.sla_deadline ? new Date(t.sla_deadline).toLocaleString() : '—'}</td>
                  <td>
                    <Button size="sm" variant="outline-primary" className="me-1" onClick={() => { setSelectedTicket(t); setShowReplyModal(true) }}>Reply</Button>
                    <Form.Select size="sm" style={{ width: 'auto', display: 'inline-block' }} value={t.status} onChange={(e) => changeStatus(t.id, e.target.value)}>
                      {STATUSES.map((s) => <option key={s}>{s}</option>)}
                    </Form.Select>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton><Modal.Title>New Ticket</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-2"><Form.Label>Lead ID (optional)</Form.Label><Form.Control type="number" value={form.lead_id} onChange={(e) => setForm({ ...form, lead_id: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Subject</Form.Label><Form.Control value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Category</Form.Label>
              <Form.Select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {['General', 'Admission', 'Fee', 'Document', 'Technical', 'Other'].map((c) => <option key={c}>{c}</option>)}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2"><Form.Label>Priority</Form.Label>
              <Form.Select value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
                {PRIORITIES.map((p) => <option key={p}>{p}</option>)}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2"><Form.Label>Description</Form.Label><Form.Control as="textarea" rows={3} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
          <Button onClick={save}>Create Ticket</Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showReplyModal} onHide={() => setShowReplyModal(false)}>
        <Modal.Header closeButton><Modal.Title>Reply to {selectedTicket?.ticket_number}</Modal.Title></Modal.Header>
        <Modal.Body>
          <p className="text-muted small mb-2">{selectedTicket?.subject}</p>
          <Form.Control as="textarea" rows={4} placeholder="Type your reply..." value={replyText} onChange={(e) => setReplyText(e.target.value)} />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowReplyModal(false)}>Cancel</Button>
          <Button onClick={submitReply}>Send Reply</Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
