import { Button, Card, Col, Form, ListGroup, Row } from 'react-bootstrap'

function WhatsAppPage() {
  return (
    <div>
      <h3 className="fw-bold mb-1">WhatsApp Communication</h3>
      <p className="text-muted mb-4">Send templates, brochures, fee structures, and chat with prospects.</p>
      <Row className="g-4">
        <Col lg={7}>
          <Card className="border-0">
            <Card.Body>
              <h5 className="mb-3">Conversation History</h5>
              <ListGroup variant="flush">
                <ListGroup.Item><strong>Student:</strong> Hello, I want fee structure details.</ListGroup.Item>
                <ListGroup.Item><strong>Agent:</strong> Sure, I have shared the brochure.</ListGroup.Item>
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>
        <Col lg={5}>
          <Card className="border-0">
            <Card.Body>
              <h5 className="mb-3">Message Composer</h5>
              <Form>
                <Form.Group className="mb-3"><Form.Label>Template</Form.Label><Form.Select><option>Admission Follow-up</option><option>Fee Structure</option><option>Brochure</option></Form.Select></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Message</Form.Label><Form.Control as="textarea" rows={4} /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Attachment</Form.Label><Form.Control type="file" /></Form.Group>
                <div className="d-flex flex-wrap gap-2">
                  <Button variant="primary">Send WhatsApp</Button>
                  <Button variant="outline-secondary">Send Brochure</Button>
                  <Button variant="outline-secondary">Send Fee Structure</Button>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default WhatsAppPage
