// OWNER: MEMBER-3
// TODO (MEMBER-3): display all schedule fields, show last_triggered_at,
// next_due_at, and link to the associated asset (MEMBER-2 integration).

import { useParams } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

export default function MaintenanceDetail() {
  const { id } = useParams()
  return (
    <div>
      <PageHeader title="Schedule Detail" subtitle={id} />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-3): display maintenance schedule #{id}.</p>
      </div>
    </div>
  )
}
