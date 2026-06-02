// OWNER: MEMBER-1
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'

export default function ProtectedRoute({ children }) {
  const { token, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center text-gray-400">
        Loading…
      </div>
    )
  }

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return children
}
