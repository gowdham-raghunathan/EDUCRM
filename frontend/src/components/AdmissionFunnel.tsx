import { Card, Col, ProgressBar, Row } from 'react-bootstrap'

const stages = [
  { title: 'New Leads', count: 184, percent: 100 },
  { title: 'Contacted', count: 126, percent: 68 },
  { title: 'Interested', count: 94, percent: 51 },
  { title: 'Follow-up', count: 72, percent: 39 },
  { title: 'Application Submitted', count: 48, percent: 26 },
  { title: 'Admission Confirmed', count: 24, percent: 13 },
]

function AdmissionFunnel() {
  return (
    <Card className="h-100 shadow-sm border-0">
      <Card.Body>
        <div className="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h5 className="mb-1">Admission Funnel</h5>
            <p className="text-muted small mb-0">Conversion trend across admission stages</p>
          </div>
        </div>
        <Row className="g-3">
          {stages.map((stage) => (
            <Col xs={12} key={stage.title}>
              <div className="d-flex justify-content-between mb-1">
                <span>{stage.title}</span>
                <strong>{stage.count}</strong>
              </div>
              <ProgressBar now={stage.percent} variant="primary" />
            </Col>
          ))}
        </Row>
      </Card.Body>
    </Card>
  )
}

export default AdmissionFunnel
