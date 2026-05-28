import { useEffect } from 'react'
import { useStore } from '../store/useStore'
import { hubAPI } from '../services/api'
import AgentHubPanel from '../components/AgentHubPanel'
import ResearchAreaPanel from '../components/ResearchAreaPanel'
import ActivityLog from '../components/ActivityLog'

export default function CyberHubDashboard() {
  const user = useStore((s) => s.user)
  const setAgents = useStore((s) => s.setAgents)
  const addActivity = useStore((s) => s.addActivity)

  // Load all agents when dashboard mounts
  useEffect(() => {
    const loadAgents = async () => {
      try {
        const { data } = await hubAPI.getAllAgents()
        setAgents(data)
      } catch (e) {
        console.error('Failed to load agents', e)
      }
    }
    loadAgents()
    addActivity('Dashboard initialized. Welcome to Cyber Hub.')

    // Poll agents every 5 seconds to reflect spawning/releasing
    const interval = setInterval(loadAgents, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Bar */}
      <header className="flex items-center justify-between px-6 py-3 border-b border-cyber-border">
        <div className="flex items-center gap-3">
          <span className="font-display text-cyber-accent text-lg font-bold tracking-widest">
            CYBER HUB
          </span>
          <span className="text-cyber-muted text-xs">v0.1.0</span>
        </div>

        {/* User identity */}
        <div className="flex items-center gap-3 text-xs">
          <span className="w-2 h-2 rounded-full bg-cyber-green animate-pulse-slow" />
          <span className="text-cyber-muted">Logged in as</span>
          <span className="text-cyber-accent font-bold">{user?.name}</span>
        </div>
      </header>

      {/* Main Layout: 2 panels + sidebar */}
      <div className="flex flex-1 gap-0 overflow-hidden">

        {/* Left: Agent Hub */}
        <div className="w-72 border-r border-cyber-border overflow-y-auto">
          <AgentHubPanel />
        </div>

        {/* Center: Research Area */}
        <div className="flex-1 overflow-y-auto">
          <ResearchAreaPanel />
        </div>

        {/* Right: Activity Log */}
        <div className="w-64 border-l border-cyber-border overflow-y-auto">
          <ActivityLog />
        </div>
      </div>
    </div>
  )
}
