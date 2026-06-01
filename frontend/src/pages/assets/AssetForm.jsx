// OWNER: MEMBER-2
// TODO (MEMBER-2): create / edit form for assets.
// Fields: name, asset_tag, category, location, status (select),
//         purchase_date, warranty_expires_at, model_number, serial_number, notes.
// On submit: create(payload) or update(id, payload), navigate back.

import { useParams, useNavigate } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

export default function AssetForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  return (
    <div>
      <PageHeader title={isEdit ? 'Edit Asset' : 'New Asset'} />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-2): build the asset form here.</p>
        <button onClick={() => navigate('/assets')} className="mt-4 text-sm text-brand-600 underline">
          Back to list
        </button>
      </div>
    </div>
  )
}
