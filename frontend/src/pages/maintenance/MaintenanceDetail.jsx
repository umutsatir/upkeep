// OWNER: MEMBER-3
import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'
import { getById } from '../../api/maintenance.js'
import { getById as getAssetById } from '../../api/assets.js'

function renderRow(label, value) {
  return (
    <div className="grid grid-cols-3 gap-4 py-2 border-b border-gray-200 text-sm">
      <div className="font-medium text-gray-700">{label}</div>
      <div className="col-span-2 text-gray-800">{value ?? '—'}</div>
    </div>
  )
}

export default function MaintenanceDetail() {
  const { id } = useParams()
  const [schedule, setSchedule] = useState(null)
  const [assetName, setAssetName] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    getById(id)
      .then((s) => {
        setSchedule(s)
        if (s.asset_id) {
          getAssetById(s.asset_id)
            .then((a) => setAssetName(a.name))
            .catch(() => {})
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  const subtitle = schedule ? schedule.title : id

  return (
    <div>
      <PageHeader title="Schedule Detail" subtitle={subtitle} backTo="/maintenance" />

      {loading ? (
        <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
          Loading…
        </div>
      ) : error ? (
        <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-700">
          {error}
        </div>
      ) : (
        <div className="space-y-6">
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            {renderRow('Asset', (
              <Link
                to={`/assets/${schedule.asset_id}`}
                className="text-brand-600 hover:text-brand-800 underline"
              >
                {assetName ?? schedule.asset_id}
              </Link>
            ))}
            {renderRow('Title', schedule.title)}
            {renderRow('Description', schedule.description)}
            {renderRow('Trigger Type', schedule.trigger_type)}
            {renderRow('Interval Days', schedule.interval_days ? `${schedule.interval_days} days` : '—')}
            {renderRow('Usage Threshold', schedule.usage_threshold_hours ? `${schedule.usage_threshold_hours} hrs` : '—')}
            {renderRow('Current Usage', schedule.current_usage_hours ? `${schedule.current_usage_hours} hrs` : '—')}
            {renderRow('Next Due', schedule.next_due_at ? new Date(schedule.next_due_at).toLocaleString() : '—')}
            {renderRow('Last Triggered', schedule.last_triggered_at ? new Date(schedule.last_triggered_at).toLocaleString() : '—')}
            {renderRow('Priority', schedule.generated_wo_priority)}
            {renderRow('Assigned To', schedule.assigned_to ?? '—')}
            {renderRow('Active', schedule.is_active ? 'Yes' : 'No')}
          </div>

          <div className="flex flex-wrap gap-3">
            <Link
              to="/maintenance"
              className="inline-flex items-center gap-1.5 rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Back to schedules
            </Link>
            <Link
              to={`/maintenance/${id}/edit`}
              className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
            >
              Edit schedule
            </Link>
          </div>
        </div>
      )}
    </div>
  )
}
