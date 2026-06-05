const PAGE_SIZES = [10, 20, 50]

export default function Pagination({ total, page, pageSize, onPage, onPageSize }) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize))
  const from = total === 0 ? 0 : (page - 1) * pageSize + 1
  const to   = Math.min(page * pageSize, total)

  return (
    <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-gray-200 pt-3">
      {/* left: page size selector */}
      <div className="flex items-center gap-2 text-sm text-gray-600">
        <span>Show</span>
        <select
          value={pageSize}
          onChange={(e) => { onPageSize(Number(e.target.value)); onPage(1) }}
          className="rounded-md border border-gray-300 px-2 py-1 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
        >
          {PAGE_SIZES.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <span>per page</span>
        {total > 0 && (
          <span className="ml-2 text-gray-400">
            {from}–{to} of {total}
          </span>
        )}
      </div>

      {/* right: page buttons */}
      <div className="flex items-center gap-1">
        <NavBtn onClick={() => onPage(1)} disabled={page === 1} label="«" />
        <NavBtn onClick={() => onPage(page - 1)} disabled={page === 1} label="‹" />

        {pageNumbers(page, totalPages).map((p, i) =>
          p === '…' ? (
            <span key={`ellipsis-${i}`} className="px-2 text-gray-400">…</span>
          ) : (
            <button
              key={p}
              onClick={() => onPage(p)}
              className={`min-w-[2rem] rounded-md px-2 py-1 text-sm font-medium transition-colors ${
                p === page
                  ? 'bg-brand-600 text-white'
                  : 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              {p}
            </button>
          )
        )}

        <NavBtn onClick={() => onPage(page + 1)} disabled={page === totalPages} label="›" />
        <NavBtn onClick={() => onPage(totalPages)} disabled={page === totalPages} label="»" />
      </div>
    </div>
  )
}

function NavBtn({ onClick, disabled, label }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="min-w-[2rem] rounded-md border border-gray-300 bg-white px-2 py-1 text-sm text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
    >
      {label}
    </button>
  )
}

function pageNumbers(current, total) {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  if (current <= 4) return [1, 2, 3, 4, 5, '…', total]
  if (current >= total - 3) return [1, '…', total - 4, total - 3, total - 2, total - 1, total]
  return [1, '…', current - 1, current, current + 1, '…', total]
}
