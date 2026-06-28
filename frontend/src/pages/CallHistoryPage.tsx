import { Card, Table } from 'react-bootstrap'

function CallHistoryPage() {
  return (
    <div>
      <h3 className="fw-bold mb-1">Call History</h3>
      <p className="text-muted mb-4">Track inbound, outbound, and recorded calls end to end.</p>
      <Card className="border-0">
        <Card.Body>
          <Table responsive hover>
            <thead>
              <tr><th>Call Date</th><th>Call Type</th><th>Agent</th><th>Duration</th><th>Status</th><th>Recording</th></tr>
            </thead>
            <tbody>
              <tr><td>2026-06-27</td><td>Inbound</td><td>Neha</td><td>04:12</td><td>Answered</td><td><audio controls src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" /></td></tr>
              <tr><td>2026-06-26</td><td>Outbound</td><td>Ravi</td><td>03:07</td><td>Completed</td><td><audio controls src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3" /></td></tr>
            </tbody>
          </Table>
        </Card.Body>
      </Card>
    </div>
  )
}

export default CallHistoryPage
