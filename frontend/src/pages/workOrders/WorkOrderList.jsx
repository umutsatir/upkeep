// OWNER: MEMBER-1
import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { getAll } from '../../api/workOrders.js'
import Table from '../../components/Table.jsx'
import StatusBadge from '../../components/StatusBadge.jsx'
import PageHeader from '../../components/PageHeader.jsx'
import Pagination from '../../components/Pagination.jsx'

const STATUSES  = ['open', 'assigned', 'in_progress', 'completed', 'closed', 'cancelled']
const PRIORITIES = ['low', 'medium', 'high', 'critical']

const COLUMNS = [
  { key: 'title', header: 'Title' },
  {
    key: 'status',
    header: 'Status',
    render: (val) => <StatusBadge value={val} />,
  },
  {
    key: 'priority',
    header: 'Priority',
    render: (val) => <StatusBadge value={val} />,
  },
  {
    key: 'due_date',
    header: 'Due Date',
    render: (val) => val ? new Date(val).toLocaleDateString() : '—',
  },
  {
    key: 'id',
    header: 'Actions',
    render: (val) => (
      <Link
        to={`/work-orders/${val}`}
        className="text-brand-600 hover:text-brand-800 text-xs font-medium underline underline-offset-2"
      >
        View
      </Link>
    ),
  },
]

export default function WorkOrderList() {
  const [workOrders, setWorkOrders] = useState([])
  const [loading, setLoading]       = useState(true)
  const [error, setError]           = useState(null)
  const [search, setSearch]           = useState('')
  const [statusFilter, setStatus]     = useState('')
  const [priorityFilter, setPriority] = useState('')
  const [page, setPage]               = useState(1)
  const [pageSize, setPageSize]       = useState(20)

  useEffect(() => {
    setLoading(true)
    setError(null)
    getAll()
      .then(setWorkOrders)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return workOrders.filter((wo) => {
      if (q && !wo.title.toLowerCase().includes(q)) return false
      if (statusFilter && wo.status !== statusFilter) return false
      if (priorityFilter && wo.priority !== priorityFilter) return false
      return true
    })
  }, [workOrders, search, statusFilter, priorityFilter])

  useEffect(() => { setPage(1) }, [filtered])

  const paginated = useMemo(
    () => filtered.slice((page - 1) * pageSize, page * pageSize),
    [filtered, page, pageSize],
  )

  const hasFilters = search || statusFilter || priorityFilter

  return (
    <div>
      <PageHeader
        title="Work Orders"
        subtitle="Track and manage all maintenance tasks."
        action={
          <Link
            to="/work-orders/new"
            className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500"
          >
            + New Work Order
          </Link>
        }
      />

      <div className="mb-4 flex flex-wrap gap-2">
        <input
          type="search"
          placeholder="Search by title…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-56 rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatus(e.target.value)}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
        >
          <option value="">All statuses</option>
          {STATUSES.map((s) => (
            <option key={s} value={s}>{s.replace('_', ' ')}</option>
          ))}
        </select>
        <select
          value={priorityFilter}
          onChange={(e) => setPriority(e.target.value)}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
        >
          <option value="">All priorities</option>
          {PRIORITIES.map((p) => (
            <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
          ))}
        </select>
        {hasFilters && (
          <button
            onClick={() => { setSearch(''); setStatus(''); setPriority(''); setPage(1) }}
            className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50"
          >
            Clear
          </button>
        )}
        {!loading && (
          <span className="ml-auto self-center text-xs text-gray-400">
            {filtered.length} of {workOrders.length}
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
