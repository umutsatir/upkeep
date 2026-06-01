// OWNER: MEMBER-4
import client from './client'

const BASE = '/v1/inventory'

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
 * @returns {Promise<Array>} items where quantity_on_hand <= low_stock_threshold
 */
export function getLowStock() {
  return client.get(`${BASE}/low-stock`).then((r) => r.data)
}

/**
 * @param {string} id
 * @param {{ quantity: number, work_order_id?: string, notes?: string }} payload
 * @returns {Promise<Object>} updated item
 */
export function consume(id, payload) {
  return client.post(`${BASE}/${id}/consume`, payload).then((r) => r.data)
}

/**
 * @param {string} id
 * @param {{ quantity: number, notes?: string }} payload
 * @returns {Promise<Object>} updated item
 */
export function restock(id, payload) {
  return client.post(`${BASE}/${id}/restock`, payload).then((r) => r.data)
}
