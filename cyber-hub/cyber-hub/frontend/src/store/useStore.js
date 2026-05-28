import { create } from 'zustand'

export const useStore = create((set, get) => ({
  // Current user
  user: null,
  setUser: (user) => set({ user }),

  // Agents visible in the hub
  agents: [],
  setAgents: (agents) => set({ agents }),

  // Active research session
  activeSession: null,
  setActiveSession: (session) => set({ activeSession: session }),

  // Research result
  researchResult: null,
  setResearchResult: (result) => set({ researchResult: result }),

  // UI state
  isResearching: false,
  setIsResearching: (v) => set({ isResearching: v }),

  // Research history
  history: [],
  setHistory: (history) => set({ history }),

  // Log of what's happening (shown in the UI as live activity)
  activityLog: [],
  addActivity: (message) => set((state) => ({
    activityLog: [
      { id: Date.now(), message, time: new Date().toLocaleTimeString() },
      ...state.activityLog.slice(0, 19)  // keep last 20 entries
    ]
  })),
  clearActivity: () => set({ activityLog: [] })
}))
