// OWNER: MEMBER-4
// TODO (MEMBER-4): create / edit form.
// Fields: name, sku, category, quantity_on_hand, low_stock_threshold,
//         unit_cost, unit (select: pcs/litres/metres/kg), supplier,
//         location (bin/shelf), notes.
// Validate: sku uniqueness should be caught from the 422 API response.

import { useParams, useNavigate } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

export default function InventoryForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  return (
    <div>
      <PageHeader title={isEdit ? 'Edit Item' : 'New Inventory Item'} />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-4): build the inventory form here.</p>
        <button onClick={() => navigate('/inventory')} className="mt-4 text-sm text-brand-600 underline">
          Back to list
        </button>
      </div>
    </div>
  )
}
