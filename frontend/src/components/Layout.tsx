import { useEffect, useMemo, useRef, useState } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { setActiveModule } from '../store'
import CTISoftphone from './CTISoftphone'

const NAV = [
  {
    section: 'MAIN',
    items: [{ label: 'Dashboard', path: '/', icon: 'bi-speedometer2' }],
  },
  {
    section: 'LEAD MANAGEMENT',
    items: [
      { label: 'Admission Leads', path: '/leads', icon: 'bi-people-fill', badge: 'leads' },
      { label: 'Applicants', path: '/applications', icon: 'bi-file-earmark-text-fill' },
      { label: 'Follow-ups', path: '/follow-ups', icon: 'bi-calendar-check-fill', badge: 'followups' },
    ],
  },
  {
    section: 'PAYMENTS',
    items: [
      { label: 'Fee & Payments', path: '/payments', icon: 'bi-cash-coin' },
    ],
  },
  {
    section: 'COMMUNICATION',
    items: [
      { label: 'CTI Call Center', path: '/cti', icon: 'bi-telephone-fill' },
      { label: 'Call History', path: '/call-history', icon: 'bi-clock-history' },
      { label: 'WhatsApp', path: '/whatsapp', icon: 'bi-whatsapp' },
      { label: 'Email Campaigns', path: '/email-campaigns', icon: 'bi-envelope-fill' },
      { label: 'SMS', path: '/sms', icon: 'bi-chat-dots-fill' },
    ],
  },
  {
    section: 'AUTOMATION',
    items: [
      { label: 'Automations', path: '/automations', icon: 'bi-gear-wide-connected' },
      { label: 'Campaigns', path: '/campaigns', icon: 'bi-megaphone-fill' },
    ],
  },
  {
    section: 'SUPPORT',
    items: [
      { label: 'Query Manager', path: '/queries', icon: 'bi-question-circle-fill' },
    ],
  },
  {
    section: 'ANALYTICS',
    items: [
      { label: 'Reports', path: '/reports', icon: 'bi-bar-chart-fill' },
    ],
  },
  {
    section: 'ADMINISTRATION',
    items: [
      { label: 'User Management', path: '/user-management', icon: 'bi-shield-lock-fill' },
      { label: 'Settings', path: '/settings', icon: 'bi-sliders' },
    ],
  },
]

const allItems = NAV.flatMap((s) => s.items)

export default function Layout() {
  const location = useLocation()
  const dispatch = useDispatch()
  const role = useMemo(() => localStorage.getItem('user_role') || 'counselor', [])
  const username = useMemo(() => localStorage.getItem('username') || 'Admin', [])
  const initials = username.slice(0, 2).toUpperCase()
  const [showUserMenu, setShowUserMenu] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const item = allItems.find((i) => i.path === location.pathname)
    dispatch(setActiveModule(item?.label ?? 'Dashboard'))
  }, [dispatch, location.pathname])

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) setShowUserMenu(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div className="crm-shell">
      {/* ── Sidebar ── */}
      <aside className="crm-sidebar">
        <div className="sidebar-logo d-flex align-items-center gap-2">
          <div className="logo-mark">A</div>
          <div>
            <div className="logo-text">AdmissionCRM</div>
            <div className="logo-sub">Lead Management System</div>
          </div>
        </div>

        <div className="agent-status-bar d-flex align-items-center gap-2">
          <div className="status-dot"></div>
          <div>
            <div className="d-block"><strong>Agent Status</strong></div>
            <span>Available</span>
          </div>
        </div>

        {NAV.map((section) => (
          <div key={section.section}>
            <div className="sidebar-section-label">{section.section}</div>
            {section.items.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) => `sidebar-nav-item${isActive ? ' active' : ''}`}
              >
                <i className={`bi ${item.icon}`}></i>
                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>
        ))}
        <div style={{ height: 24 }} />
      </aside>

      {/* ── Body ── */}
      <div className="crm-body">
        {/* Top bar */}
        <header className="crm-topbar">
          <div className="search-wrap">
            <i className="bi bi-search search-icon"></i>
            <input placeholder="Search leads, students, courses..." />
          </div>

          <div className="topbar-right">
            <div className="icon-btn">
              <i className="bi bi-bell-fill"></i>
              <span className="notif-dot"></span>
            </div>
            <div className="icon-btn"><i className="bi bi-calendar3"></i></div>
            <div className="icon-btn"><i className="bi bi-chat-dots-fill"></i></div>

            <div style={{ position: 'relative' }} ref={menuRef}>
              <div className="user-avatar" onClick={() => setShowUserMenu((v) => !v)}>
                {initials}
              </div>
              {showUserMenu && (
                <div style={{
                  position: 'absolute', right: 0, top: '44px', background: '#fff',
                  border: '1px solid #e2e8f0', borderRadius: '10px', minWidth: '160px',
                  boxShadow: '0 8px 24px rgba(15,23,42,0.12)', zIndex: 999, overflow: 'hidden',
                }}>
                  <div style={{ padding: '10px 14px 6px', borderBottom: '1px solid #f1f5f9' }}>
                    <div style={{ fontWeight: 700, fontSize: 13 }}>{username}</div>
                    <div style={{ fontSize: 11, color: '#64748b' }}>{role}</div>
                  </div>
                  <div style={{ padding: '4px 0' }}>
                    <NavLink to="/settings" style={{ display: 'block', padding: '8px 14px', fontSize: 13, color: '#374151', textDecoration: 'none' }}>Settings</NavLink>
                    <div
                      style={{ padding: '8px 14px', fontSize: 13, color: '#ef4444', cursor: 'pointer' }}
                      onClick={() => { localStorage.clear(); window.location.href = '/login' }}
                    >Logout</div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Content + CTI panel */}
        <div className="crm-content-row">
          <main className="crm-main">
            <Outlet />
          </main>
          <CTISoftphone />
        </div>
      </div>
    </div>
  )
}
