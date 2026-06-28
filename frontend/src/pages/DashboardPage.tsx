import { useEffect, useState } from 'react'
import {
  AreaChart, Area, PieChart, Pie, Cell,
  XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts'
import api from '../services/api'

const FUNNEL_COLORS = ['#3b82f6', '#6366f1', '#f59e0b', '#10b981', '#14b8a6', '#8b5cf6']
const PIE_COLORS    = ['#3b82f6', '#6366f1', '#f59e0b', '#10b981', '#ef4444', '#14b8a6', '#f97316']

const fmt = (n: number) => n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(n)

function StatCard({ icon, iconBg, label, value, change, changeDir }: {
  icon: string; iconBg: string; label: string
  value: string | number; change: string; changeDir: 'up' | 'down' | 'neutral'
}) {
  return (
    <div className="stat-card">
      <div className="sc-icon" style={{ background: iconBg }}>
        <i className={`bi ${icon}`} style={{ color: '#fff' }}></i>
      </div>
      <div className="sc-value">{value}</div>
      <div className="sc-label">{label}</div>
      <div className={`sc-change ${changeDir}`}>
        {changeDir === 'up' && '↑ '}{changeDir === 'down' && '↓ '}{change} vs last month
      </div>
    </div>
  )
}

export default function DashboardPage() {
  const [metrics, setMetrics]     = useState<any>({})
  const [analytics, setAnalytics] = useState<any>({})
  const [trend, setTrend]         = useState<any>({})
  const [loading, setLoading]     = useState(true)
  const [period, setPeriod]       = useState('This Month')

  useEffect(() => {
    setLoading(true)
    Promise.all([
      api.get('/api/dashboard'),
      api.get('/api/dashboard/analytics'),
      api.get('/api/dashboard/monthly-trend'),
    ]).then(([m, a, t]) => {
      setMetrics(m.data)
      setAnalytics(a.data)
      setTrend(t.data)
    }).finally(() => setLoading(false))
  }, [])

  const funnel: { stage: string; count: number }[] = analytics.funnel || []
  const maxFunnel = funnel.reduce((m, r) => Math.max(m, r.count), 1)
  const sourceBreakdown = analytics.source_breakdown || {}
  const pieData = Object.entries(sourceBreakdown).map(([name, value]) => ({ name, value: Number(value) }))
  const monthly: { month: string; leads: number; admissions: number }[] = trend.monthly || []

  const statCards = [
    { icon: 'bi-people-fill',       iconBg: '#3b82f6', label: 'Total Leads',         value: fmt(metrics.total_leads || 0),            change: '+12%', changeDir: 'up'      },
    { icon: 'bi-person-plus-fill',  iconBg: '#10b981', label: 'New Leads',            value: fmt(metrics.new_leads || 0),              change: '+24%', changeDir: 'up'      },
    { icon: 'bi-star-fill',         iconBg: '#f59e0b', label: 'Interested',           value: fmt(metrics.interested_leads || 0),       change: '+8%',  changeDir: 'up'      },
    { icon: 'bi-file-earmark-text', iconBg: '#6366f1', label: 'Applications',         value: fmt(metrics.applications_submitted || 0), change: '-3%',  changeDir: 'down'    },
    { icon: 'bi-patch-check-fill',  iconBg: '#14b8a6', label: 'Confirmed Admissions', value: fmt(metrics.confirmed_admissions || 0),   change: '+18%', changeDir: 'up'      },
    { icon: 'bi-telephone-fill',    iconBg: '#f97316', label: 'Calls Today',          value: fmt(trend.calls_today || 0),              change: '+15%', changeDir: 'up'      },
  ] as const

  const acYear = `Academic Year ${new Date().getFullYear()}-${String(new Date().getFullYear() + 1).slice(2)}`

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 20 }}>
        <div>
          <h4 style={{ fontWeight: 800, margin: 0, color: '#0f172a' }}>Admission Dashboard</h4>
          <p style={{ margin: 0, color: '#64748b', fontSize: 13 }}>Overview of all admission activities — {acYear}</p>
        </div>
        <button
          onClick={() => { setLoading(true); api.get('/api/dashboard').then((r) => setMetrics(r.data)).finally(() => setLoading(false)) }}
          style={{ background: '#3b82f6', border: 'none', color: '#fff', borderRadius: 8, padding: '8px 16px', fontWeight: 600, fontSize: 13, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 6 }}
        >
          <i className="bi bi-arrow-clockwise"></i> Refresh
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: 12, marginBottom: 20 }}>
        {statCards.map((c) => <StatCard key={c.label} {...c} />)}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr 1.4fr', gap: 14, marginBottom: 14 }}>
        {/* Admission Funnel */}
        <div className="section-card">
          <div className="sc-header">
            <h6>Admission Funnel</h6>
            <select value={period} onChange={(e) => setPeriod(e.target.value)}
              style={{ fontSize: 12, border: '1px solid #e2e8f0', borderRadius: 6, padding: '3px 8px', background: '#f8fafc', cursor: 'pointer' }}>
              {['This Month', 'Last Month', 'This Year'].map((p) => <option key={p}>{p}</option>)}
            </select>
          </div>
          {loading ? (
            <div style={{ textAlign: 'center', color: '#94a3b8', padding: '40px 0' }}>Loading…</div>
          ) : funnel.length === 0 ? (
            <div style={{ textAlign: 'center', color: '#94a3b8', padding: '40px 0' }}>No data yet</div>
          ) : funnel.map((row, i) => {
            const pct = maxFunnel > 0 ? Math.round((row.count / maxFunnel) * 100) : 0
            return (
              <div className="funnel-row" key={row.stage}>
                <div className="fr-label">
                  <span className="fr-name">{row.stage}</span>
                  <span className="fr-count">{row.count.toLocaleString()}</span>
                </div>
                <div className="fr-bar">
                  <div className="fr-fill" style={{ width: `${pct}%`, background: FUNNEL_COLORS[i % FUNNEL_COLORS.length] }} />
                </div>
              </div>
            )
          })}
        </div>

        {/* Lead Sources pie */}
        <div className="section-card">
          <div className="sc-header"><h6>Lead Sources</h6></div>
          {pieData.length === 0 ? (
            <div style={{ textAlign: 'center', color: '#94a3b8', padding: '40px 0' }}>No data yet</div>
          ) : (
            <>
              <ResponsiveContainer width="100%" height={160}>
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" innerRadius={45} outerRadius={72} dataKey="value" paddingAngle={2}>
                    {pieData.map((_, i) => <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 5, marginTop: 4 }}>
                {pieData.slice(0, 5).map((d, i) => (
                  <div key={d.name} style={{ display: 'flex', alignItems: 'center', gap: 7, fontSize: 11 }}>
                    <span style={{ width: 10, height: 10, borderRadius: 3, background: PIE_COLORS[i % PIE_COLORS.length], flexShrink: 0 }}></span>
                    <span style={{ color: '#475569', flex: 1 }}>{d.name}</span>
                    <span style={{ fontWeight: 700, color: '#0f172a' }}>{d.value}</span>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>

        {/* Monthly trend */}
        <div className="section-card">
          <div className="sc-header"><h6>Monthly Admissions</h6></div>
          {monthly.every((m) => m.leads === 0 && m.admissions === 0) ? (
            <div style={{ textAlign: 'center', color: '#94a3b8', padding: '40px 0' }}>No data yet</div>
          ) : (
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={monthly} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
                <defs>
                  <linearGradient id="gLeads" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#3b82f6" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gAdmit" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#10b981" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="month" tick={{ fontSize: 10, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8, border: '1px solid #e2e8f0' }} />
                <Area type="monotone" dataKey="leads"      stroke="#3b82f6" strokeWidth={2} fill="url(#gLeads)" name="Leads"      dot={false} />
                <Area type="monotone" dataKey="admissions" stroke="#10b981" strokeWidth={2} fill="url(#gAdmit)" name="Admissions" dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 12 }}>
        {[
          { label: 'Total Revenue Collected', value: `₹${((metrics.total_payments || 0) / 100000).toFixed(1)}L`, icon: 'bi-cash-stack',        color: '#10b981' },
          { label: 'Pending Follow-ups',       value: metrics.pending_follow_ups || 0,                           icon: 'bi-calendar-x-fill',   color: '#f59e0b' },
          { label: 'Open Support Tickets',     value: metrics.open_tickets || 0,                                 icon: 'bi-ticket-perforated', color: '#ef4444' },
          { label: 'Active Campaigns',         value: metrics.active_campaigns || 0,                             icon: 'bi-megaphone-fill',    color: '#6366f1' },
        ].map((s) => (
          <div key={s.label} className="section-card" style={{ display: 'flex', alignItems: 'center', gap: 14, padding: '14px 16px' }}>
            <div style={{ width: 40, height: 40, borderRadius: 10, background: `${s.color}18`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <i className={`bi ${s.icon}`} style={{ color: s.color, fontSize: 18 }}></i>
            </div>
            <div>
              <div style={{ fontSize: 20, fontWeight: 800, color: '#0f172a', lineHeight: 1 }}>{s.value}</div>
              <div style={{ fontSize: 11, color: '#64748b', marginTop: 3 }}>{s.label}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
