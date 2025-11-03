import React from 'react'
import { Smile, MessageSquare } from 'lucide-react'
import { MoreHorizontalIcon } from './slack-icons'
import '../styles/ChatWindow.css'

export default function ChatWindow({ messages = [] }){
  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], {hour: 'numeric', minute:'2-digit'})
  }

  const formatDate = (timestamp) => {
    const date = new Date(timestamp)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    if (date.toDateString() === today.toDateString()) {
      return 'Today'
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday'
    } else {
      return date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })
    }
  }

  let lastDate = null

  return (
    <div className="chat-messages">
      <div className="chat-messages-inner">
        {messages.map((m, index) => {
          const username = `User ${m.user_id}`
          const initial = username.charAt(0)
          const messageDate = new Date(m.timestamp).toDateString()
          const showDateDivider = messageDate !== lastDate
          lastDate = messageDate

          return (
            <React.Fragment key={m.id}>
              {showDateDivider && index > 0 && (
                <div className="date-divider">
                  <div className="date-divider-line"></div>
                  <span className="date-divider-text">{formatDate(m.timestamp)}</span>
                </div>
              )}
              <div className="message">
                <div className="message-avatar">{initial}</div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-author">{username}</span>
                    <span className="message-time">{formatTime(m.timestamp)}</span>
                  </div>
                  <div className="message-text">{m.content}</div>
                </div>
                <div className="message-actions">
                  <button className="message-action-btn" title="Add reaction"><Smile size={16} /></button>
                  <button className="message-action-btn" title="Reply"><MessageSquare size={16} /></button>
                  <button className="message-action-btn" title="More"><MoreHorizontalIcon size={16} /></button>
                </div>
              </div>
            </React.Fragment>
          )
        })}
      </div>
    </div>
  )
}
