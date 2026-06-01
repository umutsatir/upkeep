// OWNER: MEMBER-3
// TODO (MEMBER-3): create / edit form.
// Fields: title, description, asset_id (searchable select from assets API),
//         trigger_type (radio: time_based | usage_based),
//         interval_days (shown only when time_based),
//         usage_threshold_hours (shown only when usage_based),
//         generated_wo_priority, assigned_to.
// Use conditional rendering based on trigger_type selection.

import { useParams, useNavigate } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

export default function MaintenanceForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  return (
    <div>
      <PageHeader title={isEdit ? 'Edit Schedule' : 'New Schedule'} />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-3): build the maintenance schedule form here.</p>
        <button onClick={() => navigate('/maintenance')} className="mt-4 text-sm text-brand-600 underline">
          Back to list
        </button>
      </div>
    </div>
  )
}
