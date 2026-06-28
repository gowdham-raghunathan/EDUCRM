import { useEffect, useState } from 'react'
import { Badge, Button, Card, Col, Form, Modal, Nav, Row, Table } from 'react-bootstrap'
import {
  getEmailTemplates, createEmailTemplate, getEmailCampaigns, createEmailCampaign, sendEmailCampaign,
} from '../services/api'

export default function EmailCampaignsPage() {
  const [tab, setTab] = useState('campaigns')
  const [templates, setTemplates] = useState<any[]>([])
  const [campaigns, setCampaigns] = useState<any[]>([])
  const [showTplModal, setShowTplModal] = useState(false)
  const [showCampModal, setShowCampModal] = useState(false)
  const [tplForm, setTplForm] = useState({ name: '', subject: '', body: '', template_type: 'Promotional' })
  const [campForm, setCampForm] = useState({ name: '', subject: '', body: '', template_id: '' })

  const load = async () => {
    const [tr, cr] = await Promise.all([getEmailTemplates(), getEmailCampaigns()])
    setTemplates(tr.data)
    setCampaigns(cr.data)
  }

  useEffect(() => { load() }, [])

  const saveTpl = async () => { await createEmailTemplate(tplForm); setShowTplModal(false); load() }
  const saveCamp = async () => { await createEmailCampaign(campForm); setShowCampModal(false); load() }
  const send = async (id: number) => { await sendEmailCampaign(id); load() }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">Email Campaigns</h4>
        <div className="d-flex gap-2">
          <Button size="sm" variant="outline-primary" onClick={() => setShowTplModal(true)}>+ Template</Button>
          <Button size="sm" onClick={() => setShowCampModal(true)}>+ Campaign</Button>
        </div>
      </div>

      <Nav variant="tabs" className="mb-3" activeKey={tab} onSelect={(k) => setTab(k || 'campaigns')}>
        <Nav.Item><Nav.Link eventKey="campaigns">Campaigns ({campaigns.length})</Nav.Link></Nav.Item>
        <Nav.Item><Nav.Link eventKey="templates">Templates ({templates.length})</Nav.Link></Nav.Item>
      </Nav>

      {tab === 'campaigns' && (
        <Card>
          <Card.Body className="p-0">
            <Table hover responsive className="mb-0">
              <thead className="table-light">
                <tr><th>Name</th><th>Subject</th><th>Status</th><th>Sent</th><th>Actions</th></tr>
              </thead>
              <tbody>
                {campaigns.length === 0 && <tr><td colSpan={5} className="text-center text-muted py-4">No campaigns yet</td></tr>}
                {campaigns.map((c) => (
                  <tr key={c.id}>
                    <td>{c.name}</td>
                    <td>{c.subject}</td>
                    <td><Badge bg={c.status === 'Sent' ? 'success' : c.status === 'Scheduled' ? 'warning' : 'secondary'}>{c.status}</Badge></td>
                    <td>{c.sent_at ? new Date(c.sent_at).toLocaleDateString() : '—'}</td>
                    <td>
                      {c.status === 'Draft' && (
                        <Button size="sm" variant="success" onClick={() => send(c.id)}>Send Now</Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Card.Body>
        </Card>
      )}

      {tab === 'templates' && (
        <Row className="g-3">
          {templates.length === 0 && <Col><p className="text-muted">No templates yet</p></Col>}
          {templates.map((t) => (
            <Col md={4} key={t.id}>
              <Card>
                <Card.Body>
                  <div className="fw-semibold">{t.name}</div>
                  <div className="text-muted small mb-2">{t.subject}</div>
                  <Badge bg="info">{t.template_type}</Badge>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      )}

      <Modal show={showTplModal} onHide={() => setShowTplModal(false)}>
        <Modal.Header closeButton><Modal.Title>New Email Template</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-2"><Form.Label>Name</Form.Label><Form.Control value={tplForm.name} onChange={(e) => setTplForm({ ...tplForm, name: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Subject</Form.Label><Form.Control value={tplForm.subject} onChange={(e) => setTplForm({ ...tplForm, subject: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Type</Form.Label>
              <Form.Select value={tplForm.template_type} onChange={(e) => setTplForm({ ...tplForm, template_type: e.target.value })}>
                {['Promotional', 'Transactional', 'Newsletter', 'Drip'].map((t) => <option key={t}>{t}</option>)}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2"><Form.Label>Body (HTML)</Form.Label><Form.Control as="textarea" rows={5} value={tplForm.body} onChange={(e) => setTplForm({ ...tplForm, body: e.target.value })} /></Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowTplModal(false)}>Cancel</Button>
          <Button onClick={saveTpl}>Save Template</Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showCampModal} onHide={() => setShowCampModal(false)}>
        <Modal.Header closeButton><Modal.Title>New Email Campaign</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-2"><Form.Label>Campaign Name</Form.Label><Form.Control value={campForm.name} onChange={(e) => setCampForm({ ...campForm, name: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Subject</Form.Label><Form.Control value={campForm.subject} onChange={(e) => setCampForm({ ...campForm, subject: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Use Template</Form.Label>
              <Form.Select value={campForm.template_id} onChange={(e) => setCampForm({ ...campForm, template_id: e.target.value })}>
                <option value="">Custom body</option>
                {templates.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2"><Form.Label>Body</Form.Label><Form.Control as="textarea" rows={4} value={campForm.body} onChange={(e) => setCampForm({ ...campForm, body: e.target.value })} /></Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowCampModal(false)}>Cancel</Button>
          <Button onClick={saveCamp}>Create Campaign</Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
