import { useEffect, useState } from 'react'
import { Badge, Button, Card, Col, Form, Modal, Row, Table } from 'react-bootstrap'
import { getPayments, createPayment, updatePayment, getPaymentStats } from '../services/api'

function statusBadge(status: string) {
  const map: Record<string, string> = { Pending: 'warning', Paid: 'success', Overdue: 'danger', Waived: 'secondary', Refunded: 'info' }
  return <Badge bg={map[status] || 'secondary'}>{status}</Badge>
}

export default function PaymentsPage() {
  const [payments, setPayments] = useState<any[]>([])
  const [stats, setStats] = useState<any>({})
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ lead_id: '', application_id: '', fee_type: '', amount: '', due_date: '' })

  const load = async () => {
    const [pr, sr] = await Promise.all([getPayments(), getPaymentStats()])
    setPayments(pr.data)
    setStats(sr.data)
  }

  useEffect(() => { load() }, [])

  const save = async () => {
    await createPayment({ ...form, amount: parseFloat(form.amount) })
    setShowModal(false)
    load()
  }

  const markPaid = async (id: number) => {
    await updatePayment(id, { payment_status: 'Paid' })
    load()
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">Fee & Payments (Collexo)</h4>
        <Button size="sm" onClick={() => setShowModal(true)}>+ Add Payment</Button>
      </div>

      <Row className="g-3 mb-4">
        {[
          { label: 'Total Collected', value: `₹${(stats.total_collected || 0).toLocaleString()}`, color: 'success' },
          { label: 'Pending', value: `₹${(stats.total_pending || 0).toLocaleString()}`, color: 'warning' },
          { label: 'Overdue', value: `₹${(stats.total_overdue || 0).toLocaleString()}`, color: 'danger' },
        ].map((s) => (
          <Col md={4} key={s.label}>
            <Card border={s.color} className="text-center">
              <Card.Body>
                <div className={`h4 text-${s.color}`}>{s.value}</div>
                <div className="text-muted small">{s.label}</div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Card>
        <Card.Body className="p-0">
          <Table hover responsive className="mb-0">
            <thead className="table-light">
              <tr><th>Reference</th><th>Lead</th><th>Fee Type</th><th>Amount</th><th>Due</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {payments.length === 0 && <tr><td colSpan={7} className="text-center text-muted py-4">No payments found</td></tr>}
              {payments.map((p) => (
                <tr key={p.id}>
                  <td><code>{p.payment_reference}</code></td>
                  <td>{p.lead_id}</td>
                  <td>{p.fee_type}</td>
                  <td>₹{p.amount?.toLocaleString()}</td>
                  <td>{p.due_date?.slice(0, 10)}</td>
                  <td>{statusBadge(p.payment_status)}</td>
                  <td>
                    {p.payment_status === 'Pending' && (
                      <Button size="sm" variant="success" onClick={() => markPaid(p.id)}>Mark Paid</Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton><Modal.Title>Add Payment</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form>
            {[
              { label: 'Lead ID', key: 'lead_id', type: 'number' },
              { label: 'Application ID (optional)', key: 'application_id', type: 'number' },
              { label: 'Amount (₹)', key: 'amount', type: 'number' },
              { label: 'Due Date', key: 'due_date', type: 'date' },
            ].map(({ label, key, type }) => (
              <Form.Group className="mb-3" key={key}>
                <Form.Label>{label}</Form.Label>
                <Form.Control type={type} value={(form as any)[key]} onChange={(e) => setForm({ ...form, [key]: e.target.value })} />
              </Form.Group>
            ))}
            <Form.Group className="mb-3">
              <Form.Label>Fee Type</Form.Label>
              <Form.Select value={form.fee_type} onChange={(e) => setForm({ ...form, fee_type: e.target.value })}>
                <option value="">Select</option>
                {['Application Fee', 'Tuition Fee', 'Hostel Fee', 'Exam Fee', 'Library Fee', 'Other'].map((f) => <option key={f}>{f}</option>)}
              </Form.Select>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
          <Button onClick={save}>Add Payment</Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
