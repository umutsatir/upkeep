// OWNER: MEMBER-1
// Standard page header with title, optional subtitle, and an action slot.

export default function PageHeader({ title, subtitle, action }) {
  return (
    <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <h1 className="text-xl font-bold text-gray-900 sm:text-2xl">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-gray-500">{subtitle}</p>}
      </div>
      {action && <div className="sm:ml-4 flex-shrink-0">{action}</div>}
    </div>
  )
}
