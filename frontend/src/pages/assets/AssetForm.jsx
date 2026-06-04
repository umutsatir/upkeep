// OWNER: MEMBER-2
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { create, getById, update } from '../../api/assets.js'
import PageHeader from '../../components/PageHeader.jsx'

const STATUSES = ['active', 'inactive', 'under_maintenance', 'decommissioned']

const EMPTY = {
  name: '',
  asset_tag: '',
  category: '',
  location: '',
  status: 'active',
  purchase_date: '',
  warranty_expires_at: '',
  model_number: '',
  serial_number: '',
  notes: '',
}

export default function AssetForm() {
  const { id }   = useParams()
  const navigate = useNavigate()
  const isEdit   = Boolean(id)

  const [form, setForm]         = useState(EMPTY)
  const [error, setError]       = useState(null)
  const [loading, setLoading]   = useState(false)
  const [fetching, setFetching] = useState(isEdit)

  // Pre-fill form when editing
  useEffect(() => {
    if (!isEdit) return
    getById(id)
      .then((asset) => {
        setForm({
          name:                asset.name,
          asset_tag:           asset.asset_tag,
          category:            asset.category,
          location:            asset.location || '',
          status:              asset.status,
          purchase_date:       asset.purchase_date ? asset.purchase_date.slice(0, 10) : '',
          warranty_expires_at: asset.warranty_expires_at ? asset.warranty_expires_at.slice(0, 10) : '',
          model_number:        asset.model_number || '',
          serial_number:       asset.serial_number || '',
          notes:               asset.notes || '',
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
      // Clean up empty strings to null for the backend
      const payload = {
        name: form.name,
        asset_tag: form.asset_tag,
        category: form.category,
        location: form.location || null,
        purchase_date: form.purchase_date ? new Date(form.purchase_date).toISOString() : null,
        warranty_expires_at: form.warranty_expires_at ? new Date(form.warranty_expires_at).toISOString() : null,
        model_number: form.model_number || null,
        serial_number: form.serial_number || null,
        notes: form.notes,
      }

      if (isEdit) {
        payload.status = form.status // Status can only be changed on update
        await update(id, payload)
      } else {
        await create(payload)
      }
      navigate('/assets')
    } catch (err) {
      // e.g. duplicate asset tag 409 conflict
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
      <PageHeader title={isEdit ? 'Edit Asset' : 'New Asset'} />

      {error && (
        <div className="mb-4 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        className="space-y-5 rounded-lg border border-gray-200 bg-white p-4 shadow-sm sm:p-6"
      >
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
          <Field label="Name" required>
            <input type="text" required value={form.name} onChange={set('name')} className={inputCls} placeholder="e.g. Main HVAC Unit" />
          </Field>

          <Field label="Asset Tag (Unique)" required>
            <input type="text" required value={form.asset_tag} onChange={set('asset_tag')} className={inputCls} placeholder="e.g. HVAC-001" />
          </Field>
        </div>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
          <Field label="Category" required>
            <input type="text" required value={form.category} onChange={set('category')} className={inputCls} placeholder="e.g. Electrical" />
          </Field>

          <Field label="Location">
            <input type="text" value={form.location} onChange={set('location')} className={inputCls} placeholder="e.g. Roof - Sector A" />
          </Field>
        </div>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
          <Field label="Model Number">
            <input type="text" value={form.model_number} onChange={set('model_number')} className={inputCls} />
          </Field>

          <Field label="Serial Number">
            <input type="text" value={form.serial_number} onChange={set('serial_number')} className={inputCls} />
          </Field>
        </div>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
          <Field label="Purchase Date">
            <input type="date" value={form.purchase_date} onChange={set('purchase_date')} className={inputCls} />
          </Field>

          <Field label="Warranty Expiry">
            <input type="date" value={form.warranty_expires_at} onChange={set('warranty_expires_at')} className={inputCls} />
          </Field>
        </div>

        {isEdit && (
          <Field label="Status">
            <select value={form.status} onChange={set('status')} className={inputCls}>
              {STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
          </Field>
        )}

        <Field label="Notes">
          <textarea rows={3} value={form.notes} onChange={set('notes')} className={inputCls} />
        </Field>

        <div className="flex flex-col-reverse gap-3 border-t pt-4 sm:flex-row sm:justify-end">
          <button
            type="button"
            onClick={() => navigate('/assets')}
            className="w-full rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 sm:w-auto"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50 sm:w-auto"
          >
            {loading ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Asset'}
          </button>
        </div>
      </form>
    </div>
  )
}

const inputCls =
  'mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500'

function Field({ label, children, required = false }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700">
        {label}
        {required && <span className="ml-0.5 text-red-500">*</span>}
      </label>
      {children}
    </div>
  )
}
