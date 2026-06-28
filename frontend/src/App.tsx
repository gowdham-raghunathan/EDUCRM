import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { Provider } from 'react-redux'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import RoleGuard from './components/RoleGuard'
import DashboardPage from './pages/DashboardPage'
import LeadsPage from './pages/LeadsPage'
import FollowUpsPage from './pages/FollowUpsPage'
import CallHistoryPage from './pages/CallHistoryPage'
import CTIPage from './pages/CTIPage'
import WhatsAppPage from './pages/WhatsAppPage'
import ApplicationsPage from './pages/ApplicationsPage'
import PaymentsPage from './pages/PaymentsPage'
import EmailCampaignsPage from './pages/EmailCampaignsPage'
import QueryManagerPage from './pages/QueryManagerPage'
import AutomationsPage from './pages/AutomationsPage'
import CampaignsPage from './pages/CampaignsPage'
import ReportsPage from './pages/ReportsPage'
import UserManagementPage from './pages/UserManagementPage'
import SettingsPage from './pages/SettingsPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import { store } from './store'
import './App.css'

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/leads" element={<LeadsPage />} />
              <Route path="/applications" element={<ApplicationsPage />} />
              <Route path="/follow-ups" element={<FollowUpsPage />} />
              <Route path="/payments" element={<PaymentsPage />} />
              <Route path="/whatsapp" element={<WhatsAppPage />} />
              <Route path="/email-campaigns" element={<EmailCampaignsPage />} />
              <Route path="/sms" element={<div className="page-placeholder p-4"><h5>SMS Manager</h5><p className="text-muted">Bulk SMS sending via the SMS page is handled through the WhatsApp & Communication hub. Use the API at /api/sms/send to send messages programmatically.</p></div>} />
              <Route path="/cti" element={<CTIPage />} />
              <Route path="/call-history" element={<CallHistoryPage />} />
              <Route path="/queries" element={<QueryManagerPage />} />
              <Route element={<RoleGuard allowedRoles={['manager', 'admin']} />}>
                <Route path="/automations" element={<AutomationsPage />} />
                <Route path="/campaigns" element={<CampaignsPage />} />
                <Route path="/reports" element={<ReportsPage />} />
              </Route>
              <Route element={<RoleGuard allowedRoles={['admin']} />}>
                <Route path="/user-management" element={<UserManagementPage />} />
                <Route path="/settings" element={<SettingsPage />} />
              </Route>
            </Route>
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  )
}

export default App
