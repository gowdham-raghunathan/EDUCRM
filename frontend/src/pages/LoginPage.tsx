import { useState } from 'react'
import { Alert, Button, Card, Col, Container, Form, Row } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom'
import api from '../services/api'

function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    try {
      const response = await api.post('/api/auth/login', { username, password })
      localStorage.setItem('access_token', response.data.access_token)
      localStorage.setItem('user_role', 'admin')
      navigate('/')
    } catch {
      setError('Unable to sign in. Please check your credentials.')
    }
  }

  return (
    <Container fluid className="login-page">
      <Row className="g-0 min-vh-100">
        <Col lg={7} className="login-hero d-none d-lg-flex">
          <div className="hero-content">
            <p className="eyebrow">EduCRM</p>
            <h1>Admissions operations, unified.</h1>
            <p className="hero-text">Secure student engagement, lead routing, CTI, and follow-up automation in one platform.</p>
          </div>
        </Col>
        <Col lg={5} className="d-flex align-items-center justify-content-center bg-white">
          <Card className="login-card border-0">
            <Card.Body className="p-4 p-md-5">
              <div className="text-center mb-4">
                <h2 className="fw-bold mb-2">Welcome back</h2>
                <p className="text-muted mb-0">Sign in to manage admissions.</p>
              </div>
              {error ? <Alert variant="danger">{error}</Alert> : null}
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Username</Form.Label>
                  <Form.Control value={username} onChange={(event) => setUsername(event.target.value)} required />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Password</Form.Label>
                  <Form.Control type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
                </Form.Group>
                <Button variant="primary" type="submit" className="w-100 py-2">Sign in</Button>
              </Form>
              <div className="text-center mt-3">
                <Link to="/register" className="text-decoration-none">Create an account</Link>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default LoginPage
