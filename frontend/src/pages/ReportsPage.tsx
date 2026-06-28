import { useEffect, useState } from 'react'
import { Button, Card, Col, Form, Row, Table } from 'react-bootstrap'
import { getDashboardSummary, runReport } from '../services/api'

const ENTITIES = ['leads', 'applications', 'payments', 'followups', 'tickets']

export default function ReportsPage() {
  const [summary, setSummary] = useState<any>({})
  const [entity, setEntity] = useState('leads')
  const [rows, setRows] = useState<any[]>([])
  const [cols, setCols] = useState<string[]>([])

  useEffect(() => { getDashboardSummary().then((r) => setSummary(r.data)) }, [])

  const run = async () => {
    const res = await runReport(entity)
    const data: any[] = res.data
    if (data.length > 0) {
      setCols(Object.keys(data[0]))
      setRows(data)
    } else {
      setCols([])
      setRows([])
    }
  }

  const renderBreakdown = (title: string, data: Record<string, number>) => (
    <Card className="mb-3">
      <Card.Header className="fw-semibold">{title}</Card.Header>
      <Card.Body className="p-0">
        <Table size="sm" className="mb-0">
          <tbody>
            {Object.entries(data || {}).map(([k, v]) => (
              <tr key={k}><td>{k}</td><td className="text-end fw-semibold">{v}</td></tr>
            ))}
            {Object.keys(data || {}).length === 0 && <tr><td className="text-muted p-2">No data</td></tr>}
          </tbody>
        </Table>
      </Card.Body>
    </Card>
  )

  return (
    <div>
      <h4 className="mb-3">Reports & Analytics</h4>

      <Row className="g-3 mb-4">
        <Col md={4}>{renderBreakdown('Lead Status Breakdown', summary.lead_status_breakdown)}</Col>
        <Col md={4}>{renderBreakdown('Lead Source Breakdown', summary.lead_source_breakdown)}</Col>
        <Col md={4}>
          <Card className="mb-3">
            <Card.Header className="fw-semibold">Revenue Summary</Card.Header>
            <Card.Body>
              <div className="d-flex justify-content-between"><span>Total Revenue</span><strong>₹{(summary.revenue?.total || 0).toLocaleString()}</strong></div>
              <div className="d-flex justify-content-between"><span>Pending</span><strong>₹{(summary.revenue?.pending || 0).toLocaleString()}</strong></div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Card>
        <Card.Header className="fw-semibold d-flex align-items-center gap-3">
          Run Custom Report
          <Form.Select size="sm" style={{ width: 160 }} value={entity} onChange={(e) => setEntity(e.target.value)}>
            {ENTITIES.map((e) => <option key={e}>{e}</option>)}
          </Form.Select>
          <Button size="sm" onClick={run}>Run</Button>
        </Card.Header>
        <Card.Body className="p-0">
          {rows.length === 0 ? (
            <p className="text-muted text-center py-4">Select an entity and click Run to generate a report.</p>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <Table hover size="sm" className="mb-0">
                <thead className="table-light">
                  <tr>{cols.map((c) => <th key={c}>{c}</th>)}</tr>
                </thead>
                <tbody>
                  {rows.map((row, i) => (
                    <tr key={i}>{cols.map((c) => <td key={c}>{row[c] !== null && row[c] !== undefined ? String(row[c]) : '—'}</td>)}</tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}
        </Card.Body>
      </Card>
    </div>
  )
}
