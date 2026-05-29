import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import { researchAPI, hubAPI } from '../services/api'
import { useStore } from '../store/useStore'

const STATUS_MESSAGES = {
  pending:    '⏳ Assembling research team...',
  processing: '🔬 Agents are researching...',
  completed:  '✅ Research complete',
  failed:     '❌ Research failed',
}

export default function ResearchAreaPanel() {
  const user            = useStore((s) => s.user)
  const isResearching   = useStore((s) => s.isResearching)
  const setIsResearching = useStore((s) => s.setIsResearching)
  const researchResult  = useStore((s) => s.researchResult)
  const setResearchResult = useStore((s) => s.setResearchResult)
  const setAgents       = useStore((s) => s.setAgents)
  const addActivity     = useStore((s) => s.addActivity)

  const [topic, setTopic] = useState('')
  const [sessionStatus, setSessionStatus] = useState(null)
  const [agentsUsed, setAgentsUsed] = useState([])
  const [error, setError] = useState(null)
  const [plan, setPlan] = useState(null)
  const pollRef = useRef(null)

  const handleSubmit = async () => {
    if (!topic.trim() || isResearching) return
    setError(null)
    setResearchResult(null)
    setAgentsUsed([])
    setPlan(null)
    setIsResearching(true)
    addActivity(`New research request: "${topic}"`)

    try {
      const { data } = await researchAPI.submit(user.id, topic)
      addActivity('Research Major is planning agent team...')
      setSessionStatus('pending')
      startPolling(data.session_id)
    } catch (e) {
      setError('Failed to submit research. Is the backend running?')
      setIsResearching(false)
    }
  }

  const startPolling = (sessionId) => {
    pollRef.current = setInterval(async () => {
      try {
        const { data } = await researchAPI.getResult(sessionId)
        setSessionStatus(data.status)

        if (data.agents_used?.length > 0) {
          setAgentsUsed(data.agents_used)
          addActivity(`${data.agents_used.length} agent(s) spawned from Hub`)
        }

        if (data.status === 'processing') {
          addActivity('Agents are conducting research...')
        }

        if (data.status === 'completed') {
          clearInterval(pollRef.current)
          setResearchResult(data.result)
          setIsResearching(false)
          addActivity('Research synthesized. Report ready.')
          // Refresh agent list
          const agents = await hubAPI.getAllAgents()
          setAgents(agents.data)
        }

        if (data.status === 'failed') {
          clearInterval(pollRef.current)
          setError(data.result || 'Research failed.')
          setIsResearching(false)
        }
      } catch (e) {
        console.error('Poll error', e)
      }
    }, 3000)
  }

  useEffect(() => () => clearInterval(pollRef.current), [])

  return (
    <div className="p-6 max-w-3xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <div className="text-xs text-cyber-muted uppercase tracking-widest mb-1">Department</div>
        <h2 className="font-display text-white text-xl font-bold tracking-wider">
          RESEARCH AREA
        </h2>
        <p className="text-cyber-muted text-xs mt-1">
          Submit a topic. The Major will assemble a team and deliver a full report.
        </p>
      </div>

      {/* Input */}
      <div className="glow-border rounded p-4 mb-6">
        <label className="block text-xs text-cyber-muted mb-2 uppercase tracking-widest">
          Research Topic
        </label>
        <textarea
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="e.g. How does React handle state management in large apps?"
          rows={3}
          disabled={isResearching}
          className="w-full bg-transparent text-cyber-text text-sm resize-none outline-none placeholder:text-cyber-muted/40 leading-relaxed"
          onKeyDown={(e) => {
            if (e.key === 'Enter' && e.ctrlKey) handleSubmit()
          }}
        />
        <div className="flex items-center justify-between mt-3">
          <span className="text-cyber-muted text-xs">Ctrl+Enter to submit</span>
          <button
            onClick={handleSubmit}
            disabled={isResearching || !topic.trim()}
            className="px-5 py-2 text-xs font-display tracking-widest uppercase transition-all duration-200"
            style={{
              background: isResearching || !topic.trim()
                ? 'transparent'
                : 'rgba(0,212,255,0.1)',
              border: '1px solid',
              borderColor: isResearching || !topic.trim()
                ? 'rgba(0,212,255,0.15)'
                : 'rgba(0,212,255,0.5)',
              color: isResearching || !topic.trim() ? '#3a5a7a' : '#00d4ff',
            }}
          >
            {isResearching ? 'Researching...' : 'Deploy Agents →'}
          </button>
        </div>
      </div>

      {/* Status bar */}
      {sessionStatus && (
        <div className="glow-border rounded px-4 py-3 mb-4 flex items-center gap-3">
          <span className={`w-2 h-2 rounded-full flex-shrink-0 ${
            sessionStatus === 'completed' ? 'bg-cyber-green' :
            sessionStatus === 'failed'    ? 'bg-cyber-red' :
            'bg-cyber-yellow animate-pulse'
          }`} />
          <span className="text-xs">{STATUS_MESSAGES[sessionStatus]}</span>
        </div>
      )}

      {/* Agents being used */}
      {agentsUsed.length > 0 && (
        <div className="mb-4">
          <div className="text-xs text-cyber-muted mb-2 uppercase tracking-widest">
            Agents on this task
          </div>
          <div className="flex flex-wrap gap-2">
            {agentsUsed.map((agent) => (
              <div key={agent.id}
                className="glow-border rounded px-3 py-1.5 text-xs flex items-center gap-2">
                <span className={`w-1.5 h-1.5 rounded-full ${
                  agent.status === 'busy'     ? 'bg-cyber-yellow animate-pulse' :
                  agent.status === 'released' ? 'bg-cyber-green' :
                  'bg-cyber-muted'
                }`} />
                <span className="text-cyber-accent">{agent.name}</span>
                <span className="text-cyber-muted">{agent.role}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="glow-border border-cyber-red/30 rounded p-4 mb-4 text-cyber-red text-sm">
          {error}
        </div>
      )}

      {/* Research result */}
      {researchResult && (
        <div className="glow-border rounded p-5">
          <div className="text-xs text-cyber-muted uppercase tracking-widest mb-4">
            Final Report
          </div>
          <div className="prose prose-invert prose-sm max-w-none"
            style={{
              '--tw-prose-headings': '#00d4ff',
              '--tw-prose-body': '#a8c8e8',
              '--tw-prose-bold': '#ffffff',
            }}>
            <ReactMarkdown
              components={{
                h1: ({children}) => <h1 className="font-display text-cyber-accent text-lg mb-3">{children}</h1>,
                h2: ({children}) => <h2 className="font-display text-cyber-accent text-base mb-2 mt-4">{children}</h2>,
                h3: ({children}) => <h3 className="text-white text-sm font-bold mb-2 mt-3">{children}</h3>,
                p:  ({children}) => <p className="text-cyber-text text-sm leading-relaxed mb-3">{children}</p>,
                li: ({children}) => <li className="text-cyber-text text-sm mb-1">{children}</li>,
                strong: ({children}) => <strong className="text-white">{children}</strong>,
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
