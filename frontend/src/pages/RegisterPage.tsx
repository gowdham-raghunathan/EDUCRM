import { useState } from 'react'
import { Alert, Button, Card, Col, Container, Form, Row } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom'
import api from '../services/api'

function RegisterPage() {
  const [form, setForm] = useState({ username: '', email: '', full_name: '', password: '', role: 'counselor' })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleChange = (event: React.ChangeEvent<any>) => {
    setForm({ ...form, [event.target.name]: event.target.value })
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    try {
      await api.post('/api/auth/register', form)
      setMessage('Registration successful. You can sign in now.')
      setTimeout(() => navigate('/login'), 800)
    } catch {
      setError('Registration failed. Please try another username.')
    }
  }

  return (
    <Container fluid className="login-page">
      <Row className="g-0 min-vh-100">
        <Col lg={7} className="login-hero d-none d-lg-flex">
          <div className="hero-content">
            <p className="eyebrow">EduCRM</p>
            <h1>Grow your admissions team securely.</h1>
            <p className="hero-text">Create accounts for counselors and managers and keep lead operations organized.</p>
          </div>
        </Col>
        <Col lg={5} className="d-flex align-items-center justify-content-center bg-white">
          <Card className="login-card border-0">
            <Card.Body className="p-4 p-md-5">
              <div className="text-center mb-4">
                <h2 className="fw-bold mb-2">Create an account</h2>
                <p className="text-muted mb-0">Register a new admissions user.</p>
              </div>
              {message ? <Alert variant="success">{message}</Alert> : null}
              {error ? <Alert variant="danger">{error}</Alert> : null}
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Full name</Form.Label>
                  <Form.Control name="full_name" value={form.full_name} onChange={handleChange} required />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Username</Form.Label>
                  <Form.Control name="username" value={form.username} onChange={handleChange} required />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control type="email" name="email" value={form.email} onChange={handleChange} required />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Password</Form.Label>
                  <Form.Control type="password" name="password" value={form.password} onChange={handleChange} required />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Role</Form.Label>
                  <Form.Select name="role" value={form.role} onChange={handleChange}>
                    <option value="counselor">Counselor</option>
                    <option value="manager">Manager</option>
                    <option value="admin">Admin</option>
                  </Form.Select>
                </Form.Group>
                <Button variant="primary" type="submit" className="w-100 py-2">Register</Button>
              </Form>
              <div className="text-center mt-3">
                <Link to="/login" className="text-decoration-none">Already have an account? Sign in</Link>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default RegisterPage
