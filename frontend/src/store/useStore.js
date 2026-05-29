import { create } from 'zustand'

const HUB_POSITION = { x: 120, y: 320 }
const RESEARCH_POSITION = { x: 850, y: 260 }

export const useStore = create((set, get) => ({

  // USER
  user: null,
  setUser: (user) => set({ user }),

  // AGENTS
  agents: [],

  setAgents: (agents) => {
    const enhancedAgents = agents.map((agent, index) => ({
      ...agent,

      x: HUB_POSITION.x + (index % 3) * 30,
      y: HUB_POSITION.y + Math.floor(index / 3) * 30,

      targetX: HUB_POSITION.x,
      targetY: HUB_POSITION.y,

      currentZone: 'hub',
      isMoving: false,
      isWorking: false,

      animationState: 'idle'
    }))

    set({ agents: enhancedAgents })
  },

  moveAgentsToResearch: () => {
    set((state) => ({
      agents: state.agents.map((agent, index) => ({
        ...agent,

        targetX: RESEARCH_POSITION.x + (index % 3) * 40,
        targetY: RESEARCH_POSITION.y + Math.floor(index / 3) * 40,

        currentZone: 'moving',
        isMoving: true,
        isWorking: false,
        animationState: 'walking'
      }))
    }))
  },

  setAgentsWorking: () => {
    set((state) => ({
      agents: state.agents.map((agent) => ({
        ...agent,
        currentZone: 'research',
        isMoving: false,
        isWorking: true,
        animationState: 'working'
      }))
    }))
  },

  returnAgentsToHub: () => {
    set((state) => ({
      agents: state.agents.map((agent, index) => ({
        ...agent,

        targetX: HUB_POSITION.x + (index % 3) * 30,
        targetY: HUB_POSITION.y + Math.floor(index / 3) * 30,

        currentZone: 'returning',
        isMoving: true,
        isWorking: false,
        animationState: 'walking'
      }))
    }))
  },

  finishReturn: () => {
    set((state) => ({
      agents: state.agents.map((agent) => ({
        ...agent,
        currentZone: 'hub',
        isMoving: false,
        isWorking: false,
        animationState: 'idle'
      }))
    }))
  },

  // RESEARCH
  activeSession: null,
  setActiveSession: (session) => set({ activeSession: session }),

  researchResult: null,
  setResearchResult: (result) => set({ researchResult: result }),

  isResearching: false,
  setIsResearching: (v) => set({ isResearching: v }),

  // ACTIVITY
  activityLog: [],

  addActivity: (message) => set((state) => ({
    activityLog: [
      {
        id: Date.now(),
        message,
        time: new Date().toLocaleTimeString()
      },
      ...state.activityLog.slice(0, 19)
    ]
  }))
}))