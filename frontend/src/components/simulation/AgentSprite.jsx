import { motion } from 'framer-motion'
import { Bot } from 'lucide-react'

export default function AgentSprite({ agent }) {

  const getColor = () => {
    if (agent.isWorking) return '#00ff88'
    if (agent.isMoving) return '#ffcc00'
    return '#00d4ff'
  }

  return (
    <motion.div
      animate={{
        x: agent.targetX,
        y: agent.targetY,
        scale: agent.isWorking ? [1, 1.1, 1] : 1
      }}
      transition={{
        duration: 3,
        repeat: agent.isWorking ? Infinity : 0
      }}
      className="absolute z-50"
    >

      <div className="flex flex-col items-center">

        <div
          className="w-8 h-8 rounded-full flex items-center justify-center"
          style={{
            background: `${getColor()}22`,
            border: `1px solid ${getColor()}`,
            boxShadow: `0 0 15px ${getColor()}`
          }}
        >
          <Bot size={16} color={getColor()} />
        </div>

        <div className="mt-1 text-[10px] text-cyan-100 whitespace-nowrap">
          {agent.name}
        </div>

      </div>
    </motion.div>
  )
}