// OWNER: MEMBER-3
import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'
import Table from '../../components/Table.jsx'
import StatusBadge from '../../components/StatusBadge.jsx'
import Pagination from '../../components/Pagination.jsx'
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
  const [schedules, setSchedules]   = useState([])
  const [loading, setLoading]       = useState(true)
  const [error, setError]           = useState(null)
  const [notice, setNotice]         = useState(null)
  const [search, setSearch]         = useState('')
  const [triggerFilter, setTrigger] = useState('')
  const [activeFilter, setActive]   = useState('')
  const [page, setPage]             = useState(1)
  const [pageSize, setPageSize]     = useState(20)

  useEffect(() => {
    setLoading(true)
    setError(null)
    getAll()
      .then(setSchedules)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return schedules.filter((s) => {
      if (q && !s.title.toLowerCase().includes(q)) return false
      if (triggerFilter && s.trigger_type !== triggerFilter) return false
      if (activeFilter === 'active' && !s.is_active) return false
      if (activeFilter === 'inactive' && s.is_active) return false
      return true
    })
  }, [schedules, search, triggerFilter, activeFilter])

  useEffect(() => { setPage(1) }, [filtered])

  const paginated = useMemo(
    () => filtered.slice((page - 1) * pageSize, page * pageSize),
    [filtered, page, pageSize],
  )

  const hasFilters = search || triggerFilter || activeFilter

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

      <div className="mb-4 flex flex-wrap gap-2">
        <input
          type="search"
          placeholder="Search by title…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-56 rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
        />
        <select
          value={triggerFilter}
          onChange={(e) => setTrigger(e.target.value)}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
        >
          <option value="">All trigger types</option>
          <option value="time_based">Time based</option>
          <option value="usage_based">Usage based</option>
        </select>
        <select
          value={activeFilter}
          onChange={(e) => setActive(e.target.value)}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
        >
          <option value="">Active &amp; inactive</option>
          <option value="active">Active only</option>
          <option value="inactive">Inactive only</option>
        </select>
        {hasFilters && (
          <button
            onClick={() => { setSearch(''); setTrigger(''); setActive(''); setPage(1) }}
            className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50"
          >
            Clear
          </button>
        )}
        {!loading && (
          <span className="ml-auto self-center text-xs text-gray-400">
            {filtered.length} of {schedules.length}
          </span>
        )}
      </div>

      <Table columns={COLUMNS} data={paginated} loading={loading} error={error} />
      {!loading && (
        <Pagination
          total={filtered.length}
          page={page}
          pageSize={pageSize}
          onPage={setPage}
          onPageSize={(s) => { setPageSize(s); setPage(1) }}
        />
      )}
    </div>
  )
}
