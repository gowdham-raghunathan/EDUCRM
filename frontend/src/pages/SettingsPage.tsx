import { Card, Col, Form, Row, Button } from 'react-bootstrap'

export default function SettingsPage() {
  return (
    <div>
      <h4 className="mb-4">System Settings</h4>
      <Row className="g-4">
        <Col md={6}>
          <Card>
            <Card.Header className="fw-semibold">General</Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3"><Form.Label>Institution Name</Form.Label><Form.Control defaultValue="EduCRM Institute" /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Support Email</Form.Label><Form.Control type="email" defaultValue="support@educrm.local" /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Default Timezone</Form.Label>
                  <Form.Select defaultValue="Asia/Kolkata">
                    <option>Asia/Kolkata</option><option>UTC</option>
                  </Form.Select>
                </Form.Group>
                <Button size="sm">Save General</Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card>
            <Card.Header className="fw-semibold">Integrations</Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3"><Form.Label>WhatsApp Business API Key</Form.Label><Form.Control type="password" placeholder="Enter WABA key" /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>SMS Gateway API Key</Form.Label><Form.Control type="password" placeholder="Enter SMS gateway key" /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Email SMTP Host</Form.Label><Form.Control placeholder="smtp.gmail.com" /></Form.Group>
                <Button size="sm">Save Integrations</Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card>
            <Card.Header className="fw-semibold">Lead Scoring Thresholds</Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3"><Form.Label>Hot Lead Threshold</Form.Label><Form.Control type="number" defaultValue={70} /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Warm Lead Threshold</Form.Label><Form.Control type="number" defaultValue={40} /></Form.Group>
                <Button size="sm">Save Thresholds</Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card>
            <Card.Header className="fw-semibold">SLA Configuration</Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3"><Form.Label>Low Priority SLA (hours)</Form.Label><Form.Control type="number" defaultValue={72} /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Medium Priority SLA (hours)</Form.Label><Form.Control type="number" defaultValue={48} /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>High Priority SLA (hours)</Form.Label><Form.Control type="number" defaultValue={24} /></Form.Group>
                <Form.Group className="mb-3"><Form.Label>Urgent Priority SLA (hours)</Form.Label><Form.Control type="number" defaultValue={4} /></Form.Group>
                <Button size="sm">Save SLA</Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
