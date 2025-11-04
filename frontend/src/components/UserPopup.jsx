import React, { useEffect, useState, useRef } from 'react'
import api from '../api/axios'
import '../styles/UserPopup.css'

export default function UserPopup({ visible, onClose, style = {} }){
  const [user, setUser] = useState(null)
  const ref = useRef(null)

  useEffect(() => {
    if (!visible) return
    let mounted = true
    const fetch = async () => {
      try {
        const res = await api.get('/api/auth/me')
        if (mounted) setUser(res.data || null)
      } catch (err) {
        console.error('Failed to load current user', err)
        if (mounted) setUser(null)
      }
    }
    fetch()
    return () => { mounted = false }
  }, [visible])

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (visible && ref.current && !ref.current.contains(e.target)) {
        onClose()
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [visible, onClose])

  if (!visible) return null

  return (
    <div className="user-popup" ref={ref} role="dialog" aria-modal="false" style={style}>
      <div className="user-popup-inner">
        {user ? (
          <>
            <div className="user-popup-header">
              <div className="user-popup-avatar">
                {user.profile_picture ? (
                  <img src={user.profile_picture} alt={user.full_name || user.username} />
                ) : (
                  <div className="user-initial">{(user.full_name || user.username || 'U')[0].toUpperCase()}</div>
                )}
              </div>
              <div className="user-popup-info">
                <div className="user-popup-name">{user.full_name || user.name || user.username}</div>
                <div className="user-popup-status">Active</div>
              </div>
            </div>

            <div className="user-popup-status-box">
              <span className="status-emoji">🙂</span>
              <input className="status-input" placeholder="Update your status" />
            </div>

            <ul className="user-popup-menu">
              <li>Set yourself as away</li>
              <li>Pause notifications <span className="chev">›</span></li>
              <li className="menu-divider" aria-hidden="true" />
              <li>Profile</li>
              <li>Preferences</li>
              <li className="menu-divider" aria-hidden="true" />
              <li className="signout">Sign out of Debugging Demons</li>
            </ul>
          </>
        ) : (
          <div className="user-popup-loading">Loading…</div>
        )}
      </div>
    </div>
  )
}
