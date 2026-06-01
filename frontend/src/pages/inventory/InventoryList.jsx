// OWNER: MEMBER-4
// TODO (MEMBER-4): implement following WorkOrderList pattern.
// - Call getAll() from api/inventory.js on mount.
// - Suggested columns: name, sku, category, quantity_on_hand,
//   low_stock_threshold, unit_cost, unit, actions.
// - Highlight rows where quantity_on_hand <= low_stock_threshold in red.
// - Add "Low Stock Only" toggle that switches to getLowStock() instead of getAll().

import { Link } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

export default function InventoryList() {
  return (
    <div>
      <PageHeader
        title="Inventory"
        subtitle="Manage spare parts and consumables."
        action={
          <Link
            to="/inventory/new"
            className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700"
          >
            + Add Item
          </Link>
        }
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-4): implement inventory list.</p>
      </div>
    </div>
  )
}
