// OWNER: MEMBER-2
import { useState, useEffect } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getById, remove } from '../../api/assets.js'
import StatusBadge from '../../components/StatusBadge.jsx'
import PageHeader from '../../components/PageHeader.jsx'

export default function AssetDetail() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [asset, setAsset] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    getById(id)
      .then(setAsset)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  async function handleDelete() {
    if (!window.confirm('Are you sure you want to delete this asset?')) return
    try {
      await remove(id)
      navigate('/assets', { replace: true })
    } catch (err) {
      setError(err.message)
    }
  }

  if (loading) return <p className="py-8 text-center text-gray-400">Loading…</p>
  if (error) return <p className="py-8 text-center text-red-600">{error}</p>
  if (!asset) return null

  return (
    <div className="mx-auto max-w-2xl space-y-4 sm:space-y-6">
      <PageHeader
        title={asset.name}
        subtitle={asset.asset_tag}
        action={
          <div className="flex flex-wrap gap-2">
            <Link
              to={`/assets/${id}/edit`}
              className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Edit
            </Link>
            <button
              onClick={handleDelete}
              className="rounded-md border border-red-200 bg-white px-3 py-1.5 text-sm font-medium text-red-600 hover:bg-red-50"
            >
              Delete
            </button>
          </div>
        }
      />

      {/* Details card */}
      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <dl className="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-2 lg:grid-cols-3">
          <Field label="Status" value={<StatusBadge value={asset.status} />} />
          <Field label="Category" value={asset.category} />
          <Field label="Location" value={asset.location || '—'} />
          
          <Field label="Model Number" value={asset.model_number || '—'} />
          <Field label="Serial Number" value={asset.serial_number || '—'} />
          <Field label="Assigned To" value={asset.assigned_to || '—'} />
          
          <Field label="Purchase Date" value={asset.purchase_date ? new Date(asset.purchase_date).toLocaleDateString() : '—'} />
          <Field label="Warranty Expiry" value={asset.warranty_expires_at ? new Date(asset.warranty_expires_at).toLocaleDateString() : '—'} />
          <Field label="Created" value={new Date(asset.created_at).toLocaleString()} />
        </dl>

        {asset.notes && (
          <div className="mt-4 border-t border-gray-100 pt-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">Notes</p>
            <p className="mt-1 text-sm text-gray-800">{asset.notes}</p>
          </div>
        )}
      </div>

      {/* Repair History panel */}
      {asset.repair_history?.length > 0 && (
        <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <p className="mb-4 text-sm font-semibold text-gray-700">Repair History</p>
          <div className="space-y-4">
            {asset.repair_history.map((record, i) => (
              <div key={i} className="flex flex-col border-b border-gray-100 pb-4 last:border-0 last:pb-0 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-900">{record.description}</p>
                  <div className="mt-1 flex items-center gap-2 text-xs text-gray-500">
                    <time>{new Date(record.date).toLocaleDateString()}</time>
                    {record.work_order_id && (
                      <>
                        <span>•</span>
                        <span>WO: <code className="rounded bg-gray-100 px-1">{record.work_order_id}</code></span>
                      </>
                    )}
                  </div>
                </div>
                {record.cost > 0 && (
                  <div className="mt-2 text-sm font-semibold text-gray-700 sm:mt-0">
                    ${record.cost.toFixed(2)}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function Field({ label, value }) {
  return (
    <div>
      <dt className="text-xs font-semibold uppercase tracking-wider text-gray-400">{label}</dt>
      <dd className="mt-1 text-sm text-gray-900">{value}</dd>
    </div>
  )
}
