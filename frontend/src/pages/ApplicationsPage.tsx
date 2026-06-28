import { useEffect, useState } from 'react'
import { Badge, Button, Card, Form, Modal, Table } from 'react-bootstrap'
import { getApplications, createApplication, updateApplication } from '../services/api'

const STATUSES = ['Draft', 'Submitted', 'Under Review', 'Approved', 'Rejected', 'Enrolled', 'Withdrawn']

function statusBadge(status: string) {
  const map: Record<string, string> = {
    Draft: 'secondary', Submitted: 'primary', 'Under Review': 'warning',
    Approved: 'success', Rejected: 'danger', Enrolled: 'info', Withdrawn: 'dark',
  }
  return <Badge bg={map[status] || 'secondary'}>{status}</Badge>
}

export default function ApplicationsPage() {
  const [apps, setApps] = useState<any[]>([])
  const [showModal, setShowModal] = useState(false)
  const [editing, setEditing] = useState<any>(null)
  const [form, setForm] = useState({ lead_id: '', program_applied: '', course_level: '', academic_year: '' })

  const load = () => getApplications().then((r) => setApps(r.data))

  useEffect(() => { load() }, [])

  const openNew = () => { setEditing(null); setForm({ lead_id: '', program_applied: '', course_level: '', academic_year: '' }); setShowModal(true) }
  const openEdit = (a: any) => { setEditing(a); setForm({ lead_id: a.lead_id, program_applied: a.program_applied, course_level: a.course_level, academic_year: a.academic_year }); setShowModal(true) }

  const save = async () => {
    if (editing) await updateApplication(editing.id, form)
    else await createApplication(form)
    setShowModal(false)
    load()
  }

  const changeStatus = async (id: number, status: string) => {
    await updateApplication(id, { application_status: status })
    load()
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">Application Manager</h4>
        <Button size="sm" onClick={openNew}>+ New Application</Button>
      </div>

      <Card>
        <Card.Body className="p-0">
          <Table hover responsive className="mb-0">
            <thead className="table-light">
              <tr>
                <th>App No.</th><th>Lead ID</th><th>Program</th><th>Level</th><th>Year</th><th>Status</th><th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {apps.length === 0 && (
                <tr><td colSpan={7} className="text-center text-muted py-4">No applications found</td></tr>
              )}
              {apps.map((a) => (
                <tr key={a.id}>
                  <td><code>{a.application_number}</code></td>
                  <td>{a.lead_id}</td>
                  <td>{a.program_applied}</td>
                  <td>{a.course_level}</td>
                  <td>{a.academic_year}</td>
                  <td>{statusBadge(a.application_status)}</td>
                  <td>
                    <Button size="sm" variant="outline-secondary" className="me-1" onClick={() => openEdit(a)}>Edit</Button>
                    <Form.Select size="sm" style={{ width: 'auto', display: 'inline-block' }} value={a.application_status} onChange={(e) => changeStatus(a.id, e.target.value)}>
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
        <Modal.Header closeButton><Modal.Title>{editing ? 'Edit Application' : 'New Application'}</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Lead ID</Form.Label>
              <Form.Control type="number" value={form.lead_id} onChange={(e) => setForm({ ...form, lead_id: e.target.value })} />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Program</Form.Label>
              <Form.Control value={form.program_applied} onChange={(e) => setForm({ ...form, program_applied: e.target.value })} />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Course Level</Form.Label>
              <Form.Select value={form.course_level} onChange={(e) => setForm({ ...form, course_level: e.target.value })}>
                <option value="">Select</option>
                {['UG', 'PG', 'Diploma', 'PhD', 'Certificate'].map((l) => <option key={l}>{l}</option>)}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Academic Year</Form.Label>
              <Form.Control value={form.academic_year} onChange={(e) => setForm({ ...form, academic_year: e.target.value })} placeholder="e.g. 2024-25" />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
          <Button onClick={save}>Save</Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
