// OWNER: MEMBER-1
import { useState, useEffect, useRef } from 'react'
import { NavLink, Outlet, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'

const BASE_NAV = [
  { to: '/',            label: 'Dashboard',   icon: HomeIcon },
  { to: '/work-orders', label: 'Work Orders', icon: ClipboardIcon },
  { to: '/assets',      label: 'Assets',      icon: CubeIcon },
  { to: '/maintenance', label: 'Maintenance', icon: CalendarIcon },
  { to: '/inventory',   label: 'Inventory',   icon: ArchiveIcon },
]

const ADMIN_NAV = [
  { to: '/users', label: 'Users', icon: UsersIcon },
]

const ROLE_COLORS = {
  admin:       'bg-violet-500/20 text-violet-300',
  supervisor:  'bg-sky-500/20 text-sky-300',
  technician:  'bg-emerald-500/20 text-emerald-300',
  viewer:      'bg-gray-500/20 text-gray-300',
}

function UserAvatar({ name }) {
  const initials = name
    ? name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()
    : '?'
  return (
    <span className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-brand-600 text-xs font-semibold text-white">
      {initials}
    </span>
  )
}

function NavItem({ to, label, icon: Icon, onClose }) {
  return (
    <NavLink
      to={to}
      end={to === '/'}
      onClick={onClose}
      className={({ isActive }) =>
        `group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-150 ${
          isActive
            ? 'bg-brand-600 text-white shadow-sm'
            : 'text-gray-400 hover:bg-white/5 hover:text-white'
        }`
      }
    >
      {({ isActive }) => (
        <>
          <Icon className={`h-[18px] w-[18px] flex-shrink-0 transition-colors ${isActive ? 'text-white' : 'text-gray-500 group-hover:text-gray-300'}`} />
          {label}
        </>
      )}
    </NavLink>
  )
}

function SidebarContent({ user, onLogout, onClose }) {
  const isAdmin = user?.role === 'admin'

  return (
    <>
      {/* Logo */}
      <div className="flex h-16 items-center gap-3 px-5 border-b border-white/5 flex-shrink-0">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600">
          <WrenchIcon className="h-4 w-4 text-white" />
        </div>
        <div className="flex-1">
          <span className="text-sm font-bold tracking-wide text-white">Upkeep</span>
          <span className="block text-[10px] font-medium tracking-widest text-gray-500 uppercase">CMMS</span>
        </div>
        {/* Close button — only shown on mobile */}
        {onClose && (
          <button
            onClick={onClose}
            className="lg:hidden flex-shrink-0 rounded-md p-1.5 text-gray-500 hover:bg-white/10 hover:text-white transition-colors"
            aria-label="Close menu"
          >
            <XIcon className="h-5 w-5" />
          </button>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <p className="mb-2 px-3 text-[10px] font-semibold uppercase tracking-widest text-gray-500">
          Menu
        </p>
        {BASE_NAV.map((item) => (
          <NavItem key={item.to} {...item} onClose={onClose} />
        ))}

        {isAdmin && (
          <>
            <p className="mt-4 mb-2 px-3 text-[10px] font-semibold uppercase tracking-widest text-gray-500">
              Admin
            </p>
            {ADMIN_NAV.map((item) => (
              <NavItem key={item.to} {...item} onClose={onClose} />
            ))}
          </>
        )}
      </nav>

      {/* User section */}
      <div className="border-t border-white/5 p-3 flex-shrink-0">
        {user && (
          <div className="flex items-center gap-3 rounded-lg px-2 py-2">
            <UserAvatar name={user.full_name} />
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-white">{user.full_name}</p>
              <span className={`inline-block mt-0.5 rounded-full px-1.5 py-0.5 text-[10px] font-medium capitalize ${ROLE_COLORS[user.role] ?? ROLE_COLORS.viewer}`}>
                {user.role}
              </span>
            </div>
            <button
              onClick={onLogout}
              title="Log out"
              className="flex-shrink-0 rounded-md p-1.5 text-gray-500 hover:bg-white/10 hover:text-white transition-colors"
            >
              <LogoutIcon className="h-4 w-4" />
            </button>
          </div>
        )}
      </div>
    </>
  )
}

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const backdropRef = useRef(null)

  // Close sidebar on route change (mobile)
  useEffect(() => {
    setSidebarOpen(false)
  }, [location.pathname])

  // Prevent body scroll when mobile sidebar is open
  useEffect(() => {
    if (sidebarOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => { document.body.style.overflow = '' }
  }, [sidebarOpen])

  function handleLogout() {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">

      {/* ── Desktop sidebar (always visible ≥ lg) ── */}
      <aside className="hidden lg:flex w-64 flex-shrink-0 flex-col bg-gray-900 shadow-xl">
        <SidebarContent user={user} onLogout={handleLogout} onClose={null} />
      </aside>

      {/* ── Mobile sidebar overlay ── */}
      <div
        className={`fixed inset-0 z-40 lg:hidden transition-opacity duration-300 ${
          sidebarOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
        onClick={() => setSidebarOpen(false)}
      >
        {/* Backdrop */}
        <div className="absolute inset-0 bg-black/50" />
        {/* Drawer */}
        <aside
          className={`absolute inset-y-0 left-0 flex w-72 flex-col bg-gray-900 shadow-xl transition-transform duration-300 ease-in-out ${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
          onClick={(e) => e.stopPropagation()}
        >
          <SidebarContent
            user={user}
            onLogout={handleLogout}
            onClose={() => setSidebarOpen(false)}
          />
        </aside>
      </div>

      {/* ── Main area ── */}
      <div className="flex flex-1 flex-col overflow-hidden min-w-0">

        {/* Mobile top bar */}
        <header className="flex lg:hidden h-14 flex-shrink-0 items-center gap-3 border-b border-gray-200 bg-white px-4 shadow-sm">
          <button
            onClick={() => setSidebarOpen(true)}
            className="rounded-md p-1.5 text-gray-500 hover:bg-gray-100 hover:text-gray-900 transition-colors"
            aria-label="Open menu"
          >
            <MenuIcon className="h-5 w-5" />
          </button>
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-brand-600">
              <WrenchIcon className="h-3.5 w-3.5 text-white" />
            </div>
            <span className="text-sm font-bold text-gray-900">Upkeep</span>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-4 sm:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

// ── Icons ──────────────────────────────────────────────────────────────────

function WrenchIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
        d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
    </svg>
  )
}

function HomeIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
        d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
  )
}

function ClipboardIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
        d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25z" />
    </svg>
  )
}

function CubeIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
        d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
    </svg>
  )
}

function CalendarIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
        d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
    </svg>
  )
}

function ArchiveIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
        d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
    </svg>
  )
}

function LogoutIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
        d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
    </svg>
  )
}

function MenuIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
    </svg>
  )
}

function XIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
        d="M6 18L18 6M6 6l12 12" />
    </svg>
  )
}

function UsersIcon({ className }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
        d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
    </svg>
  )
}
