import { useEffect, useState } from 'react'
import api from '../services/api'

const KEYS = [
  { main: '1', sub: '' },     { main: '2', sub: 'ABC' },  { main: '3', sub: 'DEF' },
  { main: '4', sub: 'GHI' },  { main: '5', sub: 'JKL' },  { main: '6', sub: 'MNO' },
  { main: '7', sub: 'PQRS' }, { main: '8', sub: 'TUV' },  { main: '9', sub: 'WXYZ' },
  { main: '*', sub: '' },     { main: '0', sub: '+' },     { main: '#', sub: '' },
]

export default function CTISoftphone() {
  const [number, setNumber] = useState('')
  const [calling, setCalling] = useState(false)
  const [activeSid, setActiveSid] = useState<string | null>(null)
  const [stats, setStats] = useState({ calls_today: 0, duration_today: 0, active: 0 })

  const loadStats = async () => {
    try {
      const [trendRes, activeRes] = await Promise.all([
        api.get('/api/dashboard/monthly-trend'),
        api.get('/api/cti/active-calls'),
      ])
      setStats((s) => ({
        ...s,
        calls_today: trendRes.data.calls_today ?? 0,
        active: activeRes.data.length,
      }))
    } catch { /* ignore */ }
  }

  useEffect(() => {
    loadStats()
    const t = setInterval(loadStats, 15000)
    return () => clearInterval(t)
  }, [])

  const press = (k: string) => setNumber((n) => (n.length < 15 ? n + k : n))
  const backspace = () => setNumber((n) => n.slice(0, -1))

  const call = async () => {
    if (!number || calling) return
    setCalling(true)
    try {
      const res = await api.post('/api/cti/call', { to: number })
      setActiveSid(res.data.call_sid)
      loadStats()
    } catch (e: any) {
      alert(e?.response?.data?.detail || 'Call failed')
    } finally {
      setCalling(false)
    }
  }

  const hangup = async () => {
    if (!activeSid) return
    try {
      await api.post(`/api/cti/calls/${activeSid}/end`)
      setActiveSid(null)
      loadStats()
    } catch { /* ignore */ }
  }

  const formatDuration = (secs: number) => {
    const h = Math.floor(secs / 3600)
    const m = Math.floor((secs % 3600) / 60)
    return h > 0 ? `${h}h ${m}m` : `${m}m`
  }

  return (
    <div className="cti-panel">
      <div className="cti-panel-header">
        <i className="bi bi-telephone-fill" style={{ color: '#60a5fa', fontSize: 14 }}></i>
        <span>CTI Softphone</span>
        <span className="status-pill">Available</span>
      </div>

      {/* Display */}
      <div className="cti-display">
        <input
          value={number}
          onChange={(e) => setNumber(e.target.value.replace(/[^0-9+*#]/g, '').slice(0, 15))}
          placeholder="Enter number..."
        />
        {number && (
          <button
            onClick={backspace}
            style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', fontSize: 16, padding: '0 0 0 8px' }}
          >⌫</button>
        )}
      </div>

      {/* Keypad */}
      <div className="cti-keypad">
        {KEYS.map((k) => (
          <button key={k.main} className="cti-key" onClick={() => press(k.main)}>
            <span className="key-main">{k.main}</span>
            <span className="key-sub">{k.sub}</span>
          </button>
        ))}
      </div>

      {/* Call / Hangup button */}
      {activeSid ? (
        <button className="cti-call-btn calling" onClick={hangup}>
          <i className="bi bi-telephone-x-fill"></i> End Call
        </button>
      ) : (
        <button className="cti-call-btn" onClick={call} disabled={!number || calling}>
          <i className="bi bi-telephone-fill"></i>
          {calling ? 'Connecting…' : 'Call'}
        </button>
      )}

      {/* Today's Stats */}
      <div className="cti-stats">
        <div className="stat-label">TODAY'S STATS</div>
        <div className="cti-stat-row">
          <span className="sk">Calls Made</span>
          <span className="sv">{stats.calls_today}</span>
        </div>
        <div className="cti-stat-row">
          <span className="sk">Active Now</span>
          <span className={`sv ${stats.active > 0 ? 'green' : ''}`}>{stats.active}</span>
        </div>
      </div>
    </div>
  )
}
