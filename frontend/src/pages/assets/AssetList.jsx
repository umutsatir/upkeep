// OWNER: MEMBER-2
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getAll } from '../../api/assets.js'
import Table from '../../components/Table.jsx'
import StatusBadge from '../../components/StatusBadge.jsx'
import PageHeader from '../../components/PageHeader.jsx'

const COLUMNS = [
  { key: 'name',       header: 'Name' },
  {
    key: 'asset_tag',
    header: 'Tag',
    render: (val) => <code className="rounded bg-gray-100 px-1.5 py-0.5 text-xs text-gray-800">{val}</code>,
  },
  { key: 'category',   header: 'Category' },
  { key: 'location',   header: 'Location', render: (val) => val || '—' },
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
  const [assets, setAssets]   = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    getAll()
      .then(setAssets)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

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
      <Table columns={COLUMNS} data={assets} loading={loading} error={error} />
    </div>
  )
}
