// OWNER: MEMBER-1
import client from './client'

const BASE = '/v1/users'

export function getAll(params = {}) {
  return client.get(BASE, { params }).then((r) => r.data)
}

export function getById(id) {
  return client.get(`${BASE}/${id}`).then((r) => r.data)
}

export function getMe() {
  return client.get(`${BASE}/me`).then((r) => r.data)
}

export function create(payload) {
  return client.post(BASE, payload).then((r) => r.data)
}

export function update(id, payload) {
  return client.patch(`${BASE}/${id}`, payload).then((r) => r.data)
}

export function remove(id) {
  return client.delete(`${BASE}/${id}`)
}
