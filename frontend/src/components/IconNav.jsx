import React, { useState, useEffect, useRef } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Wrench, User, UserPlus } from 'lucide-react'
import { HomeIcon, PlusIcon, BellIcon, DirectMessagesIcon, ChevronDownIcon, MoreHorizontalIcon, ChevronRightIcon, MessageIcon, FilesIcon } from './slack-icons'
import '../styles/IconNav.css'
import UserPopup from './UserPopup'
import api from '../api/axios'

export default function IconNav() {
  const location = useLocation()
  const navigate = useNavigate()
  const [showMorePopup, setShowMorePopup] = useState(false)
  const [hoveredItem, setHoveredItem] = useState(null)
  const [unreadMessagesOnly, setUnreadMessagesOnly] = useState(false)
  const [unreadActivityOnly, setUnreadActivityOnly] = useState(false)
  const [dmsList, setDmsList] = useState([])
  const [activitiesList, setActivitiesList] = useState([])
  const [loadingDms, setLoadingDms] = useState(false)
  const [loadingActivities, setLoadingActivities] = useState(false)
  const moreButtonRef = useRef(null)
  const hoverTimeoutRef = useRef(null)
  const [showUserPopup, setShowUserPopup] = useState(false)
  const accountBtnRef = useRef(null)
  const [popupStyle, setPopupStyle] = useState({ left: '72px', right: 'auto', top: '8px', zIndex: 10001 })
  

  // Close popup when route changes
  useEffect(() => {
    setShowMorePopup(false)
  }, [location.pathname])

  // Close popup when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (moreButtonRef.current && !moreButtonRef.current.contains(event.target)) {
        setShowMorePopup(false)
      }
    }

    if (showMorePopup) {
      document.addEventListener('mousedown', handleClickOutside)
      return () => {
        document.removeEventListener('mousedown', handleClickOutside)
      }
    }
  }, [showMorePopup])

  const handleMouseEnter = (itemName, event) => {
    clearTimeout(hoverTimeoutRef.current)
    hoverTimeoutRef.current = setTimeout(() => {
      setHoveredItem(itemName)
    }, 300)
  }

  const handleMouseLeave = () => {
    clearTimeout(hoverTimeoutRef.current)
    hoverTimeoutRef.current = setTimeout(() => {
      setHoveredItem(null)
      console.log('Hover cleared')
    }, 100)
  }

  const handleHoverCardEnter = () => {
    clearTimeout(hoverTimeoutRef.current)
  }

  const handleHoverCardLeave = () => {
    setHoveredItem(null)
  }

  const handleNavClick = (path) => {
    setHoveredItem(null) // Close hover popup
    navigate(path)
  }

  const handlePopupClick = (e) => {
    e.stopPropagation() // Prevent click from bubbling to parent nav item
  }

  // Load DMs when hovering over DMs panel
  const loadDms = async () => {
    if (loadingDms) return
    setLoadingDms(true)
    try {
      const res = await api.get('/api/direct-messages/conversations')
      setDmsList(res.data || [])
    } catch (err) {
      // If unauthenticated or error, fail silently and keep placeholders
      console.debug('Failed to load DM conversations', err)
    } finally {
      setLoadingDms(false)
    }
  }

  // Load activities when hovering over Activity panel
  const loadActivities = async () => {
    if (loadingActivities) return
    setLoadingActivities(true)
    try {
      const res = await api.get('/api/activity/all')
      setActivitiesList(res.data || [])
    } catch (err) {
      console.debug('Failed to load activities', err)
    } finally {
      setLoadingActivities(false)
    }
  }

  useEffect(() => {
    if (hoveredItem === 'dms' && dmsList.length === 0) {
      loadDms()
    }
    if (hoveredItem === 'activity' && activitiesList.length === 0) {
      loadActivities()
    }
  }, [hoveredItem])

  const handleDmClick = (userId) => {
    setHoveredItem(null)
    navigate(`/dm/${userId}`)
  }

  const handleActivityClick = async (activity) => {
    setHoveredItem(null)
    if (!activity) return navigate('/activity')
    try {
      if (activity.contentType === 'dm') {
        navigate(`/dm/${activity.contentId}`)
        return
      }
      // contentId is channel id — fetch channel to get name
      const ch = await api.get(`/api/channels/${activity.contentId}`)
      const channelName = ch?.data?.name
      if (channelName) {
        navigate(`/channel/${channelName}`)
        return
      }
    } catch (err) {
      console.debug('Failed to open activity target', err)
    }
    // fallback
    navigate('/activity')
  }

  return (
    <nav className="slim-nav">
      <div className="slim-nav-items">
        <div 
          className="slim-nav-item"
          onClick={() => handleNavClick('/')}
        >
          <div className="workspace-icon-small">DD</div>
        </div>

        <Link to="/home" className={`slim-nav-item ${location.pathname === '/home' || location.pathname === '/' || location.pathname.startsWith('/channel') ? 'active' : ''}`}>
          <HomeIcon size={24} />
          <span className="slim-nav-label">Home</span>
        </Link>

        <div 
          className={`slim-nav-item ${location.pathname.startsWith('/dm') ? 'active' : ''}`}
          onClick={() => handleNavClick('/dms')}
          onMouseEnter={(e) => handleMouseEnter('dms', e)}
          onMouseLeave={handleMouseLeave}
        >
          <MessageIcon size={24} />
          <span className="slim-nav-label">DMs</span>
        </div>

        <div 
          className={`slim-nav-item ${location.pathname === '/activity' ? 'active' : ''}`}
          onClick={() => handleNavClick('/activity')}
          onMouseEnter={(e) => handleMouseEnter('activity', e)}
          onMouseLeave={handleMouseLeave}
        >
          <BellIcon size={24} />
          <span className="slim-nav-label">Activity</span>
        </div>

        <div 
          className={`slim-nav-item ${location.pathname === '/files' ? 'active' : ''}`}
          onClick={() => handleNavClick('/files')}
          onMouseEnter={(e) => handleMouseEnter('files', e)}
          onMouseLeave={handleMouseLeave}
        >
          <FilesIcon size={24} />
          <span className="slim-nav-label">Files</span>
          
        </div>

        <div 
          ref={moreButtonRef}
          className="slim-nav-item more-button"
          onClick={() => setShowMorePopup(!showMorePopup)}
          onMouseEnter={(e) => handleMouseEnter('more', e)}
          onMouseLeave={handleMouseLeave}
        >
          <MoreHorizontalIcon size={24} />
          <span className="slim-nav-label">More</span>
          
          {showMorePopup && (
            <div className="more-popup">
              <h3>More</h3>
              <div className="more-popup-item">
                <div className="more-popup-icon">
                  <Wrench size={24} />
                </div>
                <div className="more-popup-text">
                  <strong>Tools</strong>
                  <p>Create and find workflows and apps</p>
                </div>
              </div>
              <a href="#" className="more-popup-link">Customise navigation bar</a>
            </div>
          )}
        </div>
      </div>

      <div className="slim-nav-bottom">
        <button className="slim-nav-item">
          <PlusIcon size={24} />
        </button>
        <div style={{ position: 'relative' }}>
          <button ref={accountBtnRef} className="slim-nav-item" onClick={() => {
            // compute popup top so the popup's bottom aligns with the button bottom
            const btn = accountBtnRef.current
            if (btn) {
              const popupH = 305
              const topPx = btn.offsetTop + btn.offsetHeight - popupH
              setPopupStyle({ left: '72px', right: 'auto', top: `${topPx}px`, zIndex: 10001 })
            }
            setShowUserPopup(s => !s)
          }} title="Account">
            <User size={24} />
          </button>
          <UserPopup visible={showUserPopup} onClose={() => setShowUserPopup(false)} style={popupStyle} />
        </div>
      </div>
    </nav>
  )
}
