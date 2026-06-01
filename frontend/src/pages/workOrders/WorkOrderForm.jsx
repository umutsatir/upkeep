// OWNER: MEMBER-1
import { useParams, useNavigate } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

// TODO (MEMBER-1): implement create / edit form.
// - On mount: if params.id exists, call getById(id) and populate fields.
// - On submit: call create(payload) or update(id, payload), then navigate back.
// - Fields: title, description, asset_id (dropdown), priority, due_date, notes.
// - Validate required fields before submitting.

export default function WorkOrderForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  return (
    <div>
      <PageHeader title={isEdit ? 'Edit Work Order' : 'New Work Order'} />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-1): build the work order form here.</p>
        <button
          onClick={() => navigate('/work-orders')}
          className="mt-4 text-sm text-brand-600 underline"
        >
          Back to list
        </button>
      </div>
    </div>
  )
}
