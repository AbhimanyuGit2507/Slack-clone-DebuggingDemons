import React, { createContext, useState, useContext, useEffect } from 'react'
import api from '../api/axios'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [authChecked, setAuthChecked] = useState(false)

  // Check if user is already logged in on mount
  useEffect(() => {
    if (!authChecked) {
      checkAuth()
    }
  }, [authChecked])

  const checkAuth = async () => {
    try {
      const response = await api.get('/api/auth/me')
      setUser(response.data)
      setError(null)
    } catch (err) {
      setUser(null)
      // Don't show error on initial check (user might not be logged in)
    } finally {
      setLoading(false)
      setAuthChecked(true)
    }
  }

  const login = async (username, password) => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.post('/api/auth/login', {
        username,
        password,
      })
      setUser(response.data.user)
      return { success: true }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Login failed'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const signup = async (username, email, password, name) => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.post('/api/auth/signup', {
        username,
        email,
        password,
        name,
      })
      setUser(response.data.user)
      return { success: true }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Signup failed'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      await api.post('/api/auth/logout')
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      setUser(null)
    }
  }

  const value = {
    user,
    loading,
    error,
    login,
    signup,
    logout,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
