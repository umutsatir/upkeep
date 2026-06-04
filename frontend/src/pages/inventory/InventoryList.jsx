// OWNER: MEMBER-4
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getAll, getLowStock } from '../../api/inventory.js'
import Table from '../../components/Table.jsx'
import PageHeader from '../../components/PageHeader.jsx'

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
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lowStockOnly, setLowStockOnly] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(null)
    const fetcher = lowStockOnly ? getLowStock : getAll
    fetcher()
      .then(setItems)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [lowStockOnly])

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
      <Table columns={COLUMNS} data={items} loading={loading} error={error} />
    </div>
  )
}
