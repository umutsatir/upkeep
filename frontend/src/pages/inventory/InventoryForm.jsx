// OWNER: MEMBER-4
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getById, create, update } from '../../api/inventory.js'
import PageHeader from '../../components/PageHeader.jsx'

const UNIT_OPTIONS = ['pcs', 'litres', 'metres', 'kg']

const INITIAL_FORM = {
  name: '',
  sku: '',
  category: '',
  quantity_on_hand: 0,
  low_stock_threshold: 5,
  unit_cost: 0,
  unit: 'pcs',
  supplier: '',
  location: '',
  notes: '',
}

export default function InventoryForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  const [form, setForm] = useState(INITIAL_FORM)
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(isEdit)
  const [error, setError] = useState(null)
  const [fieldErrors, setFieldErrors] = useState({})

  useEffect(() => {
    if (!isEdit) return
    setFetching(true)
    getById(id)
      .then((data) => {
        setForm({
          name: data.name ?? '',
          sku: data.sku ?? '',
          category: data.category ?? '',
          quantity_on_hand: data.quantity_on_hand ?? 0,
          low_stock_threshold: data.low_stock_threshold ?? 5,
          unit_cost: data.unit_cost ?? 0,
          unit: data.unit ?? 'pcs',
          supplier: data.supplier ?? '',
          location: data.location ?? '',
          notes: data.notes ?? '',
        })
      })
      .catch((err) => setError(err.message))
      .finally(() => setFetching(false))
  }, [id, isEdit])

  const handleChange = (e) => {
    const { name, value, type } = e.target
    setForm((prev) => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? '' : Number(value)) : value,
    }))
    // Clear field-level error on change
    if (fieldErrors[name]) {
      setFieldErrors((prev) => {
        const next = { ...prev }
        delete next[name]
        return next
      })
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setFieldErrors({})

    try {
      const payload = { ...form }
      if (isEdit) {
        await update(id, payload)
      } else {
        await create(payload)
      }
      navigate('/inventory')
    } catch (err) {
      if (err.response?.status === 422) {
        const data = err.response.data
        // Handle validation errors — could be { errors: { field: [msg] } } or { message: '...' }
        if (data?.errors) {
          const mapped = {}
          for (const [key, msgs] of Object.entries(data.errors)) {
            mapped[key] = Array.isArray(msgs) ? msgs.join(', ') : String(msgs)
          }
          setFieldErrors(mapped)
        } else {
          setError(data?.message || 'Validation failed. Please check your inputs.')
        }
      } else {
        setError(err.response?.data?.message || err.message)
      }
    } finally {
      setLoading(false)
    }
  }

  if (fetching) {
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

  const inputClass = (name) =>
    `block w-full rounded-md border px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-1 ${
      fieldErrors[name]
        ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
        : 'border-gray-300 focus:border-brand-600 focus:ring-brand-600'
    }`

  return (
    <div>
      <PageHeader
        title={isEdit ? 'Edit Item' : 'New Inventory Item'}
        subtitle={isEdit ? `Editing item #${id}` : 'Add a new spare part or consumable.'}
      />

      {error && (
        <div className="mb-6 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <div className="grid grid-cols-1 gap-x-6 gap-y-5 sm:grid-cols-2 lg:grid-cols-3">
          {/* Name */}
          <div>
            <label htmlFor="name" className="mb-1 block text-sm font-medium text-gray-700">
              Name <span className="text-red-500">*</span>
            </label>
            <input id="name" name="name" type="text" required value={form.name} onChange={handleChange} className={inputClass('name')} />
            {fieldErrors.name && <p className="mt-1 text-xs text-red-600">{fieldErrors.name}</p>}
          </div>

          {/* SKU */}
          <div>
            <label htmlFor="sku" className="mb-1 block text-sm font-medium text-gray-700">
              SKU <span className="text-red-500">*</span>
            </label>
            <input id="sku" name="sku" type="text" required value={form.sku} onChange={handleChange} className={inputClass('sku')} />
            {fieldErrors.sku && <p className="mt-1 text-xs text-red-600">{fieldErrors.sku}</p>}
          </div>

          {/* Category */}
          <div>
            <label htmlFor="category" className="mb-1 block text-sm font-medium text-gray-700">
              Category <span className="text-red-500">*</span>
            </label>
            <input id="category" name="category" type="text" required value={form.category} onChange={handleChange} className={inputClass('category')} />
            {fieldErrors.category && <p className="mt-1 text-xs text-red-600">{fieldErrors.category}</p>}
          </div>

          {/* Quantity on Hand */}
          <div>
            <label htmlFor="quantity_on_hand" className="mb-1 block text-sm font-medium text-gray-700">
              Quantity on Hand <span className="text-red-500">*</span>
            </label>
            <input id="quantity_on_hand" name="quantity_on_hand" type="number" min="0" required value={form.quantity_on_hand} onChange={handleChange} className={inputClass('quantity_on_hand')} />
            {fieldErrors.quantity_on_hand && <p className="mt-1 text-xs text-red-600">{fieldErrors.quantity_on_hand}</p>}
          </div>

          {/* Low Stock Threshold */}
          <div>
            <label htmlFor="low_stock_threshold" className="mb-1 block text-sm font-medium text-gray-700">
              Low Stock Threshold <span className="text-red-500">*</span>
            </label>
            <input id="low_stock_threshold" name="low_stock_threshold" type="number" min="0" required value={form.low_stock_threshold} onChange={handleChange} className={inputClass('low_stock_threshold')} />
            {fieldErrors.low_stock_threshold && <p className="mt-1 text-xs text-red-600">{fieldErrors.low_stock_threshold}</p>}
          </div>

          {/* Unit Cost */}
          <div>
            <label htmlFor="unit_cost" className="mb-1 block text-sm font-medium text-gray-700">
              Unit Cost ($) <span className="text-red-500">*</span>
            </label>
            <input id="unit_cost" name="unit_cost" type="number" step="0.01" min="0" required value={form.unit_cost} onChange={handleChange} className={inputClass('unit_cost')} />
            {fieldErrors.unit_cost && <p className="mt-1 text-xs text-red-600">{fieldErrors.unit_cost}</p>}
          </div>

          {/* Unit */}
          <div>
            <label htmlFor="unit" className="mb-1 block text-sm font-medium text-gray-700">
              Unit
            </label>
            <select id="unit" name="unit" value={form.unit} onChange={handleChange} className={inputClass('unit')}>
              {UNIT_OPTIONS.map((u) => (
                <option key={u} value={u}>
                  {u}
                </option>
              ))}
            </select>
            {fieldErrors.unit && <p className="mt-1 text-xs text-red-600">{fieldErrors.unit}</p>}
          </div>

          {/* Supplier */}
          <div>
            <label htmlFor="supplier" className="mb-1 block text-sm font-medium text-gray-700">
              Supplier
            </label>
            <input id="supplier" name="supplier" type="text" value={form.supplier} onChange={handleChange} className={inputClass('supplier')} />
            {fieldErrors.supplier && <p className="mt-1 text-xs text-red-600">{fieldErrors.supplier}</p>}
          </div>

          {/* Location */}
          <div>
            <label htmlFor="location" className="mb-1 block text-sm font-medium text-gray-700">
              Location
            </label>
            <input id="location" name="location" type="text" value={form.location} onChange={handleChange} className={inputClass('location')} />
            {fieldErrors.location && <p className="mt-1 text-xs text-red-600">{fieldErrors.location}</p>}
          </div>

          {/* Notes — full width */}
          <div className="sm:col-span-2 lg:col-span-3">
            <label htmlFor="notes" className="mb-1 block text-sm font-medium text-gray-700">
              Notes
            </label>
            <textarea id="notes" name="notes" rows={3} value={form.notes} onChange={handleChange} className={inputClass('notes')} />
            {fieldErrors.notes && <p className="mt-1 text-xs text-red-600">{fieldErrors.notes}</p>}
          </div>
        </div>

        {/* Form Actions */}
        <div className="mt-6 flex items-center gap-3 border-t border-gray-200 pt-5">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center rounded-md bg-brand-600 px-5 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700 disabled:opacity-50"
          >
            {loading ? 'Saving…' : isEdit ? 'Update Item' : 'Create Item'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/inventory')}
            className="rounded-md border border-gray-300 bg-white px-5 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}
