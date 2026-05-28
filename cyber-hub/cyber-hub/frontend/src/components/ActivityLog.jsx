import { useStore } from '../store/useStore'

export default function ActivityLog() {
  const activityLog = useStore((s) => s.activityLog)

  return (
    <div className="p-4">
      <div className="mb-4">
        <div className="text-xs text-cyber-muted uppercase tracking-widest mb-1">System</div>
        <h2 className="font-display text-cyber-green text-sm font-bold tracking-wider">
          ACTIVITY LOG
        </h2>
      </div>

      {activityLog.length === 0 ? (
        <div className="text-cyber-muted text-xs text-center py-6">
          No activity yet
        </div>
      ) : (
        <div className="space-y-2">
          {activityLog.map((entry) => (
            <div key={entry.id} className="text-xs border-l-2 border-cyber-border pl-3 py-1">
              <div className="text-cyber-muted mb-0.5">{entry.time}</div>
              <div className="text-cyber-text leading-relaxed">{entry.message}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
