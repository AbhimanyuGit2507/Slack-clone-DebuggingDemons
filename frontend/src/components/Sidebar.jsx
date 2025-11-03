import React, { useEffect, useState, useRef } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { 
  Sparkles, 
  Ticket,
  X
} from 'lucide-react'
import { StarIcon, HashtagIcon, ChevronDownIcon, ChevronRightIcon, SettingsIcon, PencilIcon, HeadphonesIcon, UserDirectoryIcon } from './slack-icons'
import api from '../api/axios'
import CreateChannelModal from './CreateChannelModal'
import ResizableHandle from './ResizableHandle'
import '../styles/Sidebar.css'

export default function Sidebar(){
  const [channels, setChannels] = useState([])
  const [dms, setDms] = useState([])
  const [channelsExpanded, setChannelsExpanded] = useState(true)
  const [dmsExpanded, setDmsExpanded] = useState(true)
  const [appsExpanded, setAppsExpanded] = useState(true)
  const [starredExpanded, setStarredExpanded] = useState(true)
  const [showWorkspacePopup, setShowWorkspacePopup] = useState(false)
  const [showCreateChannel, setShowCreateChannel] = useState(false)
  const [starredChannels, setStarredChannels] = useState([])
  const [starredDms, setStarredDms] = useState([])
  const workspaceRef = useRef(null)
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(()=>{
    // Fetch user's channels
    api.get('/api/channels/my-channels').then(res => {
      setChannels(res.data)
      updateStarredItems(res.data, dms)
    }).catch(err => {
      console.error('Error fetching channels:', err)
    })

    // Fetch DM conversations (only users with actual conversations)
    api.get('/api/direct-messages/conversations').then(res => {
      console.log('Sidebar DM conversations:', res.data)
      const conversations = res.data.map(conv => ({
        id: conv.user_id,
        name: conv.username,
        status: conv.status || 'offline',
        presence: conv.status || 'offline',
        lastMessage: conv.last_message?.content || '',
        profilePic: conv.profile_picture || conv.avatar || null,
        isYou: false
      }))
      setDms(conversations)
      updateStarredItems(channels, conversations)
    }).catch(err => {
      console.error('Error fetching DM conversations:', err)
      setDms([])
    })
  }, [])

  // Update starred items from localStorage
  const updateStarredItems = (channelsList, dmsList) => {
    const starred = JSON.parse(localStorage.getItem('starredChannels') || '[]')
    const starredCh = channelsList.filter(ch => starred.includes(ch.id))
    const starredDm = dmsList.filter(dm => starred.includes(`dm-${dm.id}`))
    setStarredChannels(starredCh)
    setStarredDms(starredDm)
  }

  // Listen for storage changes
  useEffect(() => {
    const handleStorageChange = () => {
      updateStarredItems(channels, dms)
    }
    window.addEventListener('storage', handleStorageChange)
    // Also check periodically for same-tab changes
    const interval = setInterval(() => updateStarredItems(channels, dms), 1000)
    return () => {
      window.removeEventListener('storage', handleStorageChange)
      clearInterval(interval)
    }
  }, [channels, dms])

  // Close popup when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (workspaceRef.current && !workspaceRef.current.contains(event.target)) {
        setShowWorkspacePopup(false)
      }
    }

    if (showWorkspacePopup) {
      document.addEventListener('mousedown', handleClickOutside)
      return () => {
        document.removeEventListener('mousedown', handleClickOutside)
      }
    }
  }, [showWorkspacePopup])

  const isActive = (path) => location.pathname === path || location.pathname.startsWith(path)

  // Drag and drop handlers
  const handleDragStart = (e, item, type) => {
    e.dataTransfer.effectAllowed = 'move'
    e.dataTransfer.setData('application/json', JSON.stringify({ item, type }))
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const data = JSON.parse(e.dataTransfer.getData('application/json'))
    const { item, type } = data
    
    // Add to starred
    const starred = JSON.parse(localStorage.getItem('starredChannels') || '[]')
    const itemId = type === 'channel' ? item.id : `dm-${item.id}`
    
    if (!starred.includes(itemId)) {
      starred.push(itemId)
      localStorage.setItem('starredChannels', JSON.stringify(starred))
      updateStarredItems(channels, dms)
    }
  }

  const handleRemoveFromStarred = (item, type) => {
    const starred = JSON.parse(localStorage.getItem('starredChannels') || '[]')
    const itemId = type === 'channel' ? item.id : `dm-${item.id}`
    const index = starred.indexOf(itemId)
    
    if (index > -1) {
      starred.splice(index, 1)
      localStorage.setItem('starredChannels', JSON.stringify(starred))
      updateStarredItems(channels, dms)
    }
  }

  const defaultWidth = 352
  const minWidth = 319.2
  const maxWidth = 719.2

  // Filter out starred items from regular lists
  const regularChannels = channels.filter(ch => !starredChannels.some(s => s.id === ch.id))
  const regularDms = dms.filter(dm => !starredDms.some(s => s.id === dm.id))

  return (
    <ResizableHandle minWidth={minWidth} maxWidth={maxWidth} defaultWidth={defaultWidth}>
      <div className="sidebar">
      <div className="sidebar-header">
        <div 
          ref={workspaceRef}
          className="sidebar-workspace"
          onClick={() => setShowWorkspacePopup(!showWorkspacePopup)}
        >
          <span className="workspace-name">Debugging Demons</span>
          <span className="dropdown-arrow"><ChevronDownIcon size={14} /></span>
          
          {showWorkspacePopup && (
            <div className="workspace-popup">
              <div className="workspace-popup-header">
                <div className="workspace-popup-icon">DD</div>
                <div className="workspace-popup-info">
                  <strong>Debugging Demons</strong>
                  <span>debuggingdemons.slack.com</span>
                </div>
              </div>

              <div className="workspace-popup-trial">
                <p>Your workspace is currently on Slack's <strong>Pro trial</strong>.</p>
                <a href="#">Learn more</a>
              </div>

              <div className="workspace-popup-offer">
                <span><Ticket size={16} /> Get 55% off a paid subscription for a limited time.</span>
                <a href="#">See subscription details</a>
              </div>

              <button className="workspace-upgrade-btn">
                <Sparkles size={18} color="white" />
                Upgrade now
              </button>

              <div className="workspace-popup-section">
                <button className="workspace-popup-item">Invite people to Debugging Demons</button>
                <button className="workspace-popup-item">Preferences</button>
                <button className="workspace-popup-item">
                  <span>Tools & settings</span>
                  <ChevronRightIcon size={16} />
                </button>
              </div>

              <div className="workspace-popup-section">
                <button className="workspace-popup-item">
                  <span>Open the desktop app</span>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <circle cx="10" cy="10" r="8" fill="#e01e5a"/>
                    <circle cx="10" cy="10" r="4" fill="white"/>
                  </svg>
                </button>
                <button className="workspace-popup-item">
                  <span>Get the mobile app</span>
                  <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                    <rect x="6" y="2" width="8" height="16" rx="2" fill="currentColor"/>
                  </svg>
                </button>
              </div>

              <div className="workspace-popup-section">
                <button className="workspace-popup-item workspace-signout">Sign out</button>
              </div>
            </div>
          )}
        </div>
        <div className="header-actions">
          <button className="sidebar-header-btn"><SettingsIcon size={18} /></button>
          <button className="sidebar-header-btn"><PencilIcon size={18} /></button>
        </div>
      </div>

      <div className="trial-banner">
        <Sparkles className="trial-icon" size={20} />
        <span className="trial-text">30 days left in trial</span>
        <ChevronRightIcon className="arrow" size={16} />
      </div>

      <div className="sidebar-menu">
        <button className="sidebar-menu-item">
          <HeadphonesIcon size={18} />
          <span>Huddles</span>
        </button>
        <Link to="/directories" className="sidebar-menu-item" style={{ textDecoration: 'none', color: 'inherit' }}>
          <UserDirectoryIcon size={18} />
          <span>Directories</span>
        </Link>
      </div>

      <div className="sidebar-starred">
        <button 
          className="sidebar-starred-header"
          onClick={() => setStarredExpanded(!starredExpanded)}
        >
          <ChevronRightIcon size={18} className={starredExpanded ? 'rotate-90' : ''} />
          <StarIcon size={18} />
          <span>Starred</span>
        </button>
        {starredExpanded && (
          <div 
            className="starred-dropzone"
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            {(starredChannels.length === 0 && starredDms.length === 0) ? (
              <div className="starred-empty">Drag and drop important stuff here</div>
            ) : (
              <div className="starred-items">
                {starredChannels.map(channel => (
                  <Link 
                    key={channel.id} 
                    to={`/channel/${channel.name}`} 
                    className={`sidebar-item ${isActive(`/channel/${channel.name}`) ? 'active' : ''}`}
                    draggable
                    onDragStart={(e) => handleDragStart(e, channel, 'channel')}
                  >
                    <HashtagIcon size={18} />
                    <span>{channel.name}</span>
                    <button 
                      className="starred-remove"
                      onClick={(e) => {
                        e.preventDefault()
                        handleRemoveFromStarred(channel, 'channel')
                      }}
                    >
                      <X size={14} />
                    </button>
                  </Link>
                ))}
                {starredDms.map(dm => (
                  <Link 
                    key={dm.id} 
                    to={`/dm/${dm.id}`} 
                    className={`sidebar-item ${isActive(`/dm/${dm.id}`) ? 'active' : ''}`}
                    draggable
                    onDragStart={(e) => handleDragStart(e, dm, 'dm')}
                  >
                    {dm.profilePic ? (
                      <img src={dm.profilePic} alt={dm.name} className="dm-avatar"/>
                    ) : (
                      <div className="dm-avatar-placeholder">{dm.name?.[0]?.toUpperCase()}</div>
                    )}
                    <span>{dm.name}</span>
                    <span className={`presence-indicator ${dm.presence}`}></span>
                    <button 
                      className="starred-remove"
                      onClick={(e) => {
                        e.preventDefault()
                        handleRemoveFromStarred(dm, 'dm')
                      }}
                    >
                      <X size={14} />
                    </button>
                  </Link>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      <nav className="sidebar-sections">
        <div className="sidebar-section">
          <div className="sidebar-section-header" onClick={() => setChannelsExpanded(!channelsExpanded)}>
            {channelsExpanded ? <ChevronDownIcon size={14} className="section-caret" /> : <ChevronRightIcon size={14} className="section-caret" />}
            <span>Channels</span>
          </div>
          {channelsExpanded && (
            <>
              {regularChannels.map(channel => (
                <Link 
                  key={channel.id} 
                  to={`/channel/${channel.name}`} 
                  className={`sidebar-item ${isActive(`/channel/${channel.name}`) ? 'active' : ''}`}
                  draggable
                  onDragStart={(e) => handleDragStart(e, channel, 'channel')}
                >
                  <span className="item-hash"><HashtagIcon size={18} /></span>
                  <span>{channel.name}</span>
                </Link>
              ))}
              <button className="sidebar-add-btn" onClick={() => setShowCreateChannel(true)}>
                <span className="add-icon">+</span>
                <span>Add channels</span>
              </button>
            </>
          )}
        </div>

        <div className="sidebar-section">
          <div className="sidebar-section-header" onClick={() => setDmsExpanded(!dmsExpanded)}>
            {dmsExpanded ? <ChevronDownIcon size={14} className="section-caret" /> : <ChevronRightIcon size={14} className="section-caret" />}
            <span>Direct messages</span>
          </div>
          {dmsExpanded && regularDms.map(dm => (
            <Link 
              key={dm.id} 
              to={`/dm/${dm.id}`} 
              className={`sidebar-item ${isActive(`/dm/${dm.id}`) ? 'active' : ''}`}
              draggable
              onDragStart={(e) => handleDragStart(e, dm, 'dm')}
            >
              <div className="dm-avatar">
                {dm.profilePic ? (
                  <img src={dm.profilePic} alt={dm.name} className="dm-avatar-img" />
                ) : (
                  <span>{dm.name.charAt(0)}</span>
                )}
                <div className={`dm-presence ${dm.status}`}></div>
              </div>
              <span>{dm.name}</span>
              {dm.isYou && <span className="dm-you-label">you</span>}
            </Link>
          ))}
          <button className="sidebar-add-btn">
            <span className="add-icon">+</span>
            <span>Invite people</span>
          </button>
        </div>

        <div className="sidebar-section">
          <div className="sidebar-section-header" onClick={() => setAppsExpanded(!appsExpanded)}>
            {appsExpanded ? <ChevronDownIcon size={14} className="section-caret" /> : <ChevronRightIcon size={14} className="section-caret" />}
            <span>Apps</span>
          </div>
          {appsExpanded && (
            <>
              <Link to="/apps/slackbot" className="sidebar-item">
                <div className="app-icon">
                  <svg width="18" height="18" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z"/>
                  </svg>
                </div>
                <span>Slackbot</span>
                <span className="app-badge">1</span>
              </Link>
              <button className="sidebar-add-btn">
                <span className="add-icon">+</span>
                <span>Add apps</span>
              </button>
            </>
          )}
        </div>
      </nav>

      <div className="sidebar-footer">
        <p>Slack works better when you use it together.</p>
        <button className="invite-btn">👥 Invite teammates</button>
      </div>

      <CreateChannelModal
        isOpen={showCreateChannel}
        onClose={() => setShowCreateChannel(false)}
        onCreate={(channelData) => {
          // Create a new channel and navigate to it
          const newId = channels.length + 4
          const newChannel = {
            id: newId,
            name: channelData.name,
            template: channelData.template
          }
          setChannels([...channels, newChannel])
          navigate(`/channel/${channelData.name}`)
        }}
      />
    </div>
    </ResizableHandle>
  )
}
