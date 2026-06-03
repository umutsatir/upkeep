// OWNER: MEMBER-3
import client from './client'

const BASE = '/v1/maintenance'

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

/**
 * Trigger server-side evaluation of all due schedules.
 * Returns the list of work order IDs that were auto-generated.
 * @returns {Promise<Array<string>>}
 */
export function evaluateDue() {
  return client.post(`${BASE}/evaluate`).then((r) => r.data)
}

/** @returns {Promise<Array>} */
export function listByAsset(assetId, params = {}) {
  return getAll({ ...params, asset_id: assetId })
}
