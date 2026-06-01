// OWNER: MEMBER-1
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getAll as getWorkOrders } from '../api/workOrders.js'
import { getAll as getAssets }     from '../api/assets.js'
import { getAll as getMaintenance } from '../api/maintenance.js'
import { getLowStock }              from '../api/inventory.js'
import PageHeader from '../components/PageHeader.jsx'

// TODO (MEMBER-1): replace summary cards with real API counts once the
// backend services are implemented. Low-stock data can come from MEMBER-4's
// /inventory/low-stock endpoint (already wired in api/inventory.js).

export default function Dashboard() {
  const [stats, setStats] = useState({
    workOrders: null,
    assets: null,
    schedules: null,
    lowStock: null,
  })

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

      {/* Placeholder recent-activity panel */}
      <div className="mt-8 rounded-lg border border-dashed border-gray-300 bg-white p-8 text-center text-gray-400">
        <p className="text-sm">
          TODO (MEMBER-1): add a recent work-orders table here using the reusable{' '}
          <code className="rounded bg-gray-100 px-1 text-xs">&lt;Table /&gt;</code> component.
        </p>
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
