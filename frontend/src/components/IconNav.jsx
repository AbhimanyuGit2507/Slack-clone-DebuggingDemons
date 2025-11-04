import React, { useState, useEffect, useRef } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Wrench, User, UserPlus } from 'lucide-react'
import { HomeIcon, PlusIcon, BellIcon, DirectMessagesIcon, ChevronDownIcon, MoreHorizontalIcon, ChevronRightIcon, MessageIcon, FilesIcon } from './slack-icons'
import '../styles/IconNav.css'
import UserPopup from './UserPopup'

export default function IconNav() {
  const location = useLocation()
  const navigate = useNavigate()
  const [showMorePopup, setShowMorePopup] = useState(false)
  const [hoveredItem, setHoveredItem] = useState(null)
  const [unreadMessagesOnly, setUnreadMessagesOnly] = useState(false)
  const [unreadActivityOnly, setUnreadActivityOnly] = useState(false)
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

  return (
    <nav className="slim-nav">
      <div className="slim-nav-items">
        <div 
          className="slim-nav-item"
          onClick={() => handleNavClick('/')}
          onMouseEnter={(e) => handleMouseEnter('workspace', e)}
          onMouseLeave={handleMouseLeave}
        >
          <div className="workspace-icon-small">DD</div>
          
          {hoveredItem === 'workspace' && (
            <div className="more-popup" onClick={handlePopupClick}>
              <div className="workspace-hover-card">
                <div className="workspace-hover-header">Workspaces</div>
                <div className="workspace-hover-item workspace-hover-item-active">
                  <div className="workspace-hover-icon">W</div>
                  <div className="workspace-hover-details">
                    <div className="workspace-hover-name">Workspace</div>
                    <div className="workspace-hover-members">3 members</div>
                  </div>
                </div>
                <div className="workspace-hover-add">
                  <div className="workspace-hover-add-icon">
                    <PlusIcon size={20} />
                  </div>
                  <div className="workspace-hover-add-text">Add a workspace</div>
                </div>
              </div>
            </div>
          )}
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
          
          {hoveredItem === 'dms' && (
            <div className="more-popup" onClick={handlePopupClick}>
              <div className="dm-hover-card">
                <div className="dm-hover-header">
                  <div className="dm-hover-title">Direct messages</div>
                  <div className="dm-hover-toggle">
                    <span className="dm-hover-toggle-label">Unread messages</span>
                    <label className="toggle-switch">
                      <input 
                        type="checkbox" 
                        checked={unreadMessagesOnly}
                        onChange={() => setUnreadMessagesOnly(!unreadMessagesOnly)}
                      />
                      <span className="toggle-switch-slider"></span>
                    </label>
                  </div>
                </div>
                <div className="dm-hover-notice-box">
                  <UserPlus size={20} className="dm-hover-notice-icon" />
                  <div className="dm-hover-notice-text">
                    <strong>Anyone missing?</strong> Add your whole team and get the conversation started.
                  </div>
                </div>
                <button className="dm-hover-button">Add colleagues</button>
                <div className="dm-hover-list">
                  <div className="dm-hover-item">
                    <div className="dm-hover-avatar" style={{background: '#1264a3'}}>
                      W
                      <div className="dm-hover-status"></div>
                    </div>
                    <div className="dm-hover-info">
                      <div className="dm-hover-name">Abhimanyu Negi <span>(you)</span></div>
                      <div className="dm-hover-preview">You: hello</div>
                    </div>
                    <div className="dm-hover-time">15:37</div>
                  </div>
                  <div className="dm-hover-item">
                    <div className="dm-hover-avatar">
                      <img src="https://via.placeholder.com/36" alt="Harsh Paliwal" />
                      <div className="dm-hover-status"></div>
                    </div>
                    <div className="dm-hover-info">
                      <div className="dm-hover-name">Harsh Paliwal</div>
                      <div className="dm-hover-preview"></div>
                    </div>
                  </div>
                </div>
                <div className="dm-hover-footer">
                  <div className="dm-hover-footer-item">
                    <img src="https://via.placeholder.com/28" alt="Slackbot" className="dm-hover-footer-avatar" />
                    <span className="dm-hover-footer-name">Slackbot</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div 
          className={`slim-nav-item ${location.pathname === '/activity' ? 'active' : ''}`}
          onClick={() => handleNavClick('/activity')}
          onMouseEnter={(e) => handleMouseEnter('activity', e)}
          onMouseLeave={handleMouseLeave}
        >
          <BellIcon size={24} />
          <span className="slim-nav-label">Activity</span>
          
          {hoveredItem === 'activity' && (
            <div className="more-popup" onClick={handlePopupClick}>
              <div className="activity-hover-card">
                <div className="activity-hover-header">
                  <div className="activity-hover-title">Activity</div>
                  <div className="activity-hover-toggle">
                    <span className="activity-hover-toggle-label">Unread messages</span>
                    <label className="toggle-switch">
                      <input 
                        type="checkbox" 
                        checked={unreadActivityOnly}
                        onChange={() => setUnreadActivityOnly(!unreadActivityOnly)}
                      />
                      <span className="toggle-switch-slider"></span>
                    </label>
                  </div>
                </div>
                <div className="activity-hover-item">
                  <div className="activity-hover-item-header">
                    <ChevronRightIcon size={14} className="activity-hover-chevron" />
                    <span className="activity-hover-type">Workspace invitation</span>
                    <span className="activity-hover-date">Yesterday</span>
                  </div>
                  <div className="activity-hover-item-content">
                    <img src="https://via.placeholder.com/36" alt="Harsh Paliwal" className="activity-hover-avatar-img" />
                    <div className="activity-hover-text">
                      <div className="activity-hover-name">Harsh Paliwal</div>
                      <div className="activity-hover-message">Accepted your invitation to join Slack – take a second to say hello.</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div 
          className={`slim-nav-item ${location.pathname === '/files' ? 'active' : ''}`}
          onClick={() => handleNavClick('/files')}
          onMouseEnter={(e) => handleMouseEnter('files', e)}
          onMouseLeave={handleMouseLeave}
        >
          <FilesIcon size={24} />
          <span className="slim-nav-label">Files</span>
          
          {hoveredItem === 'files' && (
            <div className="more-popup" onClick={handlePopupClick}>
              <div className="files-hover-card">
                <div className="files-hover-header">Files</div>
                <div className="files-hover-buttons">
                  <button className="files-hover-button">
                    <PlusIcon size={14} />
                    <span>New canvas</span>
                  </button>
                  <button className="files-hover-button">
                    <PlusIcon size={14} />
                    <span>New list</span>
                  </button>
                </div>
                <div className="files-hover-list">
                  <div className="files-hover-item">
                    <div className="files-hover-icon"><FilesIcon size={20} /></div>
                    <div className="files-hover-details">
                      <div className="files-hover-name">Untitled</div>
                      <div className="files-hover-meta">Updated 1 hour ago</div>
                    </div>
                  </div>
                  <div className="files-hover-item">
                    <div className="files-hover-icon"><FilesIcon size={20} /></div>
                    <div className="files-hover-details">
                      <div className="files-hover-name">Weekly 1:1 <span className="files-hover-badge">Template</span></div>
                      <div className="files-hover-meta">Updated 2 months ago</div>
                    </div>
                  </div>
                  <div className="files-hover-item">
                    <div className="files-hover-icon"><FilesIcon size={20} /></div>
                    <div className="files-hover-details">
                      <div className="files-hover-name">Channel overview <span className="files-hover-badge">Template</span></div>
                      <div className="files-hover-meta">Updated 9 months ago</div>
                    </div>
                  </div>
                  <div className="files-hover-item">
                    <div className="files-hover-icon"><FilesIcon size={20} /></div>
                    <div className="files-hover-details">
                      <div className="files-hover-name">Untitled</div>
                      <div className="files-hover-meta">Updated 20 hours ago</div>
                    </div>
                  </div>
                  <div className="files-hover-item">
                    <div className="files-hover-icon"><FilesIcon size={20} /></div>
                    <div className="files-hover-details">
                      <div className="files-hover-name">Untitled</div>
                      <div className="files-hover-meta">Updated 20 hours ago</div>
                    </div>
                  </div>
                  <div className="files-hover-item">
                    <div className="files-hover-icon"><FilesIcon size={20} /></div>
                    <div className="files-hover-details">
                      <div className="files-hover-name">Untitled</div>
                      <div className="files-hover-meta">Updated 23 hours ago</div>
                    </div>
                  </div>
                  <div className="files-hover-item">
                    <div className="files-hover-icon"><FilesIcon size={20} /></div>
                    <div className="files-hover-details">
                      <div className="files-hover-name">To-do list <span className="files-hover-badge">Template</span></div>
                      <div className="files-hover-meta">Updated 2 months ago</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
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
