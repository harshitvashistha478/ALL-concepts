import { useState } from 'react'
import { userAPI } from '../services/api'
import { useStore } from '../store/useStore'

export default function LandingPage({ onEnter }) {
  const setUser = useStore((s) => s.setUser)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleCreateUser = async () => {
    setLoading(true)
    setError(null)
    try {
      const { data } = await userAPI.createTestUser()
      setUser(data)
      onEnter()
    } catch (e) {
      setError('Failed to connect to Cyber Hub. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden scanlines">
      {/* Background grid */}
      <div className="absolute inset-0"
        style={{
          backgroundImage: `
            linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px'
        }}
      />

      {/* Glow orb */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full"
        style={{ background: 'radial-gradient(circle, rgba(0,212,255,0.06) 0%, transparent 70%)' }}
      />

      <div className="relative z-10 text-center max-w-2xl px-8">
        {/* Logo */}
        <div className="mb-2 text-xs tracking-[0.4em] text-cyber-muted uppercase">
          Multi-Agent Simulation Platform
        </div>

        <h1 className="font-display text-6xl font-black mb-2 leading-none"
          style={{ color: '#00d4ff', textShadow: '0 0 30px rgba(0,212,255,0.4)' }}>
          CYBER
        </h1>
        <h1 className="font-display text-6xl font-black mb-8 leading-none text-white">
          HUB
        </h1>

        {/* Description */}
        <p className="text-cyber-text text-sm leading-relaxed mb-2">
          A living platform where AI agents collaborate like a real tech company.
        </p>
        <p className="text-cyber-muted text-xs mb-10">
          Agent Hub  ·  Research Area  ·  Developer Area  ·  Tester Area
        </p>

        {/* Status indicators */}
        <div className="flex justify-center gap-6 mb-10 text-xs">
          {['Agent Hub', 'Research Area', 'Groq LLM'].map((label) => (
            <div key={label} className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-cyber-green animate-pulse-slow" />
              <span className="text-cyber-muted">{label}</span>
            </div>
          ))}
        </div>

        {/* CTA */}
        <button
          onClick={handleCreateUser}
          disabled={loading}
          className="group relative px-10 py-4 font-display text-sm tracking-widest font-bold uppercase transition-all duration-300"
          style={{
            background: loading ? 'transparent' : 'rgba(0,212,255,0.08)',
            border: '1px solid rgba(0,212,255,0.4)',
            color: '#00d4ff',
            boxShadow: loading ? 'none' : '0 0 20px rgba(0,212,255,0.15)',
          }}
        >
          {loading ? (
            <span className="flex items-center gap-3">
              <span className="inline-block w-4 h-4 border-2 border-cyber-accent border-t-transparent rounded-full animate-spin" />
              Initializing...
            </span>
          ) : (
            '[ Enter as Test User ]'
          )}
        </button>

        {error && (
          <p className="mt-4 text-cyber-red text-xs">{error}</p>
        )}

        <p className="mt-6 text-cyber-muted text-xs">
          No account needed — you'll be assigned a unique identity
        </p>
      </div>
    </div>
  )
}
