import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { PartyPopper } from 'lucide-react'
import { SearchIcon, PlusIcon, ChevronDownIcon, PencilIcon } from '../components/slack-icons'
import api from '../api/axios'
import ResizableHandle from '../components/ResizableHandle'
import usePageTitle from '../hooks/usePageTitle'
import '../styles/DMsListPage.css'

export default function DMsListPage() {
  usePageTitle('DMs')
  const [dms, setDms] = useState([])
  const [loading, setLoading] = useState(true)

  const defaultWidth = 352
  const minWidth = 319.2
  const maxWidth = 719.2

  useEffect(() => {
    // Fetch DM conversations list from API
    setLoading(true)
    api.get('/api/direct-messages/conversations').then(res => {
      console.log('DM Conversations API response:', res.data)
      
      if (!res.data || res.data.length === 0) {
        console.log('No DM conversations found')
        setDms([])
        setLoading(false)
        return
      }
      
      const conversations = res.data.map(conv => ({
        id: conv.user_id,
        name: conv.username,
        status: conv.status || 'offline',
        preview: conv.last_message?.content || 'No messages yet',
        unreadCount: conv.unread_count || 0,
        lastMessageTime: conv.last_message?.timestamp,
        profilePic: conv.profile_picture || conv.avatar || null,
        isYou: false
      }))
      
      console.log('Mapped conversations:', conversations)
      setDms(conversations)
      setLoading(false)
    }).catch(err => {
      console.error('Error fetching conversations:', err)
      setLoading(false)
    })
  }, [])

  return (
    <div className="dms-list-page">
      {/* Child Sidebar */}
      <ResizableHandle minWidth={minWidth} maxWidth={maxWidth} defaultWidth={defaultWidth}>
        <div className="dms-sidebar">
          <div className="dms-sidebar-header">
            <h2>Direct messages</h2>
            <button className="dropdown-btn"><ChevronDownIcon size={14} /></button>
            <div className="header-actions">
              <label className="unread-toggle">
                <span>Unread messages</span>
                <input type="checkbox" />
                <span className="toggle-switch"></span>
              </label>
              <button className="icon-btn"><PencilIcon size={16} /></button>
            </div>
          </div>

          <div className="dm-search">
            <SearchIcon size={18} />
            <input type="text" placeholder="Find a DM" />
          </div>

          <div className="dm-invite-section">
            <div className="invite-icon"><PartyPopper size={20} /></div>
            <div className="invite-text">
              <strong>Anyone missing?</strong> Add your whole team and get the conversation started.
            </div>
            <button className="add-colleagues-btn">Add colleagues</button>
          </div>

          <div className="dm-list">
            {loading ? (
              <div style={{ padding: '20px', textAlign: 'center', color: '#616061' }}>
                Loading conversations...
              </div>
            ) : dms.length === 0 ? (
              <div style={{ padding: '20px', textAlign: 'center', color: '#616061' }}>
                No conversations yet
              </div>
            ) : (
              dms.map(dm => (
                <Link key={dm.id} to={`/dm/${dm.id}`} className="dm-list-item">
                  <div className="dm-item-avatar">
                    {dm.profilePic && (
                      <img src={dm.profilePic} alt={dm.name} className="dm-avatar-img" />
                    )}
                    <div className={`dm-status ${dm.status}`}></div>
                  </div>
                  <div className="dm-item-content">
                    <div className="dm-item-header">
                      <span className="dm-item-name">{dm.name}</span>
                      {dm.isYou && <span className="you-tag">(you)</span>}
                    </div>
                    <p className="dm-item-preview">{dm.preview}</p>
                  </div>
                </Link>
              ))
            )}
          </div>
        </div>
      </ResizableHandle>

      {/* Main Content */}
      <div className="dms-main-content">
        <div className="dms-empty-state">
          <img 
            src="/src/assets/empty-dms-dark-8363c29.svg" 
            alt="No DM selected"
            className="empty-state-svg"
          />
        </div>
      </div>
    </div>
  )
}
