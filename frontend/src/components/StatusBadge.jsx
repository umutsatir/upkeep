// OWNER: MEMBER-1
// Colour-coded pill for work order / asset status values.

const PALETTE = {
  // Work order statuses
  open:        'bg-blue-100 text-blue-700',
  assigned:    'bg-yellow-100 text-yellow-700',
  in_progress: 'bg-orange-100 text-orange-700',
  completed:   'bg-green-100 text-green-700',
  closed:      'bg-gray-100 text-gray-600',
  cancelled:   'bg-red-100 text-red-600',
  // Asset statuses
  active:             'bg-green-100 text-green-700',
  inactive:           'bg-gray-100 text-gray-600',
  under_maintenance:  'bg-orange-100 text-orange-700',
  decommissioned:     'bg-red-100 text-red-600',
  // Priority
  low:      'bg-gray-100 text-gray-600',
  medium:   'bg-blue-100 text-blue-700',
  high:     'bg-orange-100 text-orange-700',
  critical: 'bg-red-100 text-red-700 font-semibold',
}

export default function StatusBadge({ value }) {
  const key = (value ?? '').toLowerCase().replace(' ', '_')
  const classes = PALETTE[key] ?? 'bg-gray-100 text-gray-600'
  const label = (value ?? '').replace(/_/g, ' ')
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs capitalize ${classes}`}>
      {label}
    </span>
  )
}
