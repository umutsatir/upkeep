// OWNER: MEMBER-3
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'
import Table from '../../components/Table.jsx'
import StatusBadge from '../../components/StatusBadge.jsx'
import { getAll, evaluateDue } from '../../api/maintenance.js'

const COLUMNS = [
  { key: 'title', header: 'Title' },
  {
    key: 'asset_id',
    header: 'Asset',
    render: (val) => val || '—',
  },
  {
    key: 'trigger_type',
    header: 'Trigger',
    render: (val) => <StatusBadge value={val} />,
  },
  {
    key: 'interval_days',
    header: 'Interval',
    render: (val, row) => (row.trigger_type === 'time_based' ? `${val ?? '—'} days` : '—'),
  },
  {
    key: 'usage_threshold_hours',
    header: 'Usage Threshold',
    render: (val, row) => (row.trigger_type === 'usage_based' ? `${val ?? '—'} hrs` : '—'),
  },
  {
    key: 'next_due_at',
    header: 'Next Due',
    render: (val) => (val ? new Date(val).toLocaleDateString() : '—'),
  },
  {
    key: 'is_active',
    header: 'Active',
    render: (val) => <StatusBadge value={val ? 'active' : 'inactive'} />,
  },
  {
    key: 'id',
    header: 'Actions',
    render: (val) => (
      <Link
        to={`/maintenance/${val}`}
        className="text-brand-600 hover:text-brand-800 text-xs font-medium underline underline-offset-2"
      >
        View
      </Link>
    ),
  },
]

export default function MaintenanceList() {
  const [schedules, setSchedules] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [notice, setNotice] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    getAll()
      .then(setSchedules)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const onEvaluate = async () => {
    setNotice(null)
    setError(null)
    try {
      const result = await evaluateDue()
      setNotice(`${result.generated_work_orders.length} work order(s) generated.`)
      const refreshed = await getAll()
      setSchedules(refreshed)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <PageHeader
        title="Preventive Maintenance"
        subtitle="Manage recurring maintenance schedules."
        action={
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={onEvaluate}
              className="inline-flex items-center gap-1.5 rounded-md border border-brand-600 bg-white px-4 py-2 text-sm font-medium text-brand-600 shadow-sm hover:bg-brand-50"
            >
              Evaluate Due
            </button>
            <Link
              to="/maintenance/new"
              className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700"
            >
              + New Schedule
            </Link>
          </div>
        }
      />

      {notice && (
        <div className="mb-4 rounded-md border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
          {notice}
        </div>
      )}

      <Table columns={COLUMNS} data={schedules} loading={loading} error={error} />
    </div>
  )
}
