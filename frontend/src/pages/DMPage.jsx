import React, { useEffect, useState, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { MessageSquare, ClipboardList, Paperclip, Video, Mic, Underline, Strikethrough, Link2, List, ListOrdered, Code, Smile, AtSign, Image as ImageIcon, User, Mail, X, Clock, Users as UsersIcon } from 'lucide-react'
import { StarIcon, HeadphonesIcon, SearchIcon, BoldIcon, ItalicIcon, SendIcon, PlusIcon, ChevronDownIcon, MoreVerticalIcon, MoreHorizontalIcon } from '../components/slack-icons'
import api from '../api/axios'
import ResizableHandleRight from '../components/ResizableHandleRight'
import Canvas from '../components/Canvas'
import RichTextComposer from '../components/RichTextComposer'
import usePageTitle from '../hooks/usePageTitle'
import '../styles/DMPage.css'

export default function DMPage({ userId }){
  const params = useParams()
  const id = userId || params.id
  const [messages, setMessages] = useState([])
  const [contact, setContact] = useState(null)
  
  usePageTitle(contact?.username || 'DM')
  const [showProfile, setShowProfile] = useState(false)
  const [profileWidth, setProfileWidth] = useState(400)
  const [activeTab, setActiveTab] = useState('messages')
  const [isStarred, setIsStarred] = useState(false)
  const dmContentRef = useRef(null)

  const fetchMessages = async () => {
    if (id) {
      try {
        const res = await api.get(`/api/direct-messages/conversation/${id}`)
        setMessages(res.data)
      } catch (err) {
        console.error('Error fetching messages:', err)
      }
    }
  }

  useEffect(()=>{
    if (id) {
      // Fetch contact/user info
      api.get(`/api/users/${id}`).then(res => {
        setContact({
          ...res.data,
          name: res.data.full_name || res.data.name || res.data.username,
          email: res.data.email || 'user@example.com',
          status: res.data.status_text || res.data.status || 'Active',
          localTime: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) + ' local time',
          profile_picture: res.data.profile_picture || res.data.avatar || null
        })
        
        // Load starred state from localStorage
        const starredChannels = JSON.parse(localStorage.getItem('starredChannels') || '[]')
        setIsStarred(starredChannels.includes(`dm-${id}`))
      }).catch((err) => {
        console.error('Error fetching user:', err)
      })

      // Fetch direct messages conversation with this user
      fetchMessages()
    }
  }, [id])

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (dmContentRef.current) {
      dmContentRef.current.scrollTop = dmContentRef.current.scrollHeight
    }
  }, [messages])

  const handleToggleStar = async () => {
    const newStarredState = !isStarred
    setIsStarred(newStarredState)
    
    const starredChannels = JSON.parse(localStorage.getItem('starredChannels') || '[]')
    const dmId = `dm-${id}`
    
    if (newStarredState) {
      if (!starredChannels.includes(dmId)) {
        starredChannels.push(dmId)
      }
    } else {
      const index = starredChannels.indexOf(dmId)
      if (index > -1) {
        starredChannels.splice(index, 1)
      }
    }
    
    localStorage.setItem('starredChannels', JSON.stringify(starredChannels))
  }

  // Show loading state while contact data is being fetched
  if (!contact) {
    return (
      <div className="dm-page" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <motion.div 
      className="dm-page" 
      style={{ marginRight: showProfile ? `${profileWidth}px` : '0' }}
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.2 }}
    >
      {/* DM Header */}
      <motion.div 
        className="dm-header"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.1 }}
      >
        <div className="dm-info">
          <button className="icon-btn" onClick={handleToggleStar}>
            <StarIcon size={16} className={isStarred ? 'starred' : ''} />
          </button>
          <h1 className="dm-name">{contact.name}</h1>
        </div>
        <div className="dm-actions">
          <button className="btn-huddle"><HeadphonesIcon size={14} /> Huddle <ChevronDownIcon size={12} /></button>
          <button className="icon-btn"><SearchIcon size={16} /></button>
          <button className="icon-btn"><MoreVerticalIcon size={16} /></button>
        </div>
      </motion.div>

      {/* DM Tabs */}
      <div className="dm-tabs">
        <button className={`tab ${activeTab === 'messages' ? 'active' : ''}`} onClick={() => setActiveTab('messages')}>
          <MessageSquare size={14} /> Messages
        </button>
        <button className={`tab ${activeTab === 'canvas' ? 'active' : ''}`} onClick={() => setActiveTab('canvas')}>
          <ClipboardList size={14} /> Canvas
        </button>
        <button className="tab"><PlusIcon size={14} /></button>
      </div>

      {/* DM Content */}
      {activeTab === 'messages' && (
        <div className="dm-content" ref={dmContentRef}>

        {/* Message Feed */}
        <div className="message-feed">
          {/* Contact Profile Section */}
          <div className="dm-profile">
            <div className="dm-profile-header">
              <div className="dm-profile-avatar">
                {contact.profile_picture ? (
                  <img src={contact.profile_picture} alt={contact.name} style={{width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px'}} />
                ) : (
                  <User size={48} />
                )}
              </div>
              <div className="dm-profile-info">
                <h2 className="dm-profile-name">{contact.name}</h2>
                <p className="dm-profile-description">
                  This conversation is just between you and <a href="#">@{contact.name}</a>. Take a look at their profile to learn more about them.
                </p>
                <button className="view-profile-btn" onClick={() => setShowProfile(true)}>View profile</button>
              </div>
            </div>
          </div>

          {/* Welcome Card Section */}
          <div className="welcome-card">
            <div className="welcome-card-content">
              <div className="welcome-card-icon">
                <Mail size={24} />
              </div>
              <div className="welcome-card-text">
                <h3>Send a welcome card</h3>
                <p>A quick way to make your new teammate feel included and connected.</p>
              </div>
            </div>
            <button className="customize-card-btn">Customise card</button>
          </div>

          <div className="date-divider">
            <button className="date-btn">Yesterday <ChevronDownIcon size={14} /></button>
          </div>

          {/* Default first message */}
          <div className="message">
            <div className="message-avatar">
              {contact.profile_picture ? (
                <img src={contact.profile_picture} alt={contact.name} style={{width: '100%', height: '100%', objectFit: 'cover', borderRadius: '4px'}} />
              ) : (
                contact.name.charAt(0)
              )}
            </div>
            <div className="message-content">
              <div className="message-header">
                <span className="author">{contact.name}</span>
                <span className="timestamp">16:42</span>
              </div>
              <p className="message-text">
                accepted your invitation to join Slack - take a second to say hello. <a href="#">Don't notify me about this</a>
              </p>
            </div>
          </div>

          {messages.map(msg => (
            <div key={msg.id} className="message">
              <div className="message-avatar">
                {msg.user?.profile_picture ? (
                  <img src={msg.user.profile_picture} alt={msg.user.name} style={{width: '100%', height: '100%', objectFit: 'cover', borderRadius: '4px'}} />
                ) : (
                  msg.user?.name?.charAt(0) || 'U'
                )}
              </div>
              <div className="message-content">
                <div className="message-header">
                  <span className="author">{msg.user?.name || 'User'}</span>
                  <span className="timestamp">{new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                </div>
                {msg.formatted_content ? (
                  <div className="message-text" dangerouslySetInnerHTML={{ __html: msg.formatted_content }} />
                ) : (
                  <p className="message-text">{msg.content}</p>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Message Input */}
        <RichTextComposer 
          dmUserId={contact.id} 
          channelName={contact.name}
          onSent={fetchMessages}
        />
        </div>
      )}

      {/* Canvas View */}
      <div style={{ display: activeTab === 'canvas' ? 'block' : 'none' }}>
        <Canvas channelId={id ? -id : null} />
      </div>

      {/* Profile Sidebar */}
      {showProfile && (
        <ResizableHandleRight 
          minWidth={300} 
          maxWidth={800} 
          defaultWidth={400}
          onResize={(newWidth) => setProfileWidth(newWidth)}
        >
          <div className="profile-sidebar">
            <div className="profile-sidebar-header">
              <h2>Profile</h2>
              <button className="profile-close-btn" onClick={() => setShowProfile(false)}>
                <X size={20} />
              </button>
            </div>

          <div className="profile-sidebar-content">
            <div className="profile-avatar-large">
              {contact.profile_picture ? (
                <img src={contact.profile_picture} alt={contact.name} style={{width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px'}} />
              ) : (
                <User />
              )}
            </div>

            <h2 className="profile-name">{contact.name}</h2>

            <div className="profile-status">
              <span className="status-icon">🔕</span>
              <span>{contact.status}</span>
            </div>

            <div className="profile-time">
              <Clock size={16} />
              <span>{contact.localTime}</span>
            </div>

            <div className="profile-actions">
              <button className="profile-action-btn">
                <MessageSquare size={16} />
                <span>Message</span>
              </button>
              <button className="profile-action-btn">
                <HeadphonesIcon size={16} />
                <span>Huddle</span>
                <ChevronDownIcon size={12} />
              </button>
              <button className="profile-action-btn">
                <UsersIcon size={16} />
                <span>VIP</span>
              </button>
              <button className="profile-action-btn-icon">
                <MoreHorizontalIcon size={16} />
              </button>
            </div>

            <div className="profile-section">
              <h3>Contact information</h3>
              <div className="profile-info-item">
                <div className="profile-info-icon">
                  <Mail size={20} />
                </div>
                <div className="profile-info-content">
                  <div className="profile-info-label">Email address</div>
                  <a href={`mailto:${contact.email}`} className="profile-info-value">{contact.email}</a>
                </div>
              </div>
            </div>
          </div>
          </div>
        </ResizableHandleRight>
      )}
    </motion.div>
  )
}
