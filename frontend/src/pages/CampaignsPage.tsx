import { useEffect, useState } from 'react'
import { Badge, Button, Card, Col, Form, Modal, Row, Table } from 'react-bootstrap'
import { getCampaigns, createCampaign, updateCampaign, getCampaignStats } from '../services/api'

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<any[]>([])
  const [stats, setStats] = useState<any>({})
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ name: '', utm_source: '', utm_medium: '', utm_campaign: '', utm_term: '', utm_content: '', budget: '' })

  const load = async () => {
    const [cr, sr] = await Promise.all([getCampaigns(), getCampaignStats()])
    setCampaigns(cr.data)
    setStats(sr.data)
  }

  useEffect(() => { load() }, [])

  const save = async () => {
    await createCampaign({ ...form, budget: form.budget ? parseFloat(form.budget) : null })
    setShowModal(false)
    load()
  }

  const toggle = async (c: any) => {
    await updateCampaign(c.id, { is_active: !c.is_active })
    load()
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">Campaign Management (UTM Tracking)</h4>
        <Button size="sm" onClick={() => setShowModal(true)}>+ New Campaign</Button>
      </div>

      <Row className="g-3 mb-4">
        <Col md={3}>
          <Card className="text-center" border="primary">
            <Card.Body><div className="h4 text-primary">{stats.total_campaigns || 0}</div><div className="text-muted small">Total Campaigns</div></Card.Body>
          </Card>
        </Col>
        {Object.entries(stats.source_breakdown || {}).slice(0, 3).map(([src, count]) => (
          <Col md={3} key={src}>
            <Card className="text-center">
              <Card.Body><div className="h4">{count as number}</div><div className="text-muted small">{src}</div></Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Card>
        <Card.Body className="p-0">
          <Table hover responsive className="mb-0">
            <thead className="table-light">
              <tr><th>Name</th><th>Source</th><th>Medium</th><th>Campaign</th><th>Budget</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {campaigns.length === 0 && <tr><td colSpan={7} className="text-center text-muted py-4">No campaigns found</td></tr>}
              {campaigns.map((c) => (
                <tr key={c.id}>
                  <td>{c.name}</td>
                  <td><code>{c.utm_source}</code></td>
                  <td>{c.utm_medium}</td>
                  <td>{c.utm_campaign}</td>
                  <td>{c.budget ? `₹${c.budget.toLocaleString()}` : '—'}</td>
                  <td><Badge bg={c.is_active ? 'success' : 'secondary'}>{c.is_active ? 'Active' : 'Paused'}</Badge></td>
                  <td>
                    <Button size="sm" variant={c.is_active ? 'outline-warning' : 'outline-success'} onClick={() => toggle(c)}>
                      {c.is_active ? 'Pause' : 'Activate'}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton><Modal.Title>New UTM Campaign</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-2"><Form.Label>Campaign Name</Form.Label><Form.Control value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></Form.Group>
            <Row>
              <Col><Form.Group className="mb-2"><Form.Label>UTM Source</Form.Label><Form.Control value={form.utm_source} onChange={(e) => setForm({ ...form, utm_source: e.target.value })} placeholder="google" /></Form.Group></Col>
              <Col><Form.Group className="mb-2"><Form.Label>UTM Medium</Form.Label><Form.Control value={form.utm_medium} onChange={(e) => setForm({ ...form, utm_medium: e.target.value })} placeholder="cpc" /></Form.Group></Col>
            </Row>
            <Form.Group className="mb-2"><Form.Label>UTM Campaign</Form.Label><Form.Control value={form.utm_campaign} onChange={(e) => setForm({ ...form, utm_campaign: e.target.value })} placeholder="summer_intake_2025" /></Form.Group>
            <Row>
              <Col><Form.Group className="mb-2"><Form.Label>UTM Term</Form.Label><Form.Control value={form.utm_term} onChange={(e) => setForm({ ...form, utm_term: e.target.value })} /></Form.Group></Col>
              <Col><Form.Group className="mb-2"><Form.Label>UTM Content</Form.Label><Form.Control value={form.utm_content} onChange={(e) => setForm({ ...form, utm_content: e.target.value })} /></Form.Group></Col>
            </Row>
            <Form.Group className="mb-2"><Form.Label>Budget (₹)</Form.Label><Form.Control type="number" value={form.budget} onChange={(e) => setForm({ ...form, budget: e.target.value })} /></Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
          <Button onClick={save}>Create Campaign</Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
