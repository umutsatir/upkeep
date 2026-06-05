// OWNER: MEMBER-1
import { useState, useEffect } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getById, transition, remove } from '../../api/workOrders.js'
import { getAll as getAllInventory } from '../../api/inventory.js'
import StatusBadge from '../../components/StatusBadge.jsx'
import PageHeader from '../../components/PageHeader.jsx'

// Maps current status → list of { label, next_status, style }
const TRANSITIONS = {
  open: [
    { label: 'Assign',        next: 'assigned',    style: 'blue',  needsAssignee: true },
    { label: 'Cancel',        next: 'cancelled',   style: 'red' },
  ],
  assigned: [
    { label: 'Start Work',    next: 'in_progress', style: 'orange' },
    { label: 'Cancel',        next: 'cancelled',   style: 'red' },
  ],
  in_progress: [
    { label: 'Mark Complete', next: 'completed',   style: 'green' },
    { label: 'Cancel',        next: 'cancelled',   style: 'red' },
  ],
  completed: [
    { label: 'Close',         next: 'closed',      style: 'gray' },
  ],
}

const BTN = {
  blue:   'bg-blue-600 hover:bg-blue-700 text-white',
  orange: 'bg-orange-500 hover:bg-orange-600 text-white',
  green:  'bg-green-600 hover:bg-green-700 text-white',
  gray:   'bg-gray-500 hover:bg-gray-600 text-white',
  red:    'border border-red-300 bg-white text-red-600 hover:bg-red-50',
}

