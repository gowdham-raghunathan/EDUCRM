import { Navigate, Outlet } from 'react-router-dom'

interface RoleGuardProps {
  allowedRoles: string[]
}

function RoleGuard({ allowedRoles }: RoleGuardProps) {
  const role = localStorage.getItem('user_role') || 'counselor'
  return allowedRoles.includes(role) ? <Outlet /> : <Navigate to="/" replace />
}

export default RoleGuard
