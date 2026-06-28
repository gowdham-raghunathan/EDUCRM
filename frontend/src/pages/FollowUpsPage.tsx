import { Button, Card, Col, Form, Row, Table } from 'react-bootstrap'

function FollowUpsPage() {
  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 className="fw-bold mb-1">Follow-up Management</h3>
          <p className="text-muted mb-0">Schedule and track student engagement tasks.</p>
        </div>
        <Button variant="primary">+ New Follow-up</Button>
      </div>

      <Row className="g-4">
        <Col lg={5}>
          <Card className="border-0">
            <Card.Body>
              <h5 className="mb-3">Follow-up Form</h5>
              <Form>
                <Form.Group className="mb-3"><Form.Label>Follow-up Date</Form.Label><Form.Control type="date" /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Follow-up Time</Form.Label><Form.Control type="time" /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Follow-up Type</Form.Label><Form.Select><option>Phone Call</option><option>WhatsApp</option><option>Email</option><option>Campus Visit</option><option>Counseling Session</option></Form.Select></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Follow-up Status</Form.Label><Form.Select><option>Pending</option><option>Completed</option><option>Rescheduled</option></Form.Select></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Remarks</Form.Label><Form.Control as="textarea" rows={3} /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Next Follow-up Date</Form.Label><Form.Control type="date" /></Form.Group>
                <Button variant="primary" className="w-100">Schedule Follow-up</Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
        <Col lg={7}>
          <Card className="border-0">
            <Card.Body>
              <h5 className="mb-3">Pending Follow-ups</h5>
              <Table responsive hover>
                <thead>
                  <tr><th>Lead</th><th>Type</th><th>Status</th><th>Next Date</th></tr>
                </thead>
                <tbody>
                  <tr><td>Aarav Rao</td><td>Phone Call</td><td>Pending</td><td>2026-06-28</td></tr>
                  <tr><td>Meera Nair</td><td>WhatsApp</td><td>Scheduled</td><td>2026-06-29</td></tr>
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default FollowUpsPage
