// OWNER: MEMBER-1
import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getById } from '../../api/workOrders.js'
import StatusBadge from '../../components/StatusBadge.jsx'
import PageHeader from '../../components/PageHeader.jsx'

export default function WorkOrderDetail() {
  const { id } = useParams()
  const [wo, setWo]         = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  useEffect(() => {
    setLoading(true)
    getById(id)
      .then(setWo)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <p className="text-gray-400 py-8 text-center">Loading…</p>
  if (error)   return <p className="text-red-600 py-8 text-center">{error}</p>
  if (!wo)     return null

  return (
    <div>
      <PageHeader
        title={wo.title}
        subtitle={`Work Order #${wo.id}`}
        action={
          <Link
            to={`/work-orders/${id}/edit`}
            className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
          >
            Edit
          </Link>
        }
      />

      {/* TODO (MEMBER-1): build out the detail card with all fields,
          status transition buttons (assign / start / complete / close),
          and parts-used table (MEMBER-4 integration). */}
      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <dl className="grid grid-cols-2 gap-4 sm:grid-cols-3">
          <Field label="Status"   value={<StatusBadge value={wo.status} />} />
          <Field label="Priority" value={<StatusBadge value={wo.priority} />} />
          <Field label="Due Date" value={wo.due_date ? new Date(wo.due_date).toLocaleDateString() : '—'} />
          <Field label="Asset ID" value={wo.asset_id} />
          <Field label="Created"  value={new Date(wo.created_at).toLocaleString()} />
          <Field label="Updated"  value={new Date(wo.updated_at).toLocaleString()} />
        </dl>
        {wo.notes && (
          <div className="mt-4 border-t pt-4">
            <p className="text-sm font-medium text-gray-500">Notes</p>
            <p className="mt-1 text-sm text-gray-800">{wo.notes}</p>
          </div>
        )}
      </div>
    </div>
  )
}

function Field({ label, value }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wider text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm text-gray-900">{value}</dd>
    </div>
  )
}
