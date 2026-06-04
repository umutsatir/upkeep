// OWNER: MEMBER-1
// Standard page header with title, optional subtitle, and an action slot.
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function PageHeader({ title, subtitle, action, backTo }) {
  const navigate = useNavigate()

  useEffect(() => {
    if (!backTo) return
    function onKey(e) {
      if (e.key === 'Escape') navigate(backTo)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [backTo, navigate])

  return (
    <div className="mb-6 flex flex-col gap-2">
      {backTo && (
        <button
          onClick={() => navigate(backTo)}
          className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-800 w-fit"
        >
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          Back
        </button>
      )}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-900 sm:text-2xl">{title}</h1>
          {subtitle && <p className="mt-1 text-sm text-gray-500">{subtitle}</p>}
        </div>
        {action && <div className="sm:ml-4 flex-shrink-0">{action}</div>}
      </div>
    </div>
  )
}
