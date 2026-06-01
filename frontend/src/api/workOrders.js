// OWNER: MEMBER-1
import client from './client'

const BASE = '/v1/work-orders'

/**
 * @returns {Promise<Array>} list of work order objects
 */
export function getAll(params = {}) {
  return client.get(BASE, { params }).then((r) => r.data)
}

/**
 * @param {string} id
 * @returns {Promise<Object>}
 */
export function getById(id) {
  return client.get(`${BASE}/${id}`).then((r) => r.data)
}

/**
 * @param {Object} payload - WorkOrderCreate fields
 * @returns {Promise<Object>} created work order
 */
export function create(payload) {
  return client.post(BASE, payload).then((r) => r.data)
}

/**
 * @param {string} id
 * @param {Object} payload - WorkOrderUpdate fields
 * @returns {Promise<Object>} updated work order
 */
export function update(id, payload) {
  return client.patch(`${BASE}/${id}`, payload).then((r) => r.data)
}

/**
 * @param {string} id
 * @param {Object} payload - { new_status, assigned_to? }
 * @returns {Promise<Object>} transitioned work order
 */
export function transition(id, payload) {
  return client.post(`${BASE}/${id}/transition`, payload).then((r) => r.data)
}

/**
 * @param {string} id
 * @returns {Promise<void>}
 */
export function remove(id) {
  return client.delete(`${BASE}/${id}`)
}
