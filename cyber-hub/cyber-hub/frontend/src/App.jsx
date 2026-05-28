import { useState } from 'react'
import LandingPage from './pages/LandingPage'
import CyberHubDashboard from './pages/CyberHubDashboard'
import './index.css'

export default function App() {
  const [view, setView] = useState('landing') // 'landing' | 'dashboard'

  return (
    <div className="min-h-screen bg-cyber-bg font-mono text-cyber-text">
      {view === 'landing' ? (
        <LandingPage onEnter={() => setView('dashboard')} />
      ) : (
        <CyberHubDashboard />
      )}
    </div>
  )
}
