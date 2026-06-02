// OWNER: MEMBER-1
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getAll as getWorkOrders } from '../api/workOrders.js'
import { getAll as getAssets }     from '../api/assets.js'
import { getAll as getMaintenance } from '../api/maintenance.js'
import { getLowStock }              from '../api/inventory.js'
import PageHeader from '../components/PageHeader.jsx'
import Table from '../components/Table.jsx'
import StatusBadge from '../components/StatusBadge.jsx'

const RECENT_COLUMNS = [
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
    header: '',
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

export default function Dashboard() {
  const [stats, setStats] = useState({
    workOrders: null,
    assets: null,
    schedules: null,
    lowStock: null,
  })
  const [recentWOs, setRecentWOs]       = useState([])
  const [recentLoading, setRecentLoading] = useState(true)
  const [recentError, setRecentError]   = useState(null)

  useEffect(() => {
    // Fetch all four in parallel; failures are silenced per-card.
    Promise.allSettled([
      getWorkOrders(),
      getAssets(),
      getMaintenance(),
      getLowStock(),
    ]).then(([wo, assets, maint, stock]) => {
      setStats({
        workOrders: wo.status === 'fulfilled' ? wo.value.length : '—',
        assets:     assets.status === 'fulfilled' ? assets.value.length : '—',
        schedules:  maint.status === 'fulfilled' ? maint.value.length : '—',
        lowStock:   stock.status === 'fulfilled' ? stock.value.length : '—',
      })
    })

    // Recent work orders (latest 5)
    getWorkOrders()
      .then((all) => setRecentWOs(all.slice(0, 5)))
      .catch((err) => setRecentError(err.message))
      .finally(() => setRecentLoading(false))
  }, [])

  return (
    <div>
      <PageHeader title="Dashboard" subtitle="System overview at a glance." />

      {/* Stat cards */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <StatCard label="Open Work Orders" value={stats.workOrders} to="/work-orders" color="blue" />
        <StatCard label="Active Assets"    value={stats.assets}     to="/assets"      color="green" />
        <StatCard label="PM Schedules"     value={stats.schedules}  to="/maintenance" color="orange" />
        <StatCard label="Low-Stock Items"  value={stats.lowStock}   to="/inventory"   color="red" />
      </div>

      {/* Quick links */}
      <div className="mt-8">
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-500">
          Quick Actions
        </h2>
        <div className="flex flex-wrap gap-3">
          <QuickLink to="/work-orders/new" label="+ New Work Order" />
          <QuickLink to="/assets/new"      label="+ Add Asset" />
          <QuickLink to="/maintenance/new" label="+ Schedule Maintenance" />
          <QuickLink to="/inventory/new"   label="+ Add Inventory Item" />
        </div>
      </div>

      {/* Recent work orders */}
      <div className="mt-8">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-gray-500">
            Recent Work Orders
          </h2>
          <Link
            to="/work-orders"
            className="text-xs font-medium text-brand-600 hover:text-brand-800 underline underline-offset-2"
          >
            View all
          </Link>
        </div>
        <Table
          columns={RECENT_COLUMNS}
          data={recentWOs}
          loading={recentLoading}
          error={recentError}
        />
      </div>
    </div>
  )
}

function StatCard({ label, value, to, color }) {
  const colors = {
    blue:   'bg-blue-50 text-blue-700 border-blue-200',
    green:  'bg-green-50 text-green-700 border-green-200',
    orange: 'bg-orange-50 text-orange-700 border-orange-200',
    red:    'bg-red-50 text-red-700 border-red-200',
  }
  return (
    <Link
      to={to}
      className={`rounded-lg border p-4 shadow-sm hover:shadow-md transition-shadow ${colors[color]}`}
    >
      <p className="text-3xl font-bold">{value ?? '…'}</p>
      <p className="mt-1 text-sm font-medium">{label}</p>
    </Link>
  )
}

function QuickLink({ to, label }) {
  return (
    <Link
      to={to}
      className="rounded-md border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 transition-colors"
    >
      {label}
    </Link>
  )
}
