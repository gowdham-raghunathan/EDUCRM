import { Card, ListGroup } from 'react-bootstrap'

const activities = [
  { title: 'Lead Created', time: '09:15 AM', icon: '📝', color: 'primary' },
  { title: 'Call Made', time: '10:30 AM', icon: '📞', color: 'success' },
  { title: 'WhatsApp Sent', time: '11:05 AM', icon: '💬', color: 'info' },
  { title: 'Follow-up Scheduled', time: '01:20 PM', icon: '📅', color: 'warning' },
  { title: 'Application Submitted', time: '03:45 PM', icon: '📄', color: 'danger' },
]

function LeadTimeline() {
  return (
    <Card className="shadow-sm border-0">
      <Card.Body>
        <h5 className="mb-3">Lead Timeline</h5>
        <ListGroup variant="flush">
          {activities.map((activity) => (
            <ListGroup.Item key={activity.title} className="d-flex justify-content-between align-items-center px-0">
              <div className="d-flex align-items-center gap-2">
                <span className={`badge bg-${activity.color}`}>{activity.icon}</span>
                <div>
                  <div className="fw-semibold">{activity.title}</div>
                  <small className="text-muted">Student interaction logged</small>
                </div>
              </div>
              <small className="text-muted">{activity.time}</small>
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Card.Body>
    </Card>
  )
}

export default LeadTimeline
