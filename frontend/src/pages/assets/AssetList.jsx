// OWNER: MEMBER-2
// TODO (MEMBER-2): implement this page following the WorkOrderList pattern.
//
// Pattern to copy from src/pages/workOrders/WorkOrderList.jsx:
//   1. import { getAll } from '../../api/assets.js'
//   2. useState for data / loading / error
//   3. useEffect → getAll() → setData / setError / setLoading
//   4. Define COLUMNS with render functions (use StatusBadge for status)
//   5. Render <PageHeader> + <Table columns data loading error>
//
// Suggested columns: name, asset_tag, category, status, location, actions.

import { Link } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

export default function AssetList() {
  return (
    <div>
      <PageHeader
        title="Assets"
        subtitle="Track equipment, machinery, and infrastructure."
        action={
          <Link
            to="/assets/new"
            className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700"
          >
            + Add Asset
          </Link>
        }
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-2): implement asset list using the WorkOrderList pattern.</p>
      </div>
    </div>
  )
}
