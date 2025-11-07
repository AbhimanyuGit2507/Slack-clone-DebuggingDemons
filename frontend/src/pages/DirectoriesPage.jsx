import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Search, X, SlidersHorizontal, Edit, User } from 'lucide-react'
import api from '../api/axios'
import { useNavigate } from 'react-router-dom'
import usePageTitle from '../hooks/usePageTitle'
import '../styles/DirectoriesPage.css'

const DirectoriesPage = () => {
  usePageTitle('People & user groups')
  const [activeTab, setActiveTab] = useState('people')
  const [searchQuery, setSearchQuery] = useState('')
  const [people, setPeople] = useState([])
  const [channels, setChannels] = useState([])
  const [groups, setGroups] = useState([])
  const [loading, setLoading] = useState(true)
  const [showFilters, setShowFilters] = useState(false)
  const [sortBy, setSortBy] = useState('recommended')
  const [currentUser, setCurrentUser] = useState(null)

  useEffect(() => {
    fetchCurrentUser()
    fetchPeople()
    fetchChannels()
    fetchGroups()
  }, [])

  const fetchCurrentUser = async () => {
    try {
      const res = await api.get('/api/auth/me')
      setCurrentUser(res.data)
    } catch (err) {
      console.error('Error fetching current user:', err)
    }
  }

  const fetchChannels = async () => {
    try {
      const res = await api.get('/api/channels')
      setChannels(res.data || [])
    } catch (err) {
      console.error('Error fetching channels:', err)
      setChannels([])
    }
  }

  const fetchGroups = async () => {
    try {
      const res = await api.get('/api/groups')
      setGroups(res.data || [])
    } catch (err) {
      console.error('Error fetching groups:', err)
      setGroups([])
    }
  }

  const fetchPeople = async () => {
    try {
      setLoading(true)
      const res = await api.get('/api/users')
      console.log('Directories - Fetched users:', res.data)
      setPeople(res.data)
      setLoading(false)
    } catch (err) {
      console.error('Error fetching users:', err)
      setPeople([])
      setLoading(false)
    }
  }

  const filteredPeople = people.filter(person => 
    person.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
    person.email.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const filteredChannels = channels.filter(ch => (ch.name || '').toLowerCase().includes(searchQuery.toLowerCase()) || (ch.description || '').toLowerCase().includes(searchQuery.toLowerCase()))

  const filteredGroups = groups.filter(g => (g.name || '').toLowerCase().includes(searchQuery.toLowerCase()) || (g.handle || '').toLowerCase().includes(searchQuery.toLowerCase()))

  const isCurrentUser = (userId) => {
    return currentUser && currentUser.id === userId
  }

  const getStatusColor = (status) => {
    switch(status) {
      case 'online': return '#2ecc71'
      case 'away': return '#f39c12'
      case 'offline': return '#95a5a6'
      default: return '#95a5a6'
    }
  }

  const getInitials = (username) => {
    return username.charAt(0).toUpperCase()
  }
  const navigate = useNavigate()

  return (
    <motion.div 
      className="directories-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2 }}
    >
      {/* Header */}
      <div className="dir-header">
        <h1 className="dir-header-title">Directories</h1>
      </div>

      {/* Tabs Navigation */}
      <div className="dir-tabs">
        <button 
          className={`dir-tab-btn ${activeTab === 'people' ? 'dir-tab-active' : ''}`}
          onClick={() => setActiveTab('people')}
        >
          <User size={16} />
          <span>People</span>
        </button>
        <button 
          className={`dir-tab-btn ${activeTab === 'channels' ? 'dir-tab-active' : ''}`}
          onClick={() => setActiveTab('channels')}
        >
          <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
            <path d="M7.5 3h5v14h-5V3zm-4 4h3v10h-3V7zm11 0h3v10h-3V7z"/>
          </svg>
          <span>Channels</span>
        </button>
        <button 
          className={`dir-tab-btn ${activeTab === 'groups' ? 'dir-tab-active' : ''}`}
          onClick={() => setActiveTab('groups')}
        >
          <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
            <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
          </svg>
          <span>User groups</span>
        </button>
        <button 
          className={`dir-tab-btn ${activeTab === 'external' ? 'dir-tab-active' : ''}`}
          onClick={() => setActiveTab('external')}
        >
          <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
            <path d="M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2v9.67z"/>
          </svg>
          <span>External</span>
        </button>
        <button 
          className={`dir-tab-btn ${activeTab === 'invitations' ? 'dir-tab-active' : ''}`}
          onClick={() => setActiveTab('invitations')}
        >
          <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
            <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
          </svg>
          <span>Invitations</span>
        </button>
      </div>

      {/* Search and Invite Section */}
      <div className="dir-search-area">
        <div className="dir-search-container">
          <Search size={18} className="dir-search-icon" />
          <input 
            type="text"
            className="dir-search-input"
            placeholder="Search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {searchQuery && (
            <button 
              className="dir-search-clear"
              onClick={() => setSearchQuery('')}
            >
              <X size={16} />
            </button>
          )}
        </div>
        <button className="dir-invite-button">
          <span>Invite people</span>
        </button>
      </div>

      {/* Content based on active tab */}
  {activeTab === 'people' && (
        <>
          {/* Invite Section */}
          <div className="invite-section">
            <button className="invite-close-btn" onClick={() => document.querySelector('.invite-section').style.display = 'none'}>
              <X size={20} />
            </button>
            <h2 className="invite-title">Invite your team to Slack</h2>
            <p className="invite-description">Bring your team members into Slack to start working better together. Send invitations via email or get a handy link to share.</p>
            <button className="invite-people-btn">Invite people</button>
          </div>

          {/* Filters and Sort */}
          <div className="filters-bar">
            <div className="filter-buttons">
              <button className="filter-btn">
                <span>Title</span>
                <svg width="10" height="10" viewBox="0 0 10 10" fill="currentColor">
                  <path d="M5 7L1 3h8z"/>
                </svg>
              </button>
              <button className="filter-btn">
                <span>Location</span>
                <svg width="10" height="10" viewBox="0 0 10 10" fill="currentColor">
                  <path d="M5 7L1 3h8z"/>
                </svg>
              </button>
              <button className="filter-btn-icon">
                <SlidersHorizontal size={16} />
                Filters
              </button>
            </div>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              className="sort-select"
            >
              <option value="recommended">Most recommended</option>
              <option value="name-asc">Name (A-Z)</option>
              <option value="name-desc">Name (Z-A)</option>
              <option value="recent">Recently active</option>
            </select>
          </div>

          {/* People Grid */}
          <div className="people-grid">
            {loading ? (
              <div className="loading-state">Loading people...</div>
            ) : filteredPeople.length === 0 ? (
              <div className="empty-state">
                <p>No people found</p>
              </div>
            ) : (
              filteredPeople.map((person) => (
                <motion.div
                  key={person.id}
                  className="person-card"
                  onClick={() => navigate(`/dm/${person.id}`)}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  {isCurrentUser(person.id) && (
                    <button className="edit-btn">
                      <Edit size={14} />
                      Edit
                    </button>
                  )}
                  
                  <div className="person-avatar-wrapper">
                    {person.profile_picture ? (
                      <img 
                        src={person.profile_picture} 
                        alt={person.username}
                        className="person-avatar"
                      />
                    ) : (
                      <div 
                        className="person-avatar-placeholder"
                        style={{ backgroundColor: `hsl(${person.id * 37}, 70%, 50%)` }}
                      >
                        {getInitials(person.username)}
                      </div>
                    )}
                    {person.status === 'online' && (
                      <div className="status-indicator" />
                    )}
                  </div>

                  <h3 className="person-name">
                    {person.username}
                    {isCurrentUser(person.id) && (
                      <span className="you-badge">🌱</span>
                    )}
                  </h3>

                  {isCurrentUser(person.id) && (
                    <p className="person-label">That's you!</p>
                  )}
                </motion.div>
              ))
            )}
          </div>
        </>
      )}

      {/* Other tabs - placeholder */}
      {activeTab === 'channels' && (
        <div className="channels-container" style={{ padding: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <h2 style={{ margin: 0, color: '#d1d2d3' }}>All channels</h2>
            <div style={{ display: 'flex', gap: 8 }}>
              <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="sort-select">
                <option value="recommended">Most recommended</option>
                <option value="name-asc">Name (A-Z)</option>
                <option value="name-desc">Name (Z-A)</option>
              </select>
            </div>
          </div>

          {filteredChannels.length === 0 ? (
            <div className="empty-state">No channels found</div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 12 }}>
              {filteredChannels.map((ch) => {
                const isJoined = ch.members && Array.isArray(ch.members) && ch.members.find(m => m.id === currentUser?.id)
                return (
                  <div key={ch.id} style={{ background: '#0b0c0d', border: '1px solid rgba(255,255,255,0.04)', padding: 12, borderRadius: 8, display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }} onClick={() => navigate(`/channel/${ch.name}`)}>
                    <div>
                      <div style={{ fontSize: 16, fontWeight: 700, color: '#e6e7e8' }}># {ch.name}</div>
                      <div style={{ color: '#9ea4ac', fontSize: 13 }}>{ch.description || 'No description'}</div>
                      <div style={{ color: '#9ea4ac', fontSize: 12, marginTop: 6 }}>{(ch.members && ch.members.length) || 0} members · {ch.is_private ? 'Private' : 'Public'}</div>
                    </div>
                    <div style={{ display: 'flex', gap: 8 }}>
                      {isJoined ? (
                        <button className="dir-invite-button" onClick={async (e) => { e.stopPropagation(); try { await api.post(`/api/channels/${ch.id}/leave`); await fetchChannels() } catch(e){ console.error(e); alert('Leave failed') } }}>Leave</button>
                      ) : (
                        <button className="dir-invite-button" onClick={async (e) => { e.stopPropagation(); try { await api.post(`/api/channels/${ch.id}/join`); await fetchChannels() } catch(e){ console.error(e); alert('Join failed') } }}>Join</button>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}

      {activeTab === 'groups' && (
        <div style={{ padding: 24 }}>
          <h2 style={{ color: '#d1d2d3' }}>User groups</h2>
          {filteredGroups.length === 0 ? (
            <div className="empty-state">No user groups found</div>
          ) : (
            <div style={{ display: 'grid', gap: 12 }}>
              {filteredGroups.map(g => (
                <div key={g.id} style={{ background: '#0b0c0d', border: '1px solid rgba(255,255,255,0.04)', padding: 12, borderRadius: 8, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: 16, fontWeight: 700, color: '#e6e7e8' }}>{g.name} <span style={{ color: '#9ea4ac', fontSize: 13 }}>@{g.handle}</span></div>
                    <div style={{ color: '#9ea4ac', fontSize: 13 }}>{g.description || ''}</div>
                  </div>
                  <div>
                    <button className="dir-invite-button" onClick={() => alert('View members not implemented')}>View members</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'external' && (
        <div style={{ padding: 24 }}>
          <h2 style={{ color: '#d1d2d3' }}>External</h2>
          <p style={{ color: '#9ea4ac' }}>Integrations and external connections will be shown here. This area is a placeholder.</p>
        </div>
      )}

      {activeTab === 'invitations' && (
        <div style={{ padding: 24 }}>
          <h2 style={{ color: '#d1d2d3' }}>Invitations</h2>
          <p style={{ color: '#9ea4ac' }}>Manage pending invitations. There are no pending invites right now.</p>
        </div>
      )}
    </motion.div>
  )
}

export default DirectoriesPage
