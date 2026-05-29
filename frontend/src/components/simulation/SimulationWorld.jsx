import { useStore } from '../../store/useStore'
import Building from './Building'
import AgentSprite from './AgentSprite'
import MovementPath from './MovementPath'

export default function SimulationWorld() {

  const agents = useStore((s) => s.agents)

  return (
    <div className="relative w-full h-[600px] overflow-hidden rounded-xl border border-cyan-500/20 bg-[#050a0f]">

      {/* Grid Background */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage: `
            linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px'
        }}
      />

      {/* Roads */}
      <MovementPath />

      {/* Buildings */}
      <Building
        title="AGENT HUB"
        x={60}
        y={220}
        width={220}
        height={220}
        color="cyan"
      />

      <Building
        title="RESEARCH LAB"
        x={720}
        y={170}
        width={260}
        height={260}
        color="purple"
      />

      {/* Agents */}
      {agents.map((agent) => (
        <AgentSprite key={agent.id} agent={agent} />
      ))}
    </div>
  )
}