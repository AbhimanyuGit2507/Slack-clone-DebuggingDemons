import React, { useState, useEffect, useRef } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { ArrowLeftIcon, SearchIcon, ArrowRightIcon, HelpIcon, HistoryIcon } from './slack-icons'
import { X, Info, Settings, MessageSquare, User } from 'lucide-react'
import api from '../api/axios'
import '../styles/TopNav.css'
import UserPopup from './UserPopup'

export default function TopNav() {
  const navigate = useNavigate()
  const location = useLocation()
  const [showHistoryPopup, setShowHistoryPopup] = useState(false)
  const [history, setHistory] = useState([])
  const [currentIndex, setCurrentIndex] = useState(-1)
  const historyPopupRef = useRef(null)
  
  // Search states
  const [showSearchModal, setShowSearchModal] = useState(false)
  const [showUserPopup, setShowUserPopup] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState({ channels: [], users: [], messages: [] })
  const [isSearching, setIsSearching] = useState(false)
  const searchInputRef = useRef(null)

  // Track navigation history
  useEffect(() => {
    setHistory(prev => {
      const newHistory = [...prev.slice(0, currentIndex + 1), location.pathname]
      return newHistory
    })
    setCurrentIndex(prev => prev + 1)
  }, [location.pathname])

  // Close popup when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (historyPopupRef.current && !historyPopupRef.current.contains(event.target)) {
        setShowHistoryPopup(false)
      }
    }

    if (showHistoryPopup) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [showHistoryPopup])

  // Focus search input when modal opens
  useEffect(() => {
    if (showSearchModal && searchInputRef.current) {
      searchInputRef.current.focus()
    }
  }, [showSearchModal])

  // Handle escape key to close modal
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && showSearchModal) {
        setShowSearchModal(false)
        setSearchQuery('')
      }
    }

    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [showSearchModal])

  // Search functionality with debounce
  useEffect(() => {
    const searchTimeout = setTimeout(async () => {
      if (searchQuery.trim().length >= 1) {
        setIsSearching(true)
        try {
          const [channelsRes, usersRes] = await Promise.all([
            api.get('/api/channels'),
            api.get('/api/users')
          ])

          const query = searchQuery.toLowerCase()
          
          // Filter channels
          const filteredChannels = channelsRes.data.filter(channel =>
            channel.name?.toLowerCase().includes(query) ||
            channel.description?.toLowerCase().includes(query) ||
            channel.topic?.toLowerCase().includes(query)
          ).slice(0, 8)

          // Filter users/people
          const filteredUsers = usersRes.data.filter(user =>
            user.username?.toLowerCase().includes(query) ||
            user.email?.toLowerCase().includes(query) ||
            user.full_name?.toLowerCase().includes(query) ||
            user.name?.toLowerCase().includes(query)
          ).slice(0, 8)

          setSearchResults({
            channels: filteredChannels,
            users: filteredUsers,
            messages: []
          })
        } catch (err) {
          console.error('Search error:', err)
        } finally {
          setIsSearching(false)
        }
      } else {
        setSearchResults({ channels: [], users: [], messages: [] })
        setIsSearching(false)
      }
    }, 200) // 200ms debounce

    return () => clearTimeout(searchTimeout)
  }, [searchQuery])

  const goBack = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1)
      navigate(history[currentIndex - 1])
    }
  }

  const goForward = () => {
    if (currentIndex < history.length - 1) {
      setCurrentIndex(prev => prev + 1)
      navigate(history[currentIndex + 1])
    }
  }

  const goToHistoryItem = (index) => {
    setCurrentIndex(index)
    navigate(history[index])
    setShowHistoryPopup(false)
  }

  const formatPath = (path) => {
    if (path === '/') return 'Home'
    if (path.startsWith('/channel/')) return `# ${path.replace('/channel/', '')}`
    if (path.startsWith('/dm/')) return `@ User ${path.replace('/dm/', '')}`
    return path
  }

  const handleSearchResultClick = (type, item) => {
    if (type === 'channel') {
      navigate(`/channel/${item.name}`)
    } else if (type === 'user') {
      navigate(`/dm/${item.id}`)
    }
    setSearchQuery('')
    setShowSearchModal(false)
  }

  const hasResults = searchResults.channels.length > 0 || searchResults.users.length > 0

  return (
    <header className="top-nav">
      <div className="nav-content">
        <div className="nav-left">
          <button 
            className="nav-btn" 
            onClick={goBack}
            disabled={currentIndex <= 0}
            style={{ opacity: currentIndex <= 0 ? 0.3 : 1 }}
          >
            <ArrowLeftIcon size={18} />
          </button>
          <button 
            className="nav-btn" 
            onClick={goForward}
            disabled={currentIndex >= history.length - 1}
            style={{ opacity: currentIndex >= history.length - 1 ? 0.3 : 1 }}
          >
            <ArrowRightIcon size={18} />
          </button>
          <div className="history-btn-wrapper" ref={historyPopupRef}>
            <button 
              className="nav-btn history-btn" 
              onClick={() => setShowHistoryPopup(!showHistoryPopup)}
            >
              <HistoryIcon size={18} />
            </button>
            
            {showHistoryPopup && (
              <div className="history-popup">
                <div className="history-popup-header">
                  <span>History</span>
                </div>
                <div className="history-popup-content">
                  {history.length === 0 ? (
                    <div className="history-empty">No history yet</div>
                  ) : (
                    history.map((path, index) => (
                      <div
                        key={index}
                        className={`history-item ${index === currentIndex ? 'active' : ''}`}
                        onClick={() => goToHistoryItem(index)}
                      >
                        <div className="history-item-icon">
                          {path.startsWith('/channel/') ? '#' : path.startsWith('/dm/') ? '@' : '🏠'}
                        </div>
                        <div className="history-item-text">
                          {formatPath(path)}
                        </div>
                      </div>
                    )).reverse()
                  )}
                </div>
              </div>
            )}
          </div>
          <div className="search-bar" onClick={() => setShowSearchModal(true)}>
            <SearchIcon size={16} />
            <span className="search-placeholder">Search across people, channels, files, workflows and more</span>
          </div>
        </div>
        <div className="nav-right">
          <button className="help-btn"><HelpIcon size={20} /></button>
          <div style={{ position: 'relative' }}>
            <button className="nav-btn" title="Account" onClick={() => setShowUserPopup(!showUserPopup)}>
              <User size={18} />
            </button>
            <UserPopup visible={showUserPopup} onClose={() => setShowUserPopup(false)} />
          </div>
        </div>
      </div>

      {/* Full Screen Search Modal */}
      {showSearchModal && (
        <div className="search-modal-overlay">
          <div className="search-modal">
            <div className="search-modal-header">
              <button className="search-nav-btn" onClick={goBack} disabled={currentIndex <= 0}>
                <ArrowLeftIcon size={18} />
              </button>
              <button className="search-nav-btn" onClick={goForward} disabled={currentIndex >= history.length - 1}>
                <ArrowRightIcon size={18} />
              </button>
              <button className="search-nav-btn" onClick={() => setShowHistoryPopup(!showHistoryPopup)}>
                <HistoryIcon size={18} />
              </button>
              
              <div className="search-modal-input-wrapper">
                <SearchIcon size={20} />
                <input
                  ref={searchInputRef}
                  type="text"
                  className="search-modal-input"
                  placeholder="Search across people, channels, files, workflows and more"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  autoFocus
                />
              </div>

              <button className="search-modal-close" onClick={() => {
                setShowSearchModal(false)
                setSearchQuery('')
              }}>
                <X size={20} />
              </button>
            </div>

            <div className="search-modal-content">
              {searchQuery.trim().length === 0 ? (
                <div className="search-modal-empty-state">
                  <div className="search-empty-icon">💡</div>
                  <h2 className="search-empty-title">Search messages, files and more</h2>
                  <p className="search-empty-text">
                    Looking for a particular message, doc or decision? If it happened in Slack, you can find it in search.
                  </p>

                  <div className="search-help-section">
                    <h3 className="search-help-header">From our Help Centre</h3>
                    
                    <div className="search-help-item">
                      <Info size={20} className="search-help-icon" />
                      <div className="search-help-content">
                        <div className="search-help-title">How to Search in Slack</div>
                        <div className="search-help-subtitle">Access the right information instantly</div>
                      </div>
                      <span className="search-help-badge">Enter</span>
                    </div>

                    <div className="search-help-item">
                      <Info size={20} className="search-help-icon" />
                      <div className="search-help-content">
                        <div className="search-help-title">Using Slack</div>
                        <div className="search-help-subtitle">Learn how Slack works from top to bottom</div>
                      </div>
                      <span className="search-help-badge">Enter</span>
                    </div>
                  </div>

                  <div className="search-help-footer">
                    <span className="search-help-nav">↑ ↓ Select</span>
                    <a href="#" className="search-help-link">Give feedback</a>
                  </div>
                </div>
              ) : isSearching ? (
                <div className="search-modal-loading">
                  <div className="search-loading-spinner"></div>
                  <p>Searching...</p>
                </div>
              ) : hasResults ? (
                <div className="search-modal-results">
                  {searchResults.channels.length > 0 && (
                    <div className="search-results-section">
                      <h3 className="search-results-header">Channels</h3>
                      {searchResults.channels.map(channel => (
                        <div
                          key={channel.id}
                          className="search-result-card"
                          onClick={() => handleSearchResultClick('channel', channel)}
                        >
                          <div className="search-result-icon-large">#</div>
                          <div className="search-result-details">
                            <div className="search-result-title">{channel.name}</div>
                            {channel.description && (
                              <div className="search-result-description">{channel.description}</div>
                            )}
                            <div className="search-result-meta">
                              {channel.is_private ? '🔒 Private channel' : 'Public channel'}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {searchResults.users.length > 0 && (
                    <div className="search-results-section">
                      <h3 className="search-results-header">People</h3>
                      {searchResults.users.map(user => (
                        <div
                          key={user.id}
                          className="search-result-card"
                          onClick={() => handleSearchResultClick('user', user)}
                        >
                          {user.profile_picture || user.avatar_url ? (
                            <img 
                              src={user.profile_picture || user.avatar_url} 
                              alt={user.username}
                              className="search-result-avatar-large"
                            />
                          ) : (
                            <div className="search-result-avatar-large">
                              {(user.full_name || user.name || user.username)?.[0]?.toUpperCase()}
                            </div>
                          )}
                          <div className="search-result-details">
                            <div className="search-result-title">
                              {user.full_name || user.name || user.username}
                            </div>
                            <div className="search-result-description">{user.email}</div>
                            {user.status_text && (
                              <div className="search-result-meta">
                                {user.status_emoji} {user.status_text}
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <div className="search-modal-no-results">
                  <p>No results found for "{searchQuery}"</p>
                  <span>Try different keywords or check your spelling</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  )
}
