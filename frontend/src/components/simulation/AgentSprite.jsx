import { motion } from 'framer-motion'

export default function AgentSprite({ agent }) {

  const getGlow = () => {
    if (agent.isWorking) return '#00ff88'
    if (agent.isMoving) return '#ffcc00'
    return '#00d4ff'
  }

  return (

    <motion.div
      animate={{
        x: agent.targetX,
        y: agent.targetY,
      }}
      transition={{
        duration: 3,
        ease: 'linear'
      }}
      className="absolute z-50"
    >

      <div className="flex flex-col items-center">

        {/* HUMAN */}
        <motion.div
          animate={{
            y: [0, -2, 0]
          }}
          transition={{
            repeat: Infinity,
            duration: 0.6
          }}
          className="relative"
        >

          {/* HEAD */}
          <div
            className="w-4 h-4 rounded-full"
            style={{
              background: getGlow(),
              boxShadow: `0 0 10px ${getGlow()}`
            }}
          />

          {/* BODY */}
          <div
            className="w-[2px] h-5 mx-auto"
            style={{
              background: getGlow()
            }}
          />

          {/* ARMS */}
          <div
            className="absolute top-5 left-[-4px] w-10 h-[2px]"
            style={{
              background: getGlow()
            }}
          />

          {/* LEGS */}
          <div className="relative">

            <motion.div
              animate={{
                rotate: agent.isMoving ? [-20, 20, -20] : 0
              }}
              transition={{
                repeat: Infinity,
                duration: 0.4
              }}
              className="absolute left-[6px] top-0 w-[2px] h-4 origin-top"
              style={{
                background: getGlow()
              }}
            />

            <motion.div
              animate={{
                rotate: agent.isMoving ? [20, -20, 20] : 0
              }}
              transition={{
                repeat: Infinity,
                duration: 0.4
              }}
              className="absolute left-[12px] top-0 w-[2px] h-4 origin-top"
              style={{
                background: getGlow()
              }}
            />

          </div>

        </motion.div>

        {/* NAME */}
        <div className="mt-3 text-[9px] text-cyan-100 whitespace-nowrap">
          {agent.name}
        </div>

      </div>

    </motion.div>
  )
}