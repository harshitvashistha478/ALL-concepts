import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

export const userAPI = {
  createTestUser: () => api.post('/users/create-test-user'),
  getUser: (id) => api.get(`/users/${id}`)
}

export const researchAPI = {
  submit: (userId, topic) =>
    api.post('/research/submit', { user_id: userId, topic }),
  getResult: (sessionId) => api.get(`/research/${sessionId}`),
  getHistory: (userId) => api.get(`/research/history/${userId}`)
}

export const hubAPI = {
  getAllAgents: () => api.get('/hub/agents')
}
