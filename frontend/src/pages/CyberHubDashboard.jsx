import { useEffect } from 'react'

import { useStore } from '../store/useStore'
import { hubAPI } from '../services/api'

import SimulationWorld from '../components/simulation/SimulationWorld'
import ResearchAreaPanel from '../components/ResearchAreaPanel'
import ActivityLog from '../components/ActivityLog'

export default function CyberHubDashboard() {

  const user = useStore((s) => s.user)
  const setAgents = useStore((s) => s.setAgents)
  const addActivity = useStore((s) => s.addActivity)

  useEffect(() => {

    const loadAgents = async () => {
      try {
        const { data } = await hubAPI.getAllAgents()
        setAgents(data)
      } catch (e) {
        console.error(e)
      }
    }

    loadAgents()

    addActivity('Cyber Hub initialized.')

    const interval = setInterval(loadAgents, 5000)

    return () => clearInterval(interval)

  }, [])

  return (
    <div className="min-h-screen bg-[#050a0f] text-white overflow-hidden">

      {/* TopBar */}
      <header className="h-16 border-b border-cyan-500/20 flex items-center justify-between px-6">

        <div>
          <div className="text-cyan-400 font-black text-2xl tracking-[0.4em]">
            CYBER HUB
          </div>
        </div>

        <div className="text-sm text-cyan-200">
          Operator: {user?.name}
        </div>

      </header>

      <div className="grid grid-cols-[1fr_350px] h-[calc(100vh-64px)]">

        {/* LEFT */}
        <div className="p-4 overflow-hidden">
          <SimulationWorld />
        </div>

        {/* RIGHT */}
        <div className="border-l border-cyan-500/20 overflow-y-auto">

          <ResearchAreaPanel />

          <div className="border-t border-cyan-500/10">
            <ActivityLog />
          </div>

        </div>

      </div>

    </div>
  )
}