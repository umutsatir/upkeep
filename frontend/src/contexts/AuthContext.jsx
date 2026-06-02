// OWNER: MEMBER-1
import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import client from '../api/client.js'

const AuthContext = createContext(null)

const TOKEN_KEY = 'upkeep_token'

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [user, setUser]   = useState(null)
  const [loading, setLoading] = useState(true)

  // Whenever the token changes, sync it into axios and fetch /users/me
  useEffect(() => {
    if (!token) {
      setUser(null)
      setLoading(false)
      return
    }
    client.defaults.headers.common['Authorization'] = `Bearer ${token}`
    client
      .get('/v1/users/me')
      .then((r) => setUser(r.data))
      .catch(() => {
        // Token is invalid or expired — clear it
        localStorage.removeItem(TOKEN_KEY)
        setToken(null)
        delete client.defaults.headers.common['Authorization']
      })
      .finally(() => setLoading(false))
  }, [token])

  const login = useCallback(async (email, password) => {
    const { data } = await client.post('/v1/auth/login', { email, password })
    localStorage.setItem(TOKEN_KEY, data.access_token)
    client.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`
    setToken(data.access_token)
    const me = await client.get('/v1/users/me')
    setUser(me.data)
    return me.data
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    delete client.defaults.headers.common['Authorization']
    setToken(null)
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>')
  return ctx
}
