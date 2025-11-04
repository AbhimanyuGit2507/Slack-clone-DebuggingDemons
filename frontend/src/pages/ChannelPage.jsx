import React, { useEffect, useState, useRef } from 'react'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { UserPlus, Mail, Users, MessageSquare, ClipboardList, Paperclip, Video, Mic, Underline, Strikethrough, Link2, List, ListOrdered, Code, Smile, AtSign, Image as ImageIcon } from 'lucide-react'
import { StarIcon, HeadphonesIcon, SearchIcon, BoldIcon, ItalicIcon, SendIcon, PlusIcon, HashtagIcon, ChevronDownIcon, MoreVerticalIcon, PencilIcon } from '../components/slack-icons'
import api from '../api/axios'
import Canvas from '../components/Canvas'
import RichTextComposer from '../components/RichTextComposer'
import ReactionBar from '../components/ReactionBar'
import usePageTitle from '../hooks/usePageTitle'
import '../styles/ChannelPage.css'

export default function ChannelPage({ channelId }){
  const params = useParams()
  const channelName = channelId || params.name
  const [messages, setMessages] = useState([])
  const [channel, setChannel] = useState({ name: 'new-channel', id: 1 })
  const [hoveredMessageId, setHoveredMessageId] = useState(null)
  
  usePageTitle(`#${channel?.name || 'channel'}`)
  const [activeTab, setActiveTab] = useState('messages')
  const channelContentRef = useRef(null)
  
  // Modal states
  const [showDescriptionModal, setShowDescriptionModal] = useState(false)
  const [showAddPeopleModal, setShowAddPeopleModal] = useState(false)
  const [showEmailModal, setShowEmailModal] = useState(false)
  const [showHuddleMenu, setShowHuddleMenu] = useState(false)
  const [showInviteModal, setShowInviteModal] = useState(false)
  const [showChannelMenu, setShowChannelMenu] = useState(false)
  const [description, setDescription] = useState('')
  const [addPeopleMode, setAddPeopleMode] = useState('specific') // 'all' or 'specific'
  const [peopleInput, setPeopleInput] = useState('')
  const [allUsers, setAllUsers] = useState([])
  const [filteredUsers, setFilteredUsers] = useState([])
  const [showUserDropdown, setShowUserDropdown] = useState(false)
  const [selectedUser, setSelectedUser] = useState(null)
  const [isStarred, setIsStarred] = useState(false)
  const [showSearchModal, setShowSearchModal] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [openCanvasId, setOpenCanvasId] = useState(null)

  const fetchMessages = async () => {
    if (channel?.id) {
      try {
        const res = await api.get(`/api/messages/channel/${channel.id}`)
        setMessages(res.data)
      } catch (err) {
        console.error('Error fetching messages:', err)
      }
    }
  }

  useEffect(()=>{
    if (channelName) {
      // Fetch channel details by name
      api.get(`/api/channels/${channelName}`).then(res => {
        setChannel(res.data)
        setDescription(res.data.description || '')
        // Load starred state from localStorage
        const starredChannels = JSON.parse(localStorage.getItem('starredChannels') || '[]')
        setIsStarred(starredChannels.includes(res.data.id))
        
        // Check if we should auto-open canvas
        const canvasIdToOpen = localStorage.getItem('openCanvasInChannel')
        if (canvasIdToOpen) {
          setActiveTab('canvas')
          setOpenCanvasId(parseInt(canvasIdToOpen))
          localStorage.removeItem('openCanvasInChannel')
        }
      }).catch(err => {
        console.error('Error fetching channel:', err)
      })
    }
  }, [channelName])

  // Fetch messages when channel is loaded
  useEffect(() => {
    if (channel?.id) {
      fetchMessages()
    }
  }, [channel?.id])

  // Fetch all users for search
  useEffect(() => {
    api.get('/api/users').then(res => {
      setAllUsers(res.data)
    }).catch(err => {
      console.error('Error fetching users:', err)
    })
  }, [])

  // Filter users based on input
  useEffect(() => {
    if (peopleInput.trim()) {
      const searchTerm = peopleInput.toLowerCase()
      const filtered = allUsers.filter(user => 
        user.username?.toLowerCase().includes(searchTerm) ||
        user.email?.toLowerCase().includes(searchTerm) ||
        user.full_name?.toLowerCase().includes(searchTerm) ||
        user.name?.toLowerCase().includes(searchTerm)
      )
      setFilteredUsers(filtered)
      setShowUserDropdown(filtered.length > 0)
    } else {
      setFilteredUsers([])
      setShowUserDropdown(false)
    }
  }, [peopleInput, allUsers])

  // Close dropdowns on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest('.dropdown-menu') && !e.target.closest('.icon-btn') && !e.target.closest('.btn-huddle')) {
        setShowHuddleMenu(false)
        setShowChannelMenu(false)
      }
    }
    
    document.addEventListener('click', handleClickOutside)
    return () => document.removeEventListener('click', handleClickOutside)
  }, [])

  // Handle description update
  const handleSaveDescription = async () => {
    if (!channel?.id) return
    try {
      await api.put(`/api/channels/${channel.id}`, { description })
      setChannel({ ...channel, description })
      setShowDescriptionModal(false)
    } catch (err) {
      console.error('Error updating description:', err)
      alert('Failed to update description')
    }
  }

  // Handle adding people to channel
  const handleAddPeople = async () => {
    if (!channel?.id) return
    try {
      if (addPeopleMode === 'all') {
        // Add all workspace members
        for (const user of allUsers) {
          try {
            await api.post(`/api/channels/${channel.id}/invite`, { user_id: user.id })
          } catch (err) {
            console.error(`Failed to add user ${user.id}:`, err)
          }
        }
        await fetchMessages()
        setShowAddPeopleModal(false)
        setPeopleInput('')
        setSelectedUser(null)
      } else if (selectedUser) {
        await api.post(`/api/channels/${channel.id}/invite`, { user_id: selectedUser.id })
        
        // Refresh messages to show the system notification
        await fetchMessages()
        
        // Close modal and reset
        setShowAddPeopleModal(false)
        setPeopleInput('')
        setSelectedUser(null)
        setShowUserDropdown(false)
      }
    } catch (err) {
      console.error('Error adding people:', err)
      alert(err.response?.data?.detail || 'Failed to add people to channel')
    }
  }

  const handleSelectUser = (user) => {
    setSelectedUser(user)
    setPeopleInput(user.full_name || user.name || user.username)
    setShowUserDropdown(false)
  }

  const handleToggleStar = async () => {
    try {
      const newStarredState = !isStarred
      setIsStarred(newStarredState)
      
      // Save to localStorage
      const starredChannels = JSON.parse(localStorage.getItem('starredChannels') || '[]')
      if (newStarredState) {
        // Add to starred
        if (!starredChannels.includes(channel.id)) {
          starredChannels.push(channel.id)
        }
      } else {
        // Remove from starred
        const index = starredChannels.indexOf(channel.id)
        if (index > -1) {
          starredChannels.splice(index, 1)
        }
      }
      localStorage.setItem('starredChannels', JSON.stringify(starredChannels))
      
      console.log(`Channel ${newStarredState ? 'starred' : 'unstarred'}`)
      
      // In a real implementation, also save to backend
      // await api.post(`/api/channels/${channel.id}/star`, { starred: newStarredState })
    } catch (err) {
      console.error('Error toggling star:', err)
    }
  }

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (channelContentRef.current) {
      channelContentRef.current.scrollTop = channelContentRef.current.scrollHeight
    }
  }, [messages])

  return (
    <motion.div 
      className="channel-page"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.2 }}
    >
      {/* Channel Header */}
      <motion.div 
        className="channel-header"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.1 }}
      >
        <div className="channel-info">
          <button 
            className="icon-btn" 
            title={isStarred ? "Unstar channel" : "Star channel"}
            onClick={handleToggleStar}
            style={{ color: isStarred ? '#FFD700' : 'rgba(255, 255, 255, 0.7)' }}
          >
            <StarIcon size={16} filled={isStarred} />
          </button>
          <h1 className="channel-name"># {channel.name}</h1>
        </div>
        <div className="channel-actions">
          <button className="btn-secondary" onClick={() => setShowInviteModal(true)}>
            <Users size={14} /> Invite teammates
          </button>
          <div style={{ position: 'relative' }}>
            <button className="btn-huddle" onClick={() => setShowHuddleMenu(!showHuddleMenu)}>
              <HeadphonesIcon size={14} /> Huddle <ChevronDownIcon size={12} />
            </button>
            {showHuddleMenu && (
              <div className="dropdown-menu">
                <div className="dropdown-item" onClick={async () => {
                  try {
                    const res = await api.post('/api/calls/start', {
                      channel_id: channel.id,
                      call_type: 'audio'
                    })
                    alert(`Audio huddle started! Join at: ${res.data.call_url}`)
                  } catch (err) {
                    console.error('Error starting huddle:', err)
                    alert('Failed to start huddle')
                  }
                  setShowHuddleMenu(false)
                }}>
                  <Mic size={16} />
                  <span>Start audio huddle</span>
                </div>
                <div className="dropdown-item" onClick={async () => {
                  try {
                    const res = await api.post('/api/calls/start', {
                      channel_id: channel.id,
                      call_type: 'video'
                    })
                    alert(`Video huddle started! Join at: ${res.data.call_url}`)
                  } catch (err) {
                    console.error('Error starting huddle:', err)
                    alert('Failed to start huddle')
                  }
                  setShowHuddleMenu(false)
                }}>
                  <Video size={16} />
                  <span>Start video huddle</span>
                </div>
              </div>
            )}
          </div>
          <button 
            className="icon-btn" 
            title="Search in channel"
            onClick={() => setShowSearchModal(true)}
          >
            <SearchIcon size={16} />
          </button>
          <div style={{ position: 'relative' }}>
            <button className="icon-btn" onClick={() => setShowChannelMenu(!showChannelMenu)}>
              <MoreVerticalIcon size={16} />
            </button>
            {showChannelMenu && (
              <div className="dropdown-menu">
                <div className="dropdown-item" onClick={() => {
                  setShowDescriptionModal(true)
                  setShowChannelMenu(false)
                }}>
                  <PencilIcon size={16} />
                  <span>Edit description</span>
                </div>
                <div className="dropdown-item" onClick={() => {
                  setShowAddPeopleModal(true)
                  setShowChannelMenu(false)
                }}>
                  <UserPlus size={16} />
                  <span>Add people</span>
                </div>
                <div className="dropdown-item" onClick={() => {
                  setShowEmailModal(true)
                  setShowChannelMenu(false)
                }}>
                  <Mail size={16} />
                  <span>Get email address</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </motion.div>

      {/* Channel Tabs */}
      <div className="channel-tabs">
        <button className={`tab ${activeTab === 'messages' ? 'active' : ''}`} onClick={() => setActiveTab('messages')}>
          <MessageSquare size={14} /> Messages
        </button>
        <button className={`tab ${activeTab === 'canvas' ? 'active' : ''}`} onClick={() => setActiveTab('canvas')}>
          <ClipboardList size={14} /> Canvas
        </button>
        <button className="tab"><PlusIcon size={14} /></button>
      </div>

      {/* Channel Content */}
      {activeTab === 'messages' && (
        <div className="channel-content" ref={channelContentRef}>
        
        {/* Optional: Welcome Section for templates */}
        <div className="welcome-section" style={{display: 'none'}}>
          <h2 className="welcome-title">👋 Welcome to your first channel!</h2>
          <p className="welcome-subtitle">
            Channels keep work focused around a specific topic. Pick a template to get started, or <Link to="#">see all</Link>.
          </p>

          <div className="template-grid">
            <div className="template-card teal">
              <div className="card-header">
                <h3>Run a project</h3>
                <p>Project starter kit template</p>
              </div>
              <div className="card-preview">
                <div className="preview-content">
                  <div className="preview-item"><span className="preview-icon">👥</span> Team</div>
                  <div className="preview-item"><span className="preview-icon">📄</span> Documents</div>
                  <div className="preview-item"><span className="preview-icon">🎯</span> Milestones</div>
                </div>
              </div>
            </div>

            <div className="template-card green">
              <div className="card-header">
                <h3>Chat with your team</h3>
                <p>Team support template</p>
              </div>
              <div className="card-preview">
                <div className="huddle-preview">
                  <div className="huddle-header">
                    <span className="huddle-icon">🎧</span>
                    <span>Weekly sync</span>
                  </div>
                  <div className="huddle-participants">
                    <div className="participant-avatar"></div>
                    <div className="join-badge">Join huddle</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="template-card orange">
              <div className="card-header">
                <h3>Collaborate with external partners</h3>
                <p>External partner template</p>
              </div>
              <div className="card-preview">
                <div className="preview-channel">
                  <div className="channel-line"></div>
                  <div className="channel-avatars">
                    <span className="mini-avatar"></span>
                    <span className="mini-avatar"></span>
                  </div>
                </div>
              </div>
            </div>

            <div className="template-card purple">
              <div className="card-header">
                <h3>Invite teammates</h3>
                <p>Add your whole team</p>
              </div>
              <div className="card-preview">
                <div className="avatars-group">
                  <div className="avatar-circle pink"></div>
                  <div className="avatar-circle blue"></div>
                  <div className="avatar-circle yellow"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Message Feed */}
        <div className="message-feed">
          {/* Channel Beginning Section */}
          <div className="channel-beginning">
            <h2 className="channel-beginning-title"># {channel.name}</h2>
            <p className="channel-beginning-subtitle">
              {channel.description || `You created this channel today. This is the very beginning of the # ${channel.name} channel.`}
            </p>
            <div className="channel-beginning-actions">
              <button className="channel-action-btn" onClick={() => setShowDescriptionModal(true)}>
                <PencilIcon size={16} />
                Add description
              </button>
              <button className="channel-action-btn" onClick={() => setShowAddPeopleModal(true)}>
                <UserPlus size={16} />
                Add people to channel
              </button>
              <button className="channel-action-btn" onClick={() => setShowEmailModal(true)}>
                <Mail size={16} />
                Send emails to channel
              </button>
            </div>
          </div>

          <div className="date-divider">
            <button className="date-btn">Today <ChevronDownIcon size={14} /></button>
          </div>

          {messages.map(msg => (
      <div key={msg.id} className={`message ${msg.is_system_message ? 'system-message' : ''}`}
        style={{ position: 'relative' }}
        onMouseEnter={() => setHoveredMessageId(msg.id)}
        onMouseLeave={() => setHoveredMessageId(prev => prev === msg.id ? null : prev)}>
              {msg.user?.profile_picture || msg.user?.avatar_url ? (
                <img 
                  src={msg.user.profile_picture || msg.user.avatar_url} 
                  alt={msg.user.name || 'User'}
                  className="message-avatar-img"
                />
              ) : (
                <div className="message-avatar">
                  {msg.user?.name?.charAt(0) || msg.user?.username?.charAt(0) || 'U'}
                </div>
              )}
              <div className="message-content">
                <div className="message-header">
                  <span className="author">{msg.user?.name || msg.user?.full_name || msg.user?.username || 'User'}</span>
                  <span className="timestamp">{new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                </div>
                {msg.formatted_content ? (
                  <div className="message-text" dangerouslySetInnerHTML={{ __html: msg.formatted_content }} />
                ) : (
                  <p className="message-text">{msg.content}</p>
                )}
                {/* Reaction bar shown under each message. The hover picker appears when the
                    message is hovered; the inline pills are shown only if reactions exist. */}
                <ReactionBar messageId={msg.id} onChange={fetchMessages} isHovered={hoveredMessageId === msg.id} />
              </div>
            </div>
          ))}

          {messages.length === 0 && (
            <div className="message">
              <div className="message-avatar">a</div>
              <div className="message-content">
                <div className="message-header">
                  <span className="author">aditya shukla</span>
                  <span className="timestamp">17:55</span>
                </div>
                <p className="message-text">joined #{channel.name}.</p>
              </div>
            </div>
          )}
        </div>

        {/* Message Input */}
        <RichTextComposer 
          channelId={channel.id} 
          channelName={channel.name}
          onSent={fetchMessages}
        />
        </div>
      )}

      {/* Canvas View */}
      <div style={{ display: activeTab === 'canvas' ? 'block' : 'none' }}>
        <Canvas channelId={channel?.id} canvasId={openCanvasId} />
      </div>

      {/* Edit Description Modal */}
      {showDescriptionModal && (
        <div className="modal-overlay" onClick={() => setShowDescriptionModal(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Edit description</h2>
              <button className="modal-close" onClick={() => setShowDescriptionModal(false)}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <input
                type="text"
                className="modal-input"
                placeholder="Add a description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                autoFocus
              />
              <p className="modal-help-text">Let people know what this channel is for.</p>
            </div>
            <div className="modal-footer">
              <button className="modal-btn modal-btn-secondary" onClick={() => setShowDescriptionModal(false)}>
                Cancel
              </button>
              <button className="modal-btn modal-btn-primary" onClick={handleSaveDescription}>
                Save
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add People Modal */}
      {showAddPeopleModal && (
        <div className="modal-overlay" onClick={() => setShowAddPeopleModal(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Add people to # {channel.name}</h2>
              <button className="modal-close" onClick={() => setShowAddPeopleModal(false)}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                </svg>
              </button>
            </div>
            <div className="modal-subtitle"># {channel.name}</div>
            <div className="modal-body">
              <div className="modal-radio-group">
                <label className="modal-radio-option">
                  <input
                    type="radio"
                    name="addPeopleMode"
                    value="all"
                    checked={addPeopleMode === 'all'}
                    onChange={(e) => setAddPeopleMode(e.target.value)}
                  />
                  <span className="modal-radio-label">Add all members of Debugging Demons</span>
                </label>
                <label className="modal-radio-option">
                  <input
                    type="radio"
                    name="addPeopleMode"
                    value="specific"
                    checked={addPeopleMode === 'specific'}
                    onChange={(e) => setAddPeopleMode(e.target.value)}
                  />
                  <span className="modal-radio-label">Add specific people</span>
                </label>
              </div>
              {addPeopleMode === 'specific' && (
                <div className="user-search-container">
                  <input
                    type="text"
                    className="modal-input"
                    placeholder="e.g. Nathalie, or james@a1company.com"
                    value={peopleInput}
                    onChange={(e) => setPeopleInput(e.target.value)}
                    onFocus={() => peopleInput && setShowUserDropdown(filteredUsers.length > 0)}
                  />
                  {showUserDropdown && filteredUsers.length > 0 && (
                    <div className="user-dropdown">
                      {filteredUsers.map(user => (
                        <div
                          key={user.id}
                          className="user-dropdown-item"
                          onClick={() => handleSelectUser(user)}
                        >
                          {user.profile_picture || user.avatar_url ? (
                            <img src={user.profile_picture || user.avatar_url} alt={user.username} className="user-dropdown-avatar" />
                          ) : (
                            <div className="user-dropdown-avatar">{(user.full_name || user.name || user.username)?.[0]?.toUpperCase()}</div>
                          )}
                          <div className="user-dropdown-info">
                            <div className="user-dropdown-name">{user.full_name || user.name || user.username}</div>
                            <div className="user-dropdown-email">{user.email}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
            <div className="modal-footer">
              <button className="modal-btn modal-btn-primary" onClick={handleAddPeople}>
                Add
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Send Emails Modal */}
      {showEmailModal && (
        <div className="modal-overlay" onClick={() => setShowEmailModal(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Send emails to #{channel.name}</h2>
              <button className="modal-close" onClick={() => setShowEmailModal(false)}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <p className="modal-text">
                Emails sent to this email address will be posted in the #{channel.name} channel.{' '}
                <a href="#" className="modal-link">How to use this address</a>.
              </p>
            </div>
            <div className="modal-footer">
              <button className="modal-btn modal-btn-primary" onClick={() => {
                // TODO: Get email address
                console.log('Getting email address for channel')
                setShowEmailModal(false)
              }}>
                Get email address
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Invite Teammates Modal */}
      {showInviteModal && (
        <div className="modal-overlay" onClick={() => setShowInviteModal(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Invite teammates to #{channel.name}</h2>
              <button className="modal-close" onClick={() => setShowInviteModal(false)}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <div className="user-search-container">
                <input
                  type="text"
                  className="modal-input"
                  placeholder="Search for people by name or email"
                  value={peopleInput}
                  onChange={(e) => setPeopleInput(e.target.value)}
                  onFocus={() => peopleInput && setShowUserDropdown(filteredUsers.length > 0)}
                  autoFocus
                />
                {showUserDropdown && filteredUsers.length > 0 && (
                  <div className="user-dropdown">
                    {filteredUsers.map(user => (
                      <div
                        key={user.id}
                        className="user-dropdown-item"
                        onClick={() => handleSelectUser(user)}
                      >
                        {user.profile_picture || user.avatar_url ? (
                          <img src={user.profile_picture || user.avatar_url} alt={user.username} className="user-dropdown-avatar" />
                        ) : (
                          <div className="user-dropdown-avatar">{(user.full_name || user.name || user.username)?.[0]?.toUpperCase()}</div>
                        )}
                        <div className="user-dropdown-info">
                          <div className="user-dropdown-name">{user.full_name || user.name || user.username}</div>
                          <div className="user-dropdown-email">{user.email}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              <p className="modal-help-text">
                Once they accept the invitation, they'll join this channel.
              </p>
            </div>
            <div className="modal-footer">
              <button className="modal-btn modal-btn-secondary" onClick={() => setShowInviteModal(false)}>
                Cancel
              </button>
              <button 
                className="modal-btn modal-btn-primary" 
                onClick={handleAddPeople}
                disabled={!selectedUser}
              >
                Send invitation
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Search in Channel Modal */}
      {showSearchModal && (
        <div className="modal-overlay" onClick={() => setShowSearchModal(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Search in #{channel.name}</h2>
              <button className="modal-close" onClick={() => setShowSearchModal(false)}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <input
                type="text"
                className="modal-input"
                placeholder="Search messages..."
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value)
                  // Filter messages in real-time
                  if (e.target.value.trim()) {
                    const query = e.target.value.toLowerCase()
                    const results = messages.filter(msg => 
                      msg.content?.toLowerCase().includes(query) ||
                      msg.user?.username?.toLowerCase().includes(query)
                    )
                    setSearchResults(results)
                  } else {
                    setSearchResults([])
                  }
                }}
                autoFocus
              />
              <div style={{ marginTop: '20px', maxHeight: '400px', overflowY: 'auto' }}>
                {searchQuery.trim() && searchResults.length > 0 ? (
                  <div>
                    <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '12px' }}>
                      Found {searchResults.length} message{searchResults.length !== 1 ? 's' : ''}
                    </p>
                    {searchResults.map(msg => (
                      <div 
                        key={msg.id} 
                        style={{
                          padding: '12px',
                          background: 'rgba(255,255,255,0.03)',
                          borderRadius: '8px',
                          marginBottom: '8px',
                          cursor: 'pointer'
                        }}
                        onClick={() => {
                          setShowSearchModal(false)
                          // Scroll to message in channel
                          document.getElementById(`message-${msg.id}`)?.scrollIntoView({ behavior: 'smooth' })
                        }}
                      >
                        <div style={{ fontSize: '14px', fontWeight: '600', marginBottom: '4px' }}>
                          {msg.user?.username || 'Unknown'}
                        </div>
                        <div style={{ fontSize: '13px', color: 'rgba(255,255,255,0.8)' }}>
                          {msg.content}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : searchQuery.trim() ? (
                  <p style={{ color: 'rgba(255,255,255,0.6)', textAlign: 'center' }}>
                    No messages found
                  </p>
                ) : (
                  <p style={{ color: 'rgba(255,255,255,0.6)', textAlign: 'center' }}>
                    Type to search messages in this channel
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </motion.div>
  )
}
