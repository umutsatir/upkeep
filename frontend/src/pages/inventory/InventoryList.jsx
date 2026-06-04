// OWNER: MEMBER-4
import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { getAll, getLowStock } from '../../api/inventory.js'
import Table from '../../components/Table.jsx'
import PageHeader from '../../components/PageHeader.jsx'
import Pagination from '../../components/Pagination.jsx'

const COLUMNS = [
  { key: 'name', header: 'Name' },
  { key: 'sku', header: 'SKU' },
  { key: 'category', header: 'Category' },
  {
    key: 'quantity_on_hand',
    header: 'Qty on Hand',
    render: (val, row) => {
      const isLow = val <= (row.low_stock_threshold ?? 0)
      return (
        <span className={isLow ? 'font-semibold text-red-600' : ''}>
          {val}
          {isLow && (
            <span className="ml-1.5 inline-flex items-center rounded-full bg-red-100 px-2 py-0.5 text-xs text-red-700">
              Low
            </span>
          )}
        </span>
      )
    },
  },
  {
    key: 'unit_cost',
    header: 'Unit Cost',
    render: (val) =>
      val != null
        ? new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val)
        : '—',
  },
  { key: 'unit', header: 'Unit' },
  {
    key: 'id',
    header: 'Actions',
    render: (val) => (
      <Link
        to={`/inventory/${val}`}
        className="text-brand-600 hover:text-brand-800 text-xs font-medium underline underline-offset-2"
      >
        View
      </Link>
    ),
  },
]

export default function InventoryList() {
  const [items, setItems]           = useState([])
  const [loading, setLoading]       = useState(true)
  const [error, setError]           = useState(null)
  const [lowStockOnly, setLowStockOnly] = useState(false)
  const [search, setSearch]             = useState('')
  const [categoryFilter, setCategory]   = useState('')
  const [page, setPage]                 = useState(1)
  const [pageSize, setPageSize]         = useState(20)

  useEffect(() => {
    setLoading(true)
    setError(null)
    const fetcher = lowStockOnly ? getLowStock : getAll
    fetcher()
      .then(setItems)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [lowStockOnly])

  const categories = useMemo(
    () => [...new Set(items.map((i) => i.category).filter(Boolean))].sort(),
    [items],
  )

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return items.filter((item) => {
      if (q && !item.name.toLowerCase().includes(q) && !(item.sku ?? '').toLowerCase().includes(q)) return false
      if (categoryFilter && item.category !== categoryFilter) return false
      return true
    })
  }, [items, search, categoryFilter])

  useEffect(() => { setPage(1) }, [filtered])

  const paginated = useMemo(
    () => filtered.slice((page - 1) * pageSize, page * pageSize),
    [filtered, page, pageSize],
  )

  const hasFilters = search || categoryFilter

  return (
    <div>
      <PageHeader
        title="Inventory"
        subtitle="Manage spare parts and consumables."
        action={
          <div className="flex items-center gap-2">
            <button
              onClick={() => setLowStockOnly((prev) => !prev)}
              className={`inline-flex items-center gap-1.5 rounded-md px-4 py-2 text-sm font-medium shadow-sm transition-colors ${
                lowStockOnly
                  ? 'bg-red-600 text-white hover:bg-red-700'
                  : 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              {lowStockOnly ? '✕ Low Stock Only' : '⚠ Low Stock Only'}
            </button>
            <Link
              to="/inventory/new"
              className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700"
            >
              + Add Item
            </Link>
          </div>
        }
      />

      <div className="mb-4 flex flex-wrap gap-2">
        <input
          type="search"
          placeholder="Search by name or SKU…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-56 rounded-md border border-gray-300 px-3 py-1.5 text-sm shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
        />
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
            onClick={() => { setSearch(''); setCategory(''); setPage(1) }}
            className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50"
          >
            Clear
          </button>
        )}
        {!loading && (
          <span className="ml-auto self-center text-xs text-gray-400">
            {filtered.length} of {items.length}
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
