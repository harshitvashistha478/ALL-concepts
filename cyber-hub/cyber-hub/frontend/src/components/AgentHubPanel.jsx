import { useStore } from '../store/useStore'

const STATUS_COLORS = {
  idle:     { dot: 'bg-cyber-muted',   label: 'text-cyber-muted' },
  busy:     { dot: 'bg-cyber-yellow animate-pulse', label: 'text-cyber-yellow' },
  released: { dot: 'bg-cyber-green',   label: 'text-cyber-green' },
}

const SKILL_COLORS = {
  junior: 'text-cyber-muted',
  mid:    'text-cyber-text',
  senior: 'text-cyber-accent',
  expert: 'text-cyber-yellow',
}

export default function AgentHubPanel() {
  const agents = useStore((s) => s.agents)

  const idle     = agents.filter((a) => a.status === 'idle')
  const busy     = agents.filter((a) => a.status === 'busy')
  const released = agents.filter((a) => a.status === 'released')

  return (
    <div className="p-4">
      {/* Header */}
      <div className="mb-4">
        <div className="text-xs text-cyber-muted uppercase tracking-widest mb-1">System</div>
        <h2 className="font-display text-cyber-accent text-sm font-bold tracking-wider">
          AGENT HUB
        </h2>
        <p className="text-cyber-muted text-xs mt-1">
          Spawns agents on demand
        </p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-2 mb-4">
        {[
          { label: 'Total',    value: agents.length,    color: 'text-cyber-text' },
          { label: 'Active',   value: busy.length,      color: 'text-cyber-yellow' },
          { label: 'Done',     value: released.length,  color: 'text-cyber-green' },
        ].map(({ label, value, color }) => (
          <div key={label} className="glow-border rounded p-2 text-center">
            <div className={`text-lg font-bold font-display ${color}`}>{value}</div>
            <div className="text-xs text-cyber-muted">{label}</div>
          </div>
        ))}
      </div>

      {/* Agent list */}
      {agents.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-cyber-muted text-xs">No agents spawned yet</div>
          <div className="text-cyber-muted text-xs mt-1">Submit a research topic to begin</div>
        </div>
      ) : (
        <div className="space-y-2">
          {agents.map((agent) => {
            const statusStyle = STATUS_COLORS[agent.status] || STATUS_COLORS.idle
            return (
              <div key={agent.id} className="glow-border rounded p-3 text-xs">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-cyber-text font-medium truncate">{agent.name}</span>
                  <div className="flex items-center gap-1 flex-shrink-0 ml-2">
                    <span className={`w-1.5 h-1.5 rounded-full ${statusStyle.dot}`} />
                    <span className={statusStyle.label}>{agent.status}</span>
                  </div>
                </div>
                <div className="text-cyber-muted truncate">{agent.role}</div>
                <div className={`mt-1 ${SKILL_COLORS[agent.skill_level]}`}>
                  ⬆ {agent.skill_level}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
