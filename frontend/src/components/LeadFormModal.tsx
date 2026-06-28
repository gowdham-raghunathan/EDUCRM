import { useEffect, useState } from 'react'
import { Alert, Button, Form, Modal } from 'react-bootstrap'
import api from '../services/api'

interface LeadFormModalProps {
  show: boolean
  onHide: () => void
  lead?: any
  onSaved: () => void
}

const emptyForm = {
  lead_id: '',
  student_name: '',
  mobile_number: '',
  email: '',
  course_interested: '',
  lead_status: 'New',
  admission_probability: 0,
  remarks: '',
}

function LeadFormModal({ show, onHide, lead, onSaved }: LeadFormModalProps) {
  const [form, setForm] = useState(emptyForm)
  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    if (lead) {
      setForm({ ...emptyForm, ...lead })
    } else {
      setForm(emptyForm)
    }
  }, [lead, show])

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const value = event.target.name === 'admission_probability' ? Number(event.target.value) : event.target.value
    setForm({ ...form, [event.target.name]: value })
    setErrors((current) => ({ ...current, [event.target.name]: '' }))
  }

  const validate = () => {
    const nextErrors: Record<string, string> = {}
    if (!form.lead_id.trim()) nextErrors.lead_id = 'Lead ID is required.'
    if (!form.student_name.trim()) nextErrors.student_name = 'Student name is required.'
    if (!form.mobile_number.trim()) nextErrors.mobile_number = 'Mobile number is required.'
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) && form.email) nextErrors.email = 'Enter a valid email address.'
    setErrors(nextErrors)
    return Object.keys(nextErrors).length === 0
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!validate()) return

    try {
      if (lead) {
        await api.put(`/api/leads/${lead.id}`, form)
      } else {
        await api.post('/api/leads', form)
      }
      onSaved()
      onHide()
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>{lead ? 'Edit Lead' : 'Create Lead'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={handleSubmit}>
          {Object.keys(errors).length > 0 ? <Alert variant="danger">Please fix the highlighted fields before saving.</Alert> : null}
          <Form.Group className="mb-3">
            <Form.Label>Lead ID</Form.Label>
            <Form.Control name="lead_id" value={form.lead_id} onChange={handleChange} isInvalid={!!errors.lead_id} />
            <Form.Control.Feedback type="invalid">{errors.lead_id}</Form.Control.Feedback>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Student Name</Form.Label>
            <Form.Control name="student_name" value={form.student_name} onChange={handleChange} isInvalid={!!errors.student_name} />
            <Form.Control.Feedback type="invalid">{errors.student_name}</Form.Control.Feedback>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Mobile Number</Form.Label>
            <Form.Control name="mobile_number" value={form.mobile_number} onChange={handleChange} isInvalid={!!errors.mobile_number} />
            <Form.Control.Feedback type="invalid">{errors.mobile_number}</Form.Control.Feedback>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" name="email" value={form.email} onChange={handleChange} isInvalid={!!errors.email} />
            <Form.Control.Feedback type="invalid">{errors.email}</Form.Control.Feedback>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Course Interested</Form.Label>
            <Form.Control name="course_interested" value={form.course_interested} onChange={handleChange} />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Status</Form.Label>
            <Form.Select name="lead_status" value={form.lead_status} onChange={handleChange}>
              <option value="New">New</option>
              <option value="Contacted">Contacted</option>
              <option value="Interested">Interested</option>
              <option value="Follow-up">Follow-up</option>
              <option value="Application Submitted">Application Submitted</option>
              <option value="Admission Confirmed">Admission Confirmed</option>
            </Form.Select>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Admission Probability</Form.Label>
            <Form.Control type="number" name="admission_probability" value={form.admission_probability} onChange={handleChange} />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Remarks</Form.Label>
            <Form.Control as="textarea" rows={3} name="remarks" value={form.remarks} onChange={handleChange} />
          </Form.Group>
          <div className="d-flex justify-content-end gap-2">
            <Button variant="secondary" onClick={onHide}>Cancel</Button>
            <Button variant="primary" type="submit">Save</Button>
          </div>
        </Form>
      </Modal.Body>
    </Modal>
  )
}

export default LeadFormModal
