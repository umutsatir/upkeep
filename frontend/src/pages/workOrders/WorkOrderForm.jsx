// OWNER: MEMBER-1
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { create, getById, update } from '../../api/workOrders.js'
import PageHeader from '../../components/PageHeader.jsx'

const PRIORITIES = ['low', 'medium', 'high', 'critical']

const EMPTY = {
  title: '',
  description: '',
  asset_id: '',
  priority: 'medium',
  due_date: '',
  notes: '',
}

export default function WorkOrderForm() {
  const { id }   = useParams()
  const navigate = useNavigate()
  const isEdit   = Boolean(id)

  const [form, setForm]       = useState(EMPTY)
  const [error, setError]     = useState(null)
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(isEdit)

  // Pre-fill form when editing
  useEffect(() => {
    if (!isEdit) return
    getById(id)
      .then((wo) => {
        setForm({
          title:       wo.title,
          description: wo.description,
          asset_id:    wo.asset_id,
          priority:    wo.priority,
          due_date:    wo.due_date ? wo.due_date.slice(0, 10) : '',
          notes:       wo.notes ?? '',
        })
      })
      .catch((err) => setError(err.message))
      .finally(() => setFetching(false))
  }, [id, isEdit])

  function set(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const payload = {
        ...form,
        due_date: form.due_date ? new Date(form.due_date).toISOString() : null,
      }
      if (isEdit) {
        await update(id, payload)
      } else {
        await create(payload)
      }
      navigate('/work-orders')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (fetching) {
    return <p className="py-8 text-center text-gray-400">Loading…</p>
  }

  return (
    <div className="mx-auto max-w-2xl">
      <PageHeader title={isEdit ? 'Edit Work Order' : 'New Work Order'} />

      {error && (
        <div className="mb-4 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        className="space-y-5 rounded-lg border border-gray-200 bg-white p-4 shadow-sm sm:p-6"
      >
        <Field label="Title" required>
          <input
            type="text"
            required
            value={form.title}
            onChange={set('title')}
            className={inputCls}
          />
        </Field>

        <Field label="Description" required>
          <textarea
            required
            rows={3}
            value={form.description}
            onChange={set('description')}
            className={inputCls}
          />
        </Field>

        <Field label="Asset ID" required hint="Will be a dropdown once Assets module is merged (M2)">
          <input
            type="text"
            required
            value={form.asset_id}
            onChange={set('asset_id')}
            placeholder="e.g. 507f1f77bcf86cd799439011"
            className={inputCls}
          />
        </Field>

        <Field label="Priority">
          <select value={form.priority} onChange={set('priority')} className={inputCls}>
            {PRIORITIES.map((p) => (
              <option key={p} value={p} className="capitalize">
                {p.charAt(0).toUpperCase() + p.slice(1)}
              </option>
            ))}
          </select>
        </Field>

        <Field label="Due Date">
          <input
            type="date"
            value={form.due_date}
            onChange={set('due_date')}
            className={inputCls}
          />
        </Field>

        <Field label="Notes">
          <textarea
            rows={2}
            value={form.notes}
            onChange={set('notes')}
            className={inputCls}
          />
        </Field>

        <div className="flex flex-col-reverse gap-3 border-t pt-4 sm:flex-row sm:justify-end">
          <button
            type="button"
            onClick={() => navigate('/work-orders')}
            className="w-full rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 sm:w-auto"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50 sm:w-auto"
          >
            {loading ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Work Order'}
          </button>
        </div>
      </form>
    </div>
  )
}

const inputCls =
  'mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500'

function Field({ label, children, required = false, hint }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700">
        {label}
        {required && <span className="ml-0.5 text-red-500">*</span>}
      </label>
      {hint && <p className="text-xs text-gray-400">{hint}</p>}
      {children}
    </div>
  )
}
