// OWNER: MEMBER-1
import { useState, useEffect } from 'react'
import { useAuth } from '../../contexts/AuthContext.jsx'
import { getAll, create, remove } from '../../api/users.js'
import PageHeader from '../../components/PageHeader.jsx'

const ROLES = ['viewer', 'technician', 'supervisor', 'admin']

const ROLE_COLORS = {
  admin:      'bg-violet-100 text-violet-700',
  supervisor: 'bg-sky-100 text-sky-700',
  technician: 'bg-emerald-100 text-emerald-700',
  viewer:     'bg-gray-100 text-gray-600',
}

const EMPTY_FORM = { full_name: '', email: '', password: '', role: 'technician' }

export default function UserList() {
  const { user: me } = useAuth()

  const [users, setUsers]       = useState([])
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm]         = useState(EMPTY_FORM)
  const [saving, setSaving]     = useState(false)
  const [formError, setFormError] = useState(null)

  useEffect(() => { loadUsers() }, [])

  async function loadUsers() {
    setLoading(true)
    setError(null)
    try {
      const data = await getAll({ limit: 200 })
      setUsers(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function set(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }))
  }

  async function handleCreate(e) {
    e.preventDefault()
    setSaving(true)
    setFormError(null)
    try {
      const created = await create(form)
      setUsers((prev) => [...prev, created])
      setForm(EMPTY_FORM)
      setShowForm(false)
    } catch (err) {
      setFormError(err.message)
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete(id, name) {
    if (!window.confirm(`Delete user "${name}"?`)) return
    try {
      await remove(id)
      setUsers((prev) => prev.filter((u) => u.id !== id))
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="mx-auto max-w-4xl space-y-4 sm:space-y-6">
      <PageHeader
        title="Users"
        subtitle="Manage team members and their roles"
        action={
          <button
            onClick={() => { setShowForm((v) => !v); setFormError(null) }}
            className="rounded-md bg-brand-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-brand-700"
          >
            {showForm ? 'Cancel' : 'New User'}
          </button>
        }
      />

      {/* New user form */}
      {showForm && (
        <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <p className="mb-4 text-sm font-semibold text-gray-700">Create New User</p>

          {formError && (
            <div className="mb-3 rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
              {formError}
            </div>
          )}

          <form onSubmit={handleCreate} className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Full Name</label>
              <input
                required
                type="text"
                value={form.full_name}
                onChange={set('full_name')}
                className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Email</label>
              <input
                required
                type="email"
                value={form.email}
                onChange={set('email')}
                className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Password</label>
              <input
                required
                type="password"
                minLength={8}
                value={form.password}
                onChange={set('password')}
                className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Role</label>
              <select
                value={form.role}
                onChange={set('role')}
                className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
              >
                {ROLES.map((r) => (
                  <option key={r} value={r}>{r.charAt(0).toUpperCase() + r.slice(1)}</option>
                ))}
              </select>
            </div>

            <div className="sm:col-span-2 flex justify-end">
              <button
                type="submit"
                disabled={saving}
                className="rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 disabled:opacity-50"
              >
                {saving ? 'Creating…' : 'Create User'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* User table */}
      <div className="rounded-lg border border-gray-200 bg-white shadow-sm overflow-hidden">
        {loading ? (
          <p className="py-10 text-center text-sm text-gray-400">Loading…</p>
        ) : users.length === 0 ? (
          <p className="py-10 text-center text-sm text-gray-400">No users yet.</p>
        ) : (
          <table className="min-w-full divide-y divide-gray-100">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">Name</th>
                <th className="px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">Email</th>
                <th className="px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">Role</th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-gray-50">
                  <td className="px-5 py-3 text-sm font-medium text-gray-900">{u.full_name}</td>
                  <td className="px-5 py-3 text-sm text-gray-500">{u.email}</td>
                  <td className="px-5 py-3">
                    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium capitalize ${ROLE_COLORS[u.role] ?? ROLE_COLORS.viewer}`}>
                      {u.role}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-right">
                    {u.id !== me?.id && (
                      <button
                        onClick={() => handleDelete(u.id, u.full_name)}
                        className="text-xs text-red-500 hover:text-red-700"
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
