// OWNER: MEMBER-2
// TODO (MEMBER-2): implement following WorkOrderDetail pattern.
// - Call getById(id) on mount.
// - Display all asset fields (name, tag, category, status, location,
//   warranty info, repair history list).
// - Link to the Edit form.

import { useParams } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

export default function AssetDetail() {
  const { id } = useParams()
  return (
    <div>
      <PageHeader title="Asset Detail" subtitle={id} />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-2): display asset #{id} details.</p>
      </div>
    </div>
  )
}