export default function WorkOrderDetail() {
  const { id }   = useParams()
  const navigate = useNavigate()

  const [wo, setWo]             = useState(null)
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)
  const [assignee, setAssignee]         = useState('')
  const [acting, setActing]             = useState(false)
  const [showCompleteModal, setShowCompleteModal] = useState(false)

  useEffect(() => {
    setLoading(true)
    getById(id)
      .then(setWo)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  async function handleTransition(next, needsAssignee, partsUsed = []) {
    if (needsAssignee && !assignee.trim()) {
      alert('Please enter the assignee user ID.')
      return
    }
    setActing(true)
    try {
      const updated = await transition(id, {
        new_status:  next,
        assigned_to: needsAssignee ? assignee.trim() : undefined,
        parts_used:  partsUsed,
      })
      setWo(updated)
      setAssignee('')
    } catch (err) {
      setError(err.message)
    } finally {
      setActing(false)
    }
  }

  function handleActionClick(next, needsAssignee) {
    if (next === 'completed') {
      setShowCompleteModal(true)
    } else {
      handleTransition(next, needsAssignee)
    }
  }

  async function handleDelete() {
    if (!window.confirm('Delete this work order?')) return
    try {
      await remove(id)
      navigate('/work-orders', { replace: true })
    } catch (err) {
      setError(err.message)
    }
  }

  if (loading) return <p className="py-8 text-center text-gray-400">Loading…</p>
  if (error)   return <p className="py-8 text-center text-red-600">{error}</p>
  if (!wo)     return null

  const actions = TRANSITIONS[wo.status] ?? []

  return (
    <div className="mx-auto max-w-2xl space-y-4 sm:space-y-6">
      <PageHeader
        title={wo.title}
        subtitle={`Work Order · ${wo.id}`}
        backTo="/work-orders"
        action={
          <div className="flex flex-wrap gap-2">
            <Link
              to={`/work-orders/${id}/edit`}
              className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Edit
            </Link>
            <button
              onClick={handleDelete}
              className="rounded-md border border-red-200 bg-white px-3 py-1.5 text-sm font-medium text-red-600 hover:bg-red-50"
            >
              Delete
            </button>
          </div>
        }
      />

      {/* Details card */}
      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <dl className="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-2 lg:grid-cols-3">
          <Field label="Status"    value={<StatusBadge value={wo.status} />} />
          <Field label="Priority"  value={<StatusBadge value={wo.priority} />} />
          <Field label="Asset ID"  value={<code className="rounded bg-gray-100 px-1 text-xs">{wo.asset_id}</code>} />
          <Field label="Due Date"  value={wo.due_date ? new Date(wo.due_date).toLocaleDateString() : '—'} />
          <Field label="Completed" value={wo.completed_at ? new Date(wo.completed_at).toLocaleDateString() : '—'} />
          <Field label="Assigned"  value={wo.assigned_to ?? '—'} />
          <Field label="Created"   value={new Date(wo.created_at).toLocaleString()} />
          <Field label="Updated"   value={new Date(wo.updated_at).toLocaleString()} />
        </dl>

        {wo.notes && (
          <div className="mt-4 border-t pt-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">Notes</p>
            <p className="mt-1 text-sm text-gray-800">{wo.notes}</p>
          </div>
        )}
      </div>

      {/* Transition panel */}
      {actions.length > 0 && (
        <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <p className="mb-3 text-sm font-semibold text-gray-700">Lifecycle Actions</p>

          {actions.some((a) => a.needsAssignee) && (
            <input
              type="text"
              placeholder="Assignee user ID"
              value={assignee}
              onChange={(e) => setAssignee(e.target.value)}
              className="mb-3 w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            />
          )}

          <div className="flex flex-wrap gap-2">
            {actions.map(({ label, next, style, needsAssignee }) => (
              <button
                key={next}
                disabled={acting}
                onClick={() => handleActionClick(next, needsAssignee)}
                className={`rounded-md px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 ${BTN[style]}`}
              >
                {acting ? '…' : label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Parts used */}
      {wo.parts_used?.length > 0 && (
        <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <p className="mb-3 text-sm font-semibold text-gray-700">Parts Used</p>
          <ul className="space-y-1 text-sm text-gray-700">
            {wo.parts_used.map((p, i) => (
              <li key={i}>
                <code className="rounded bg-gray-100 px-1 text-xs">{p.inventory_item_id}</code>
                {' × '}{p.quantity}
              </li>
            ))}
          </ul>
        </div>
      )}

      {showCompleteModal && (
        <CompleteModal
          workOrderId={id}
          onConfirm={(partsUsed) => {
            setShowCompleteModal(false)
            handleTransition('completed', false, partsUsed)
          }}
          onCancel={() => setShowCompleteModal(false)}
        />
      )}
    </div>
  )
}

function CompleteModal({ onConfirm, onCancel }) {
  const [inventory, setInventory]   = useState([])
  const [loadingInv, setLoadingInv] = useState(true)
  const [rows, setRows]             = useState([{ inventory_item_id: '', quantity: 1 }])

  useEffect(() => {
    getAllInventory({ limit: 200 })
      .then(setInventory)
      .finally(() => setLoadingInv(false))
  }, [])

  function addRow() {
    setRows((prev) => [...prev, { inventory_item_id: '', quantity: 1 }])
  }

  function removeRow(index) {
    setRows((prev) => prev.filter((_, i) => i !== index))
  }

  function updateRow(index, field, value) {
    setRows((prev) => prev.map((r, i) => i === index ? { ...r, [field]: value } : r))
  }

  function handleConfirm() {
    const parts = rows
      .filter((r) => r.inventory_item_id)
      .map((r) => ({ inventory_item_id: r.inventory_item_id, quantity: Number(r.quantity) }))
    onConfirm(parts)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
        <h2 className="mb-1 text-base font-semibold text-gray-900">Complete Work Order</h2>
        <p className="mb-4 text-sm text-gray-500">Select the inventory items used (optional).</p>

        {loadingInv ? (
          <p className="py-4 text-center text-sm text-gray-400">Loading inventory…</p>
        ) : (
          <div className="space-y-2">
            {rows.map((row, i) => (
              <div key={i} className="flex items-center gap-2">
                <select
                  value={row.inventory_item_id}
                  onChange={(e) => updateRow(i, 'inventory_item_id', e.target.value)}
                  className="flex-1 rounded-md border border-gray-300 px-2 py-1.5 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
                >
                  <option value="">— select item —</option>
                  {inventory.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.name} ({item.sku}) · {item.quantity_on_hand} {item.unit} available
                    </option>
                  ))}
                </select>
                <input
                  type="number"
                  min={1}
                  value={row.quantity}
                  onChange={(e) => updateRow(i, 'quantity', e.target.value)}
                  className="w-20 rounded-md border border-gray-300 px-2 py-1.5 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
                />
                <button
                  onClick={() => removeRow(i)}
                  className="text-gray-400 hover:text-red-500"
                  title="Remove row"
                >
                  ✕
                </button>
              </div>
            ))}
            <button
              onClick={addRow}
              className="mt-1 text-sm text-blue-600 hover:underline"
            >
              + Add item
            </button>
          </div>
        )}

        <div className="mt-5 flex justify-end gap-2">
          <button
            onClick={onCancel}
            className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            onClick={handleConfirm}
            className="rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700"
          >
            Confirm Complete
          </button>
        </div>
      </div>
    </div>
  )
}

function Field({ label, value }) {
  return (
    <div>
      <dt className="text-xs font-semibold uppercase tracking-wider text-gray-400">{label}</dt>
      <dd className="mt-1 text-sm text-gray-900">{value}</dd>
    </div>
  )
}
