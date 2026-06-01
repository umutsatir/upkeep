// OWNER: MEMBER-3
// TODO (MEMBER-3): implement following WorkOrderList pattern.
// - Call getAll() from api/maintenance.js on mount.
// - Suggested columns: title, asset_id, trigger_type, interval_days,
//   is_active, next_due_at, actions.
// - Add an "Evaluate Due" button that calls evaluateDue() and shows
//   how many work orders were auto-generated (toast or inline message).

import { Link } from 'react-router-dom'
import PageHeader from '../../components/PageHeader.jsx'

export default function MaintenanceList() {
  return (
    <div>
      <PageHeader
        title="Preventive Maintenance"
        subtitle="Manage recurring maintenance schedules."
        action={
          <Link
            to="/maintenance/new"
            className="inline-flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700"
          >
            + New Schedule
          </Link>
        }
      />
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center text-gray-400">
        <p className="text-sm">TODO (MEMBER-3): implement maintenance schedule list.</p>
      </div>
    </div>
  )
}
