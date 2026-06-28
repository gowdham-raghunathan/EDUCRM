import { useEffect, useState } from 'react'
import { Badge, Button, Card, Col, Form, Modal, Nav, Row, Table } from 'react-bootstrap'
import { getUsers, createUser, deleteUser, getTeams, createTeam, addTeamMember } from '../services/api'

const ROLES = ['admin', 'manager', 'counselor', 'agent', 'publisher']

function roleBadge(role: string) {
  const map: Record<string, string> = { admin: 'danger', manager: 'warning', counselor: 'primary', agent: 'info', publisher: 'secondary' }
  return <Badge bg={map[role] || 'secondary'}>{role}</Badge>
}

export default function UserManagementPage() {
  const [tab, setTab] = useState('users')
  const [users, setUsers] = useState<any[]>([])
  const [teams, setTeams] = useState<any[]>([])
  const [showUserModal, setShowUserModal] = useState(false)
  const [showTeamModal, setShowTeamModal] = useState(false)
  const [showMemberModal, setShowMemberModal] = useState(false)
  const [selectedTeam, setSelectedTeam] = useState<any>(null)
  const [memberUserId, setMemberUserId] = useState('')
  const [userForm, setUserForm] = useState({ username: '', email: '', full_name: '', role: 'counselor', password: '' })
  const [teamForm, setTeamForm] = useState({ name: '', description: '' })

  const load = async () => {
    const [ur, tr] = await Promise.all([getUsers(), getTeams()])
    setUsers(ur.data)
    setTeams(tr.data)
  }

  useEffect(() => { load() }, [])

  const saveUser = async () => { await createUser(userForm); setShowUserModal(false); load() }
  const removeUser = async (id: number) => { if (confirm('Delete this user?')) { await deleteUser(id); load() } }
  const saveTeam = async () => { await createTeam(teamForm); setShowTeamModal(false); load() }
  const addMember = async () => {
    await addTeamMember(selectedTeam.id, parseInt(memberUserId))
    setShowMemberModal(false)
    setMemberUserId('')
    load()
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">User Management</h4>
        <div className="d-flex gap-2">
          <Button size="sm" variant="outline-primary" onClick={() => setShowTeamModal(true)}>+ Team</Button>
          <Button size="sm" onClick={() => setShowUserModal(true)}>+ User</Button>
        </div>
      </div>

      <Nav variant="tabs" className="mb-3" activeKey={tab} onSelect={(k) => setTab(k || 'users')}>
        <Nav.Item><Nav.Link eventKey="users">Users ({users.length})</Nav.Link></Nav.Item>
        <Nav.Item><Nav.Link eventKey="teams">Teams ({teams.length})</Nav.Link></Nav.Item>
      </Nav>

      {tab === 'users' && (
        <Card>
          <Card.Body className="p-0">
            <Table hover responsive className="mb-0">
              <thead className="table-light">
                <tr><th>Name</th><th>Username</th><th>Email</th><th>Role</th><th>Actions</th></tr>
              </thead>
              <tbody>
                {users.length === 0 && <tr><td colSpan={5} className="text-center text-muted py-4">No users found</td></tr>}
                {users.map((u) => (
                  <tr key={u.id}>
                    <td>{u.full_name}</td>
                    <td>{u.username}</td>
                    <td>{u.email}</td>
                    <td>{roleBadge(u.role)}</td>
                    <td><Button size="sm" variant="outline-danger" onClick={() => removeUser(u.id)}>Remove</Button></td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Card.Body>
        </Card>
      )}

      {tab === 'teams' && (
        <Row className="g-3">
          {teams.length === 0 && <Col><p className="text-muted">No teams yet</p></Col>}
          {teams.map((t) => (
            <Col md={4} key={t.id}>
              <Card>
                <Card.Body>
                  <div className="fw-semibold mb-1">{t.name}</div>
                  <div className="text-muted small mb-2">{t.description || 'No description'}</div>
                  <div className="small mb-2">{t.members?.length || 0} members</div>
                  <Button size="sm" variant="outline-primary" onClick={() => { setSelectedTeam(t); setShowMemberModal(true) }}>+ Add Member</Button>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      )}

      <Modal show={showUserModal} onHide={() => setShowUserModal(false)}>
        <Modal.Header closeButton><Modal.Title>Add User</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-2"><Form.Label>Full Name</Form.Label><Form.Control value={userForm.full_name} onChange={(e) => setUserForm({ ...userForm, full_name: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Username</Form.Label><Form.Control value={userForm.username} onChange={(e) => setUserForm({ ...userForm, username: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Email</Form.Label><Form.Control type="email" value={userForm.email} onChange={(e) => setUserForm({ ...userForm, email: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Password</Form.Label><Form.Control type="password" value={userForm.password} onChange={(e) => setUserForm({ ...userForm, password: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Role</Form.Label>
              <Form.Select value={userForm.role} onChange={(e) => setUserForm({ ...userForm, role: e.target.value })}>
                {ROLES.map((r) => <option key={r}>{r}</option>)}
              </Form.Select>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowUserModal(false)}>Cancel</Button>
          <Button onClick={saveUser}>Add User</Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showTeamModal} onHide={() => setShowTeamModal(false)}>
        <Modal.Header closeButton><Modal.Title>Create Team</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-2"><Form.Label>Team Name</Form.Label><Form.Control value={teamForm.name} onChange={(e) => setTeamForm({ ...teamForm, name: e.target.value })} /></Form.Group>
            <Form.Group className="mb-2"><Form.Label>Description</Form.Label><Form.Control as="textarea" value={teamForm.description} onChange={(e) => setTeamForm({ ...teamForm, description: e.target.value })} /></Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowTeamModal(false)}>Cancel</Button>
          <Button onClick={saveTeam}>Create Team</Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showMemberModal} onHide={() => setShowMemberModal(false)}>
        <Modal.Header closeButton><Modal.Title>Add Member to {selectedTeam?.name}</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form.Label>Select User</Form.Label>
          <Form.Select value={memberUserId} onChange={(e) => setMemberUserId(e.target.value)}>
            <option value="">-- Select --</option>
            {users.map((u) => <option key={u.id} value={u.id}>{u.full_name} ({u.username})</option>)}
          </Form.Select>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowMemberModal(false)}>Cancel</Button>
          <Button onClick={addMember} disabled={!memberUserId}>Add Member</Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
