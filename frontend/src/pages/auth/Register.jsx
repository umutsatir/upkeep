// OWNER: MEMBER-1
import { Link } from 'react-router-dom'

// TODO (MEMBER-1):
// - POST to /api/v1/users/ with full_name, email, password, role.
// - Redirect to /login on success.

export default function Register() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-sm rounded-xl border border-gray-200 bg-white p-8 shadow-lg">
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-gray-900">Create Account</h1>
          <p className="mt-1 text-sm text-gray-500">Join Upkeep CMMS</p>
        </div>

        {/* TODO (MEMBER-1): wire up form */}
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Full Name</label>
            <input type="text" className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input type="email" className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input type="password" className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm" />
          </div>
          <button
            type="submit"
            className="w-full rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-brand-700"
          >
            Register
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-500">
          Already have an account?{' '}
          <Link to="/login" className="text-brand-600 hover:underline">Sign In</Link>
        </p>
      </div>
    </div>
  )
}
