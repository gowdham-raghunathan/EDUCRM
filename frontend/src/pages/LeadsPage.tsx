import { useEffect, useState } from 'react'
import { Button, Card, Col, Form, Row, Table } from 'react-bootstrap'
import CTISoftphoneWidget from '../components/CTISoftphoneWidget'
import LeadFormModal from '../components/LeadFormModal'
import LeadTimeline from '../components/LeadTimeline'
import api from '../services/api'

function LeadsPage() {
  const [leads, setLeads] = useState<any[]>([])
  const [showModal, setShowModal] = useState(false)
  const [selectedLead, setSelectedLead] = useState<any | null>(null)
  const [role, setRole] = useState('counselor')

  const loadLeads = () => {
    api.get('/api/leads').then((response) => setLeads(response.data)).catch(() => setLeads([]))
  }

  const handleDelete = async (leadId: number) => {
    if (!window.confirm('Delete this lead?')) return
    try {
      await api.delete(`/api/leads/${leadId}`)
      loadLeads()
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    loadLeads()
    const storedRole = localStorage.getItem('user_role') || 'counselor'
    setRole(storedRole)
  }, [])
  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 className="fw-bold mb-1">Admission Leads</h3>
          <p className="text-muted mb-0">Capture, qualify, and route student enquiries.</p>
        </div>
        {role !== 'counselor' ? (
          <Button variant="primary" onClick={() => setShowModal(true)}><i className="bi bi-plus-circle me-2"></i>New Lead</Button>
        ) : null}
      </div>

      <Row className="g-4">
        <Col lg={8}>
          <Card className="border-0 mb-4">
            <Card.Body>
              <h5 className="mb-3">Lead Enquiry Form</h5>
              <Row className="g-3">
                <Col md={6}><Form.Control placeholder="Lead ID" /></Col>
                <Col md={6}><Form.Control type="date" /></Col>
                <Col md={6}><Form.Control placeholder="Student Name" /></Col>
                <Col md={6}><Form.Control placeholder="Mobile Number" /></Col>
                <Col md={6}><Form.Control placeholder="Email ID" /></Col>
                <Col md={6}><Form.Control placeholder="Parent Name" /></Col>
                <Col md={6}><Form.Control placeholder="Course Interested" /></Col>
                <Col md={6}><Form.Control placeholder="Department" /></Col>
                <Col md={6}><Form.Control placeholder="Lead Source" /></Col>
                <Col md={6}><Form.Control placeholder="Assigned Counselor" /></Col>
                <Col md={6}><Form.Control placeholder="Lead Status" /></Col>
                <Col md={6}><Form.Control placeholder="Admission Probability" /></Col>
                <Col xs={12}><Form.Control as="textarea" rows={3} placeholder="Remarks" /></Col>
              </Row>
              <div className="d-flex flex-wrap gap-2 mt-3">
                <Button variant="primary">Save Lead</Button>
                <Button variant="outline-primary">Call Now</Button>
                <Button variant="outline-success">WhatsApp</Button>
                <Button variant="outline-info">Send Email</Button>
                <Button variant="outline-warning">Schedule Follow-up</Button>
              </div>
            </Card.Body>
          </Card>

          <Card className="border-0">
            <Card.Body>
              <h5 className="mb-3">Lead Queue</h5>
              <Table responsive hover>
                <thead>
                  <tr>
                    <th>Lead ID</th>
                    <th>Student</th>
                    <th>Course</th>
                    <th>Status</th>
                    <th>Probability</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.map((lead: any) => (
                    <tr key={lead.id}>
                      <td>{lead.lead_id}</td>
                      <td>{lead.student_name}</td>
                      <td>{lead.course_interested ?? '—'}</td>
                      <td>{lead.lead_status}</td>
                      <td>{lead.admission_probability}%</td>
                      <td>
                        <div className="d-flex gap-2">
                          <Button variant="outline-primary" size="sm" onClick={() => { setSelectedLead(lead); setShowModal(true) }}>Edit</Button>
                          {(role === 'manager' || role === 'admin') ? (
                            <Button variant="outline-danger" size="sm" onClick={() => handleDelete(lead.id)}>Delete</Button>
                          ) : null}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        <Col lg={4}>
          <CTISoftphoneWidget />
          <div className="mt-4">
            <LeadTimeline />
          </div>
        </Col>
      </Row>
      <LeadFormModal
        show={showModal}
        onHide={() => { setShowModal(false); setSelectedLead(null) }}
        lead={selectedLead || undefined}
        onSaved={loadLeads}
      />
    </div>
  )
}

export default LeadsPage
