import { Button, Card, Form, ListGroup } from 'react-bootstrap'

function CTISoftphoneWidget() {
  return (
    <Card className="softphone-widget shadow-sm border-0">
      <Card.Body>
        <div className="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h6 className="mb-1">CTI Softphone</h6>
            <small className="text-muted">Incoming call preview</small>
          </div>
          <span className="badge bg-success">Available</span>
        </div>

        <div className="mb-3">
          <div className="fw-bold">Aarav R.</div>
          <div className="text-muted">+91 98765 43210</div>
        </div>

        <div className="mb-3">
          <Form.Control className="text-center fw-semibold" value="9876543210" readOnly />
        </div>

        <div className="d-flex flex-wrap gap-2 mb-3">
          <Button variant="success" size="sm">Answer</Button>
          <Button variant="danger" size="sm">Reject</Button>
          <Button variant="warning" size="sm">Hold</Button>
        </div>

        <ListGroup variant="flush" className="small">
          <ListGroup.Item className="px-0">Mute</ListGroup.Item>
          <ListGroup.Item className="px-0">Transfer</ListGroup.Item>
          <ListGroup.Item className="px-0">Conference</ListGroup.Item>
        </ListGroup>
      </Card.Body>
    </Card>
  )
}

export default CTISoftphoneWidget
