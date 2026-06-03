// OWNER: MEMBER-1
import client from './client'

const BASE = '/v1/auth'

export function register(payload) {
  return client.post(`${BASE}/register`, payload).then((r) => r.data)
}

export function login(email, password) {
  return client.post(`${BASE}/login`, { email, password }).then((r) => r.data)
}
