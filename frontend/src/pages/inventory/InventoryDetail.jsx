// OWNER: MEMBER-4
import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getById, remove, consume, restock } from '../../api/inventory.js'
import PageHeader from '../../components/PageHeader.jsx'

export default function InventoryDetail() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [item, setItem] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Action panel state
  const [activeAction, setActiveAction] = useState(null) // 'consume' | 'restock' | null
  const [actionLoading, setActionLoading] = useState(false)
  const [actionError, setActionError] = useState(null)

  // Consume form
  const [consumeQty, setConsumeQty] = useState('')
  const [consumeWO, setConsumeWO] = useState('')
  const [consumeNotes, setConsumeNotes] = useState('')

  // Restock form
  const [restockQty, setRestockQty] = useState('')
  const [restockNotes, setRestockNotes] = useState('')

  const fetchItem = useCallback(() => {
    setLoading(true)
    setError(null)
    getById(id)
      .then(setItem)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  useEffect(() => {
    fetchItem()
  }, [fetchItem])

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this item?')) return
    try {
      await remove(id)
      navigate('/inventory')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleConsume = async (e) => {
    e.preventDefault()
    setActionLoading(true)
    setActionError(null)
    try {
      const payload = { quantity: Number(consumeQty) }
      if (consumeWO.trim()) payload.work_order_id = consumeWO.trim()
      if (consumeNotes.trim()) payload.notes = consumeNotes.trim()
      await consume(id, payload)
      setActiveAction(null)
      setConsumeQty('')
      setConsumeWO('')
      setConsumeNotes('')
      fetchItem()
    } catch (err) {
      setActionError(err.response?.data?.message || err.message)
    } finally {
      setActionLoading(false)
    }
  }

  const handleRestock = async (e) => {
    e.preventDefault()
    setActionLoading(true)
    setActionError(null)
    try {
      const payload = { quantity: Number(restockQty) }
      if (restockNotes.trim()) payload.notes = restockNotes.trim()
      await restock(id, payload)
      setActiveAction(null)
      setRestockQty('')
      setRestockNotes('')
      fetchItem()
    } catch (err) {
      setActionError(err.response?.data?.message || err.message)
    } finally {
      setActionLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-16 text-gray-400">
        <svg className="mr-3 h-5 w-5 animate-spin" viewBox="0 0 24 24" fill="none">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
        </svg>
        Loading…
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
        {error}
      </div>
    )
  }

  if (!item) return null

  const isLowStock = item.quantity_on_hand <= (item.low_stock_threshold ?? 0)
  const currencyFmt = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })

  const fields = [
    { label: 'Name', value: item.name },
    { label: 'SKU', value: item.sku },
    { label: 'Category', value: item.category },
    {
      label: 'Quantity on Hand',
      value: (
        <span className="flex items-center gap-2">
          <span className={isLowStock ? 'font-semibold text-red-600' : ''}>{item.quantity_on_hand}</span>
          {isLowStock && (
            <span className="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-700">
              Low Stock
            </span>
          )}
        </span>
      ),
    },
    { label: 'Low Stock Threshold', value: item.low_stock_threshold },
    { label: 'Unit Cost', value: item.unit_cost != null ? currencyFmt.format(item.unit_cost) : '—' },
    { label: 'Unit', value: item.unit },
    { label: 'Supplier', value: item.supplier || '—' },
    { label: 'Location', value: item.location || '—' },
    { label: 'Notes', value: item.notes || '—' },
  ]

  const logs = item.consumption_log ?? []

  return (
    <div>
      <PageHeader
        title={item.name}
        subtitle={`SKU: ${item.sku}`}
        action={
          <div className="flex items-center gap-2">
            <Link
              to={`/inventory/${id}/edit`}
              className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700"
            >
              Edit
            </Link>
            <button
              onClick={() => setActiveAction(activeAction === 'consume' ? null : 'consume')}
              className={`inline-flex items-center gap-1.5 rounded-md px-4 py-2 text-sm font-medium shadow-sm transition-colors ${
                activeAction === 'consume'
                  ? 'bg-orange-600 text-white hover:bg-orange-700'
                  : 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              Consume
            </button>
            <button
              onClick={() => setActiveAction(activeAction === 'restock' ? null : 'restock')}
              className={`inline-flex items-center gap-1.5 rounded-md px-4 py-2 text-sm font-medium shadow-sm transition-colors ${
                activeAction === 'restock'
                  ? 'bg-green-600 text-white hover:bg-green-700'
                  : 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              Restock
            </button>
            <button
              onClick={handleDelete}
              className="inline-flex items-center gap-1.5 rounded-md border border-red-300 bg-white px-4 py-2 text-sm font-medium text-red-600 shadow-sm hover:bg-red-50"
            >
              Delete
            </button>
          </div>
        }
      />

      {/* Consume / Restock inline forms */}
      {activeAction === 'consume' && (
        <div className="mb-6 rounded-lg border border-orange-200 bg-orange-50 p-4">
          <h3 className="mb-3 text-sm font-semibold text-orange-800">Consume Stock</h3>
          {actionError && (
            <div className="mb-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
              {actionError}
            </div>
          )}
          <form onSubmit={handleConsume} className="flex flex-wrap items-end gap-3">
            <div>
              <label className="mb-1 block text-xs font-medium text-gray-700">Quantity *</label>
              <input
                type="number"
                min="1"
                required
                value={consumeQty}
                onChange={(e) => setConsumeQty(e.target.value)}
                className="w-24 rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-600 focus:outline-none focus:ring-1 focus:ring-brand-600"
              />
            </div>
            <div>
              <label className="mb-1 block text-xs font-medium text-gray-700">Work Order ID</label>
              <input
                type="text"
                value={consumeWO}
                onChange={(e) => setConsumeWO(e.target.value)}
                placeholder="Optional"
                className="w-40 rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-600 focus:outline-none focus:ring-1 focus:ring-brand-600"
              />
            </div>
            <div>
              <label className="mb-1 block text-xs font-medium text-gray-700">Notes</label>
              <input
                type="text"
                value={consumeNotes}
                onChange={(e) => setConsumeNotes(e.target.value)}
                placeholder="Optional"
                className="w-48 rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-600 focus:outline-none focus:ring-1 focus:ring-brand-600"
              />
            </div>
            <button
              type="submit"
              disabled={actionLoading}
              className="inline-flex items-center rounded-md bg-orange-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-orange-700 disabled:opacity-50"
            >
              {actionLoading ? 'Consuming…' : 'Confirm'}
            </button>
            <button
              type="button"
              onClick={() => { setActiveAction(null); setActionError(null) }}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Cancel
            </button>
          </form>
        </div>
      )}

      {activeAction === 'restock' && (
        <div className="mb-6 rounded-lg border border-green-200 bg-green-50 p-4">
          <h3 className="mb-3 text-sm font-semibold text-green-800">Restock Item</h3>
          {actionError && (
            <div className="mb-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
              {actionError}
            </div>
          )}
          <form onSubmit={handleRestock} className="flex flex-wrap items-end gap-3">
            <div>
              <label className="mb-1 block text-xs font-medium text-gray-700">Quantity *</label>
              <input
                type="number"
                min="1"
                required
                value={restockQty}
                onChange={(e) => setRestockQty(e.target.value)}
                className="w-24 rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-600 focus:outline-none focus:ring-1 focus:ring-brand-600"
              />
            </div>
            <div>
              <label className="mb-1 block text-xs font-medium text-gray-700">Notes</label>
              <input
                type="text"
                value={restockNotes}
                onChange={(e) => setRestockNotes(e.target.value)}
                placeholder="Optional"
                className="w-48 rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-600 focus:outline-none focus:ring-1 focus:ring-brand-600"
              />
            </div>
            <button
              type="submit"
              disabled={actionLoading}
              className="inline-flex items-center rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-green-700 disabled:opacity-50"
            >
              {actionLoading ? 'Restocking…' : 'Confirm'}
            </button>
            <button
              type="button"
              onClick={() => { setActiveAction(null); setActionError(null) }}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Cancel
            </button>
          </form>
        </div>
      )}

      {/* Item Details Card */}
      <div className="mb-6 rounded-lg border border-gray-200 bg-white shadow-sm">
        <div className="border-b border-gray-200 px-6 py-4">
          <h2 className="text-lg font-semibold text-gray-900">Item Details</h2>
        </div>
        <dl className="grid grid-cols-1 gap-x-6 gap-y-4 px-6 py-5 sm:grid-cols-2 lg:grid-cols-3">
          {fields.map((f) => (
            <div key={f.label}>
              <dt className="text-xs font-medium uppercase tracking-wider text-gray-500">{f.label}</dt>
              <dd className="mt-1 text-sm text-gray-900">{f.value}</dd>
            </div>
          ))}
        </dl>
      </div>

      {/* Consumption Log */}
      <div className="rounded-lg border border-gray-200 bg-white shadow-sm">
        <div className="border-b border-gray-200 px-6 py-4">
          <h2 className="text-lg font-semibold text-gray-900">Consumption Log</h2>
        </div>
        {logs.length === 0 ? (
          <div className="px-6 py-10 text-center text-sm text-gray-400">No consumption records.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold uppercase tracking-wider text-gray-500">Date</th>
                  <th className="px-4 py-3 text-left font-semibold uppercase tracking-wider text-gray-500">Quantity</th>
                  <th className="px-4 py-3 text-left font-semibold uppercase tracking-wider text-gray-500">Work Order</th>
                  <th className="px-4 py-3 text-left font-semibold uppercase tracking-wider text-gray-500">Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 bg-white">
                {logs.map((log, i) => (
                  <tr key={log.id ?? i} className="hover:bg-gray-50 transition-colors">
                    <td className="whitespace-nowrap px-4 py-3 text-gray-700">
                      {log.timestamp ? new Date(log.timestamp).toLocaleDateString() : '—'}
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-gray-700">{log.quantity}</td>
                    <td className="whitespace-nowrap px-4 py-3 text-gray-700">
                      {log.work_order_id ? (
                        <Link to={`/work-orders/${log.work_order_id}`} className="text-brand-600 hover:text-brand-800 underline underline-offset-2">
                          {log.work_order_id}
                        </Link>
                      ) : '—'}
                    </td>
                    <td className="px-4 py-3 text-gray-700">{log.notes || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
