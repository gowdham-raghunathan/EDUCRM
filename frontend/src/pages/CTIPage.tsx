import { useEffect, useState } from 'react'
import { Badge, Button, Card, Col, Form, Row, Spinner, Table } from 'react-bootstrap'
import api from '../services/api'

interface CallLog {
  id: number
  call_id: string
  lead_id: number | null
  agent_name: string
  call_type: string
  call_status: string
  duration_seconds: number
  notes: string | null
  created_at: string
}

const STATUS_COLOR: Record<string, string> = {
  initiated: 'warning',
  ringing: 'warning',
  'in-progress': 'success',
  completed: 'secondary',
  failed: 'danger',
  busy: 'danger',
  'no-answer': 'secondary',
  canceled: 'dark',
  queued: 'info',
  inbound: 'primary',
}

function formatDuration(secs: number) {
  if (!secs) return '—'
  const m = Math.floor(secs / 60), s = secs % 60
  return `${m}m ${s}s`
}

export default function CTIPage() {
  const [toNumber, setToNumber] = useState('')
  const [leadId, setLeadId] = useState('')
  const [logs, setLogs] = useState<CallLog[]>([])
  const [activeCalls, setActiveCalls] = useState<any[]>([])
  const [calling, setCalling] = useState(false)
  const [lastCall, setLastCall] = useState<any>(null)
  const [error, setError] = useState('')

  const loadLogs = () => api.get('/api/cti/logs').then((r) => setLogs(r.data)).catch(() => {})
  const loadActive = () => api.get('/api/cti/active-calls').then((r) => setActiveCalls(r.data)).catch(() => {})

  useEffect(() => {
    loadLogs()
    loadActive()
    const interval = setInterval(() => { loadLogs(); loadActive() }, 10000)
    return () => clearInterval(interval)
  }, [])

  const makeCall = async () => {
    if (!toNumber) { setError('Enter a phone number'); return }
    setError('')
    setCalling(true)
    setLastCall(null)
    try {
      const res = await api.post('/api/cti/call', {
        to: toNumber,
        lead_id: leadId ? parseInt(leadId) : undefined,
      })
      setLastCall(res.data)
      loadLogs()
      loadActive()
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Call failed')
    } finally {
      setCalling(false)
    }
  }

  const endCall = async (sid: string) => {
    await api.post(`/api/cti/calls/${sid}/end`)
    loadActive()
    loadLogs()
  }

  return (
    <div>
      <h4 className="mb-3">CTI Call Center</h4>
      <Row className="g-3">
        {/* Dialer */}
        <Col md={4}>
          <Card>
            <Card.Header className="fw-semibold d-flex align-items-center gap-2">
              <i className="bi bi-telephone-fill text-success"></i> Click-to-Call
            </Card.Header>
            <Card.Body>
              <Form.Group className="mb-3">
                <Form.Label>Phone Number</Form.Label>
                <Form.Control
                  value={toNumber}
                  onChange={(e) => setToNumber(e.target.value)}
                  placeholder="+91XXXXXXXXXX"
                />
                <Form.Text className="text-muted">Include country code (e.g. +91 for India)</Form.Text>
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Lead ID <span className="text-muted">(optional)</span></Form.Label>
                <Form.Control
                  type="number"
                  value={leadId}
                  onChange={(e) => setLeadId(e.target.value)}
                  placeholder="Auto-links call to lead"
                />
              </Form.Group>

              {error && <div className="alert alert-danger py-2 small">{error}</div>}

              {lastCall && (
                <div className="alert alert-success py-2 small mb-3">
                  <strong>Call initiated!</strong><br />
                  SID: <code>{lastCall.call_sid}</code><br />
                  Status: <Badge bg="warning">{lastCall.call_status}</Badge>
                </div>
              )}

              <Button
                className="w-100"
                variant="success"
                onClick={makeCall}
                disabled={calling}
              >
                {calling ? <><Spinner size="sm" className="me-2" />Connecting…</> : <><i className="bi bi-telephone-fill me-2"></i>Call</>}
              </Button>

              <div className="mt-3 p-2 bg-light rounded small text-muted">
                <strong>Test mode note:</strong> With Twilio test credentials, calls are simulated — no real phone rings. Switch to live credentials and a purchased Twilio number to make real calls.
              </div>
            </Card.Body>
          </Card>

          {/* Active Calls */}
          {activeCalls.length > 0 && (
            <Card className="mt-3 border-success">
              <Card.Header className="fw-semibold text-success">
                <i className="bi bi-circle-fill me-2" style={{ fontSize: '0.6rem' }}></i>
                Live Calls ({activeCalls.length})
              </Card.Header>
              <Card.Body className="p-0">
                {activeCalls.map((c) => (
                  <div key={c.sid} className="d-flex justify-content-between align-items-center p-3 border-bottom">
                    <div>
                      <div className="fw-semibold small">{c.to}</div>
                      <div className="text-muted" style={{ fontSize: '0.75rem' }}>{c.sid}</div>
                    </div>
                    <Button size="sm" variant="outline-danger" onClick={() => endCall(c.sid)}>
                      <i className="bi bi-telephone-x-fill"></i> End
                    </Button>
                  </div>
                ))}
              </Card.Body>
            </Card>
          )}
        </Col>

        {/* Call Logs */}
        <Col md={8}>
          <Card>
            <Card.Header className="fw-semibold d-flex justify-content-between align-items-center">
              <span>Call Log</span>
              <Button size="sm" variant="outline-secondary" onClick={() => { loadLogs(); loadActive() }}>
                <i className="bi bi-arrow-clockwise"></i> Refresh
              </Button>
            </Card.Header>
            <Card.Body className="p-0">
              <Table hover responsive className="mb-0 small">
                <thead className="table-light">
                  <tr>
                    <th>Time</th>
                    <th>Type</th>
                    <th>Call SID</th>
                    <th>Lead</th>
                    <th>Agent</th>
                    <th>Status</th>
                    <th>Duration</th>
                    <th>Notes</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.length === 0 && (
                    <tr><td colSpan={8} className="text-center text-muted py-4">No calls yet</td></tr>
                  )}
                  {logs.map((l) => (
                    <tr key={l.id}>
                      <td className="text-muted">{new Date(l.created_at).toLocaleString()}</td>
                      <td>
                        <Badge bg={l.call_type === 'inbound' ? 'info' : 'primary'}>
                          {l.call_type === 'inbound' ? '↙ In' : '↗ Out'}
                        </Badge>
                      </td>
                      <td><code style={{ fontSize: '0.7rem' }}>{l.call_id?.slice(0, 20)}…</code></td>
                      <td>{l.lead_id || '—'}</td>
                      <td>{l.agent_name || '—'}</td>
                      <td>
                        <Badge bg={STATUS_COLOR[l.call_status] || 'secondary'}>
                          {l.call_status}
                        </Badge>
                      </td>
                      <td>{formatDuration(l.duration_seconds)}</td>
                      <td className="text-muted" style={{ maxWidth: 140, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {l.notes || '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
