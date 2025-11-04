import React, { useEffect, useState, useRef } from 'react'
import { Smile } from 'lucide-react'
import api from '../api/axios'
import '../styles/Reactions.css'

export default function ReactionBar({ messageId, onChange, isHovered = false }){
  const [reactions, setReactions] = useState([])
  const [grouped, setGrouped] = useState({})
  const [showPicker, setShowPicker] = useState(false)
  const [fetchedOnce, setFetchedOnce] = useState(false)
  const pickerRef = useRef(null)

  // Keep only 4 important emojis per request
  const emojiList = ['👍','👀','🎉','❤️']

  const fetchReactions = async () => {
    try {
      const res = await api.get(`/api/messages/${messageId}/reactions`)
      setReactions(res.data)
      setFetchedOnce(true)
    } catch (err) {
      console.error('Error fetching reactions:', err)
    }
  }

  // fetch current user so we can tell if the current user already reacted
  const [currentUser, setCurrentUser] = useState(null)
  useEffect(()=>{
    let mounted = true
    api.get('/api/auth/me').then(r=>{ if(mounted) setCurrentUser(r.data) }).catch(()=>{})
    return ()=>{ mounted = false }
  }, [])

  const toggleReaction = async (emoji) => {
    try {
      // check if current user has reacted with this emoji
      if (!currentUser) {
        // fallback: just add reaction if no user info
        await addReaction(emoji)
        return
      }

      const userReaction = reactions.find(r => r.emoji === emoji && r.user_id === currentUser.id)
      if (userReaction) {
        // remove
        await api.delete(`/api/messages/reactions/${userReaction.id}`)
        await fetchReactions()
        if (onChange) onChange()
        return
      }

      // otherwise add
      await addReaction(emoji)
    } catch (err) {
      console.error('Error toggling reaction:', err)
    }
  }

  // Fetch reactions when messageId changes or when the user hovers (so
  // hover opens the picker and we have up-to-date counts). Avoid fetching
  // repeatedly if we already fetched and nothing changed.
  useEffect(() => {
    if (!messageId) return
    if (isHovered || !fetchedOnce) {
      fetchReactions()
    }
  }, [messageId, isHovered])

  useEffect(() => {
    const map = {}
    reactions.forEach(r => {
      if (!map[r.emoji]) map[r.emoji] = []
      map[r.emoji].push(r)
    })
    setGrouped(map)
  }, [reactions])

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (pickerRef.current && !pickerRef.current.contains(e.target)) setShowPicker(false)
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const addReaction = async (emoji) => {
    try {
      await api.post(`/api/messages/${messageId}/reactions`, { emoji, message_id: messageId })
      await fetchReactions()
      if (onChange) onChange()
    } catch (err) {
      console.error('Error adding reaction:', err)
      // If already reacted, try to ignore
    }
  }

  // If there are no reactions and the message is not hovered, render
  // nothing to keep the UI clean.
  const hasReactions = reactions && reactions.length > 0

  return (
    <div className="reaction-bar">
      {/* Inline reaction pills shown only if there are reactions */}
      {hasReactions && (
        <div className="reaction-list">
          {Object.keys(grouped).map(emoji => (
            <button key={emoji} className="reaction-pill" title={`${grouped[emoji].length} reactions`} onClick={() => toggleReaction(emoji)}>
              <span className="reaction-emoji">{emoji}</span>
              <span className="reaction-count">{grouped[emoji].length}</span>
            </button>
          ))}
        </div>
      )}

      {/* When hovered over the message, show a compact hover bar to add reactions */}
      {isHovered && (
        <div className="reaction-hover">
          <div className="reaction-hover-list">
            {emojiList.map(e => (
              <button key={e} className="emoji-btn hover-emoji" onClick={() => toggleReaction(e)}>{e}</button>
            ))}
            <button className="emoji-btn hover-emoji" onClick={() => setShowPicker(!showPicker)}>+ </button>
          </div>

          {showPicker && (
            <div className="emoji-picker" ref={pickerRef}>
              {emojiList.map(e => (
                <button key={e} className="emoji-btn" onClick={() => { addReaction(e); setShowPicker(false) }}>{e}</button>
              ))}
              <div className="emoji-custom">
                <input placeholder="Custom emoji" onKeyDown={async (ev)=>{ if(ev.key==='Enter'){ await addReaction(ev.target.value); ev.target.value=''; setShowPicker(false)} }} />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
