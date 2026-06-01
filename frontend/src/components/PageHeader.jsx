// OWNER: MEMBER-1
// Standard page header with title, optional subtitle, and an action slot.

export default function PageHeader({ title, subtitle, action }) {
  return (
    <div className="mb-6 flex items-start justify-between">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-gray-500">{subtitle}</p>}
      </div>
      {action && <div className="ml-4">{action}</div>}
    </div>
  )
}
