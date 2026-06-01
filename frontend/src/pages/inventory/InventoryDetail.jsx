// OWNER: MEMBER-4
// TODO (MEMBER-4): display all item fields, current stock level,
// consumption log table, and buttons for Consume / Restock actions.
// Consume requires a work_order_id (searchable select from work orders API —
// MEMBER-1 integration point).

import { useParams } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

export default function InventoryDetail() {
  const { id } = useParams()
  return (
    <div>
      <PageHeader title="Inventory Item" subtitle={id} />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-4): display inventory item #{id}.</p>
      </div>
    </div>
  )
}
