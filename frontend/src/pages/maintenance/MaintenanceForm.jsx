// OWNER: MEMBER-3
import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'
import { getById, create, update } from '../../api/maintenance.js'
import { getAll as getAssets } from '../../api/assets.js'

const PRIORITIES = ['low', 'medium', 'high', 'critical']

export default function MaintenanceForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  const [form, setForm] = useState({
    asset_id: '',
    title: '',
    description: '',
    trigger_type: 'time_based',
    interval_days: 30,
    usage_threshold_hours: '',
    current_usage_hours: '',
    generated_wo_priority: 'medium',
    assigned_to: '',
  })
  const [assets, setAssets] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(null)

    Promise.all([getAssets(), id ? getById(id) : Promise.resolve(null)])
      .then(([assetList, schedule]) => {
        setAssets(assetList)
        if (schedule) {
          setForm({
            asset_id: schedule.asset_id,
            title: schedule.title,
            description: schedule.description,
            trigger_type: schedule.trigger_type,
            interval_days: schedule.interval_days ?? 30,
            usage_threshold_hours: schedule.usage_threshold_hours ?? '',
            current_usage_hours: schedule.current_usage_hours ?? '',
            generated_wo_priority: schedule.generated_wo_priority,
            assigned_to: schedule.assigned_to ?? '',
          })
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSaving(true)
    setError(null)

    try {
      const payload = {
        ...form,
        interval_days: form.interval_days ? Number(form.interval_days) : null,
        usage_threshold_hours: form.usage_threshold_hours ? Number(form.usage_threshold_hours) : null,
        current_usage_hours: form.current_usage_hours ? Number(form.current_usage_hours) : null,
        assigned_to: form.assigned_to || null,
      }

      if (isEdit) {
        await update(id, payload)
      } else {
        await create(payload)
      }
      navigate('/maintenance')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <PageHeader title={isEdit ? 'Edit Schedule' : 'New Schedule'} />

      {loading ? (
        <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
          Loading…
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          {error && (
            <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          )}

          <div className="grid gap-4 sm:grid-cols-2">
            <label className="block">
              <span className="text-sm font-medium text-gray-700">Asset</span>
              <select
                name="asset_id"
                value={form.asset_id}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500"
                required
              >
                <option value="">Select an asset</option>
                {assets.map((asset) => (
                  <option key={asset.id} value={asset.id}>
                    {asset.asset_tag} — {asset.name}
                  </option>
                ))}
              </select>
            </label>

            <label className="block">
              <span className="text-sm font-medium text-gray-700">Priority</span>
              <select
                name="generated_wo_priority"
                value={form.generated_wo_priority}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500"
              >
                {PRIORITIES.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <label className="block sm:col-span-2">
              <span className="text-sm font-medium text-gray-700">Title</span>
              <input
                name="title"
                value={form.title}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500"
                required
              />
            </label>

            <label className="block sm:col-span-2">
              <span className="text-sm font-medium text-gray-700">Description</span>
              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500"
                rows={4}
                required
              />
            </label>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <fieldset className="sm:col-span-2">
              <legend className="text-sm font-medium text-gray-700">Trigger type</legend>
              <div className="mt-3 flex flex-wrap gap-4">
                <label className="inline-flex items-center gap-2">
                  <input
                    type="radio"
                    name="trigger_type"
                    value="time_based"
                    checked={form.trigger_type === 'time_based'}
                    onChange={handleChange}
                    className="h-4 w-4"
                  />
                  <span>Time-based</span>
                </label>
                <label className="inline-flex items-center gap-2">
                  <input
                    type="radio"
                    name="trigger_type"
                    value="usage_based"
                    checked={form.trigger_type === 'usage_based'}
                    onChange={handleChange}
                    className="h-4 w-4"
                  />
                  <span>Usage-based</span>
                </label>
              </div>
            </fieldset>

            {form.trigger_type === 'time_based' && (
              <label className="block">
                <span className="text-sm font-medium text-gray-700">Interval (days)</span>
                <input
                  type="number"
                  name="interval_days"
                  min="1"
                  value={form.interval_days}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500"
                />
              </label>
            )}

            {form.trigger_type === 'usage_based' && (
              <>
                <label className="block">
                  <span className="text-sm font-medium text-gray-700">Usage threshold (hours)</span>
                  <input
                    type="number"
                    name="usage_threshold_hours"
                    min="1"
                    value={form.usage_threshold_hours}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500"
                  />
                </label>

                <label className="block">
                  <span className="text-sm font-medium text-gray-700">Current usage (hours)</span>
                  <input
                    type="number"
                    name="current_usage_hours"
                    min="0"
                    value={form.current_usage_hours}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500"
                  />
                </label>
              </>
            )}
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <label className="block">
              <span className="text-sm font-medium text-gray-700">Default assignee</span>
              <input
                name="assigned_to"
                value={form.assigned_to}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500"
                placeholder="User ID"
              />
            </label>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              type="submit"
              disabled={saving}
              className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isEdit ? 'Save changes' : 'Create schedule'}
            </button>
            <Link
              to="/maintenance"
              className="inline-flex items-center gap-1.5 rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </Link>
          </div>
        </form>
      )}
    </div>
  )
}
