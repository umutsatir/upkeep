// OWNER: MEMBER-1
// Fully implemented reference vertical slice.
// Other members should follow this same pattern for their List pages.

import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getAll } from '../../api/workOrders.js'
import Table from '../../components/Table.jsx'
import StatusBadge from '../../components/StatusBadge.jsx'
import PageHeader from '../../components/PageHeader.jsx'

const COLUMNS = [
  { key: 'title',    header: 'Title' },
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

  useEffect(() => {
    setLoading(true)
    setError(null)
    getAll()
      .then(setWorkOrders)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

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
      <Table columns={COLUMNS} data={workOrders} loading={loading} error={error} />
    </div>
  )
}
