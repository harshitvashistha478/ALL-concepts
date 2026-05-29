import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'

import { researchAPI, hubAPI } from '../services/api'
import { useStore } from '../store/useStore'

const STATUS_MESSAGES = {
  pending: '🧠 Planning research operation...',
  processing: '⚡ Agents actively researching...',
  completed: '✅ Research operation completed',
  failed: '❌ Mission failed'
}

export default function ResearchAreaPanel() {

  // STORE
  const user = useStore((s) => s.user)

  const isResearching = useStore((s) => s.isResearching)
  const setIsResearching = useStore((s) => s.setIsResearching)

  const researchResult = useStore((s) => s.researchResult)
  const setResearchResult = useStore((s) => s.setResearchResult)

  const setAgents = useStore((s) => s.setAgents)

  const addActivity = useStore((s) => s.addActivity)

  // SIMULATION ACTIONS
  const moveAgentsToResearch = useStore((s) => s.moveAgentsToResearch)
  const setAgentsWorking = useStore((s) => s.setAgentsWorking)
  const returnAgentsToHub = useStore((s) => s.returnAgentsToHub)
  const finishReturn = useStore((s) => s.finishReturn)

  // LOCAL STATE
  const [topic, setTopic] = useState('')
  const [sessionStatus, setSessionStatus] = useState(null)
  const [agentsUsed, setAgentsUsed] = useState([])
  const [error, setError] = useState(null)

  const pollRef = useRef(null)

  // SUBMIT RESEARCH
  const handleSubmit = async () => {

    if (!topic.trim() || isResearching) return

    setError(null)

    setResearchResult(null)

    setAgentsUsed([])

    setIsResearching(true)

    addActivity(`New mission received: "${topic}"`)

    try {

      const { data } = await researchAPI.submit(user.id, topic)

      setSessionStatus('pending')

      addActivity('Research Major assembling agent squad...')

      // MOVE AGENTS TO LAB
      moveAgentsToResearch()

      // AFTER WALKING -> START WORKING
      setTimeout(() => {

        setAgentsWorking()

        addActivity('Agents entered Research Lab.')

      }, 3000)

      startPolling(data.session_id)

    } catch (e) {

      console.error(e)

      setError('Failed to initialize research mission.')

      setIsResearching(false)
    }
  }

  // POLLING
  const startPolling = (sessionId) => {

    pollRef.current = setInterval(async () => {

      try {

        const { data } = await researchAPI.getResult(sessionId)

        setSessionStatus(data.status)

        // AGENTS USED
        if (data.agents_used?.length > 0) {

          setAgentsUsed(data.agents_used)

        }

        // PROCESSING
        if (data.status === 'processing') {

          addActivity('Agents are processing intelligence...')

        }

        // COMPLETED
        if (data.status === 'completed') {

          clearInterval(pollRef.current)

          setResearchResult(data.result)

          setIsResearching(false)

          addActivity('Research synthesis completed.')

          // RETURN AGENTS
          returnAgentsToHub()

          addActivity('Agents returning to Agent Hub...')

          setTimeout(() => {

            finishReturn()

            addActivity('All agents returned successfully.')

          }, 3000)

          // REFRESH AGENTS
          const agents = await hubAPI.getAllAgents()

          setAgents(agents.data)
        }

        // FAILED
        if (data.status === 'failed') {

          clearInterval(pollRef.current)

          setError(data.result || 'Mission failed.')

          setIsResearching(false)

          returnAgentsToHub()

          setTimeout(() => {

            finishReturn()

          }, 3000)
        }

      } catch (e) {

        console.error('Polling Error:', e)

      }

    }, 3000)
  }

  // CLEANUP
  useEffect(() => {

    return () => {

      clearInterval(pollRef.current)

    }

  }, [])

  return (

    <div className="p-6 text-white">

      {/* HEADER */}
      <div className="mb-6">

        <div className="text-xs uppercase tracking-[0.4em] text-cyan-400 mb-2">
          RESEARCH COMMAND
        </div>

        <h1 className="text-2xl font-black tracking-[0.2em] text-white">
          OPERATIONS PANEL
        </h1>

        <p className="text-cyan-200/70 text-sm mt-3 leading-relaxed">
          Deploy autonomous AI agents into the Research Lab.
          Agents will investigate, collaborate, synthesize findings,
          and return with a final intelligence report.
        </p>

      </div>

      {/* INPUT PANEL */}
      <div className="border border-cyan-500/20 rounded-2xl p-5 bg-cyan-500/[0.03] backdrop-blur-sm mb-6">

        <div className="text-xs uppercase tracking-[0.3em] text-cyan-400 mb-3">
          Mission Topic
        </div>

        <textarea
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          rows={4}
          disabled={isResearching}
          placeholder="Example: Analyze how LangGraph manages stateful multi-agent workflows..."
          className="
            w-full
            bg-black/30
            border
            border-cyan-500/10
            rounded-xl
            p-4
            text-sm
            text-cyan-100
            placeholder:text-cyan-200/30
            outline-none
            resize-none
            focus:border-cyan-400/40
            transition-all
          "
        />

        <div className="flex items-center justify-between mt-4">

          <div className="text-xs text-cyan-300/50">
            CTRL + ENTER to deploy agents
          </div>

          <button
            onClick={handleSubmit}
            disabled={isResearching || !topic.trim()}
            className="
              px-6
              py-3
              rounded-xl
              text-sm
              font-bold
              tracking-[0.2em]
              transition-all
              duration-300
            "
            style={{
              background: isResearching
                ? 'rgba(255,255,255,0.03)'
                : 'rgba(0,212,255,0.08)',

              border: '1px solid rgba(0,212,255,0.3)',

              color: isResearching
                ? '#5a7188'
                : '#00d4ff',

              boxShadow: isResearching
                ? 'none'
                : '0 0 20px rgba(0,212,255,0.15)'
            }}
          >

            {isResearching
              ? 'MISSION ACTIVE...'
              : 'DEPLOY AGENTS'}

          </button>

        </div>

      </div>

      {/* STATUS */}
      {sessionStatus && (

        <div
          className="
            mb-6
            border
            border-cyan-500/20
            rounded-xl
            p-4
            flex
            items-center
            gap-3
            bg-black/20
          "
        >

          <div
            className={`
              w-3
              h-3
              rounded-full
              ${
                sessionStatus === 'completed'
                  ? 'bg-green-400'

                  : sessionStatus === 'failed'
                  ? 'bg-red-400'

                  : 'bg-yellow-400 animate-pulse'
              }
            `}
          />

          <div className="text-sm text-cyan-100">
            {STATUS_MESSAGES[sessionStatus]}
          </div>

        </div>

      )}

      {/* AGENTS */}
      {agentsUsed.length > 0 && (

        <div className="mb-6">

          <div className="text-xs uppercase tracking-[0.3em] text-cyan-400 mb-3">
            Active Agents
          </div>

          <div className="flex flex-wrap gap-3">

            {agentsUsed.map((agent) => (

              <div
                key={agent.id}
                className="
                  border
                  border-cyan-500/20
                  rounded-xl
                  px-4
                  py-2
                  bg-cyan-500/[0.03]
                  text-xs
                "
              >

                <div className="text-cyan-300 font-semibold">
                  {agent.name}
                </div>

                <div className="text-cyan-100/50 mt-1">
                  {agent.role}
                </div>

              </div>

            ))}

          </div>

        </div>

      )}

      {/* ERROR */}
      {error && (

        <div
          className="
            border
            border-red-500/30
            bg-red-500/10
            rounded-xl
            p-4
            text-red-300
            text-sm
            mb-6
          "
        >
          {error}
        </div>

      )}

      {/* RESULT */}
      {researchResult && (

        <div
          className="
            border
            border-cyan-500/20
            rounded-2xl
            p-6
            bg-cyan-500/[0.02]
          "
        >

          <div className="text-xs uppercase tracking-[0.4em] text-cyan-400 mb-6">
            FINAL INTELLIGENCE REPORT
          </div>

          <div className="prose prose-invert max-w-none">

            <ReactMarkdown
              components={{

                h1: ({ children }) => (
                  <h1 className="text-2xl text-cyan-300 font-black mb-5">
                    {children}
                  </h1>
                ),

                h2: ({ children }) => (
                  <h2 className="text-xl text-cyan-200 font-bold mt-8 mb-4">
                    {children}
                  </h2>
                ),

                h3: ({ children }) => (
                  <h3 className="text-lg text-white font-semibold mt-6 mb-3">
                    {children}
                  </h3>
                ),

                p: ({ children }) => (
                  <p className="text-cyan-100/90 leading-relaxed mb-4">
                    {children}
                  </p>
                ),

                li: ({ children }) => (
                  <li className="text-cyan-100/90 mb-2">
                    {children}
                  </li>
                ),

                strong: ({ children }) => (
                  <strong className="text-white">
                    {children}
                  </strong>
                )

              }}
            >
              {researchResult}
            </ReactMarkdown>

          </div>

        </div>

      )}

    </div>
  )
}