// OWNER: MEMBER-2
import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { getAll } from '../../api/assets.js'
import Table from '../../components/Table.jsx'
import StatusBadge from '../../components/StatusBadge.jsx'
import PageHeader from '../../components/PageHeader.jsx'
import Pagination from '../../components/Pagination.jsx'

const STATUSES = ['active', 'inactive', 'under_maintenance', 'decommissioned']

const COLUMNS = [
  { key: 'name', header: 'Name' },
  {
    key: 'asset_tag',
    header: 'Tag',
    render: (val) => <code className="rounded bg-gray-100 px-1.5 py-0.5 text-xs text-gray-800">{val}</code>,
  },
  { key: 'category', header: 'Category' },
  { key: 'location', header: 'Location', render: (val) => val || '—' },
  {
    key: 'status',
    header: 'Status',
    render: (val) => <StatusBadge value={val} />,
  },
  {
    key: 'id',
    header: 'Actions',
    render: (val) => (
      <Link
        to={`/assets/${val}`}
        className="text-brand-600 hover:text-brand-800 text-xs font-medium underline underline-offset-2"
      >
        View
      </Link>
    ),
  },
]

export default function AssetList() {
  const [assets, setAssets]         = useState([])
  const [loading, setLoading]       = useState(true)
  const [error, setError]           = useState(null)
  const [search, setSearch]           = useState('')
  const [statusFilter, setStatus]     = useState('')
  const [categoryFilter, setCategory] = useState('')
  const [page, setPage]               = useState(1)
  const [pageSize, setPageSize]       = useState(20)

  useEffect(() => {
    setLoading(true)
    setError(null)
    getAll()
      .then(setAssets)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const categories = useMemo(
    () => [...new Set(assets.map((a) => a.category).filter(Boolean))].sort(),
    [assets],
  )

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return assets.filter((a) => {
      if (q && !a.name.toLowerCase().includes(q) && !(a.asset_tag ?? '').toLowerCase().includes(q)) return false
      if (statusFilter && a.status !== statusFilter) return false
      if (categoryFilter && a.category !== categoryFilter) return false
      return true
    })
  }, [assets, search, statusFilter, categoryFilter])

  useEffect(() => { setPage(1) }, [filtered])

  const paginated = useMemo(
    () => filtered.slice((page - 1) * pageSize, page * pageSize),
    [filtered, page, pageSize],
  )

  const hasFilters = search || statusFilter || categoryFilter

  return (
    <div>
      <PageHeader
        title="Assets"
        subtitle="Track equipment, machinery, and infrastructure."
        action={
          <Link
            to="/assets/new"
            className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500"
          >
            + Add Asset
          </Link>
        }
      />

      <div className="mb-4 flex flex-wrap gap-2">
        <input
          type="search"
          placeholder="Search by name or tag…"
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
          value={categoryFilter}
          onChange={(e) => setCategory(e.target.value)}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
        >
          <option value="">All categories</option>
          {categories.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        {hasFilters && (
          <button
            onClick={() => { setSearch(''); setStatus(''); setCategory(''); setPage(1) }}
            className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50"
          >
            Clear
          </button>
        )}
        {!loading && (
          <span className="ml-auto self-center text-xs text-gray-400">
            {filtered.length} of {assets.length}
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
