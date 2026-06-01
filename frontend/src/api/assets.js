// OWNER: MEMBER-2
import client from './client'

const BASE = '/v1/assets'

/** @returns {Promise<Array>} */
export function getAll(params = {}) {
  return client.get(BASE, { params }).then((r) => r.data)
}

/** @returns {Promise<Object>} */
export function getById(id) {
  return client.get(`${BASE}/${id}`).then((r) => r.data)
}

/** @returns {Promise<Object>} */
export function create(payload) {
  return client.post(BASE, payload).then((r) => r.data)
}

/** @returns {Promise<Object>} */
export function update(id, payload) {
  return client.patch(`${BASE}/${id}`, payload).then((r) => r.data)
}

/** @returns {Promise<void>} */
export function remove(id) {
  return client.delete(`${BASE}/${id}`)
}

// TODO (MEMBER-2): add getByTag(tag), listExpiringWarranties(daysBefore)
