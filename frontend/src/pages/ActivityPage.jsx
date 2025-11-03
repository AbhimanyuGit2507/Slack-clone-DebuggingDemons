import React, { useState, useEffect } from 'react'
import ResizableHandle from '../components/ResizableHandle'
import { PartyPopper, Mail } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import DMPage from './DMPage'
import ChannelPage from './ChannelPage'
import api from '../api/axios'
import usePageTitle from '../hooks/usePageTitle'
import '../styles/ActivityPage.css'

export default function ActivityPage() {
  usePageTitle('Activity')
  const [showUnreadOnly, setShowUnreadOnly] = useState(false)
  const [selectedActivity, setSelectedActivity] = useState(null)
  const [viewType, setViewType] = useState(null)
  const [activities, setActivities] = useState([])
  const [loading, setLoading] = useState(true)

  const defaultWidth = 352
  const minWidth = 319.2
  const maxWidth = 719.2

  useEffect(() => {
    // Fetch activities from API
    setLoading(true)
    api.get('/api/activity/all')
      .then(res => {
        console.log('Activities API response:', res.data)
        setActivities(res.data || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching activities:', err)
        setActivities([])
        setLoading(false)
      })
  }, [])

  const handleActivityClick = (activity) => {
    setSelectedActivity(activity)
    setViewType(activity.contentType)
  }

  return (
    <div className="activity-page">
      {/* Child Sidebar */}
      <ResizableHandle minWidth={minWidth} maxWidth={maxWidth} defaultWidth={defaultWidth}>
        <div className="activity-sidebar">
        <div className="activity-sidebar-header">
          <h2>Activity</h2>
          <div className="header-actions">
            <label className="unread-toggle">
              <span>Unread messages</span>
              <input 
                type="checkbox" 
                checked={showUnreadOnly}
                onChange={(e) => setShowUnreadOnly(e.target.checked)}
              />
              <span className="toggle-switch"></span>
            </label>
          </div>
        </div>

        <div className="activity-filters">
          <button className="filter-all">All</button>
        </div>

        <div className="activity-section">
          <div className="activity-list">
            {loading ? (
              <div style={{ padding: '20px', textAlign: 'center', color: '#616061' }}>
                Loading activities...
              </div>
            ) : activities.length === 0 ? (
              <div style={{ padding: '20px', textAlign: 'center', color: '#616061' }}>
                No activities yet
              </div>
            ) : (
              activities.map(activity => {
                // Get icon based on activity type
                const getActivityIcon = (type) => {
                  switch(type) {
                    case 'mention': return '💬'
                    case 'invitation': return '📧'
                    case 'reaction': return '👍'
                    case 'reply': return '↩️'
                    case 'channel_created': return '🆕'
                    case 'file_shared': return '📎'
                    default: return '📌'
                  }
                }

                // Format time ago
                const getTimeAgo = (timestamp) => {
                  if (!timestamp) return ''
                  const now = new Date()
                  const then = new Date(timestamp)
                  const diffMs = now - then
                  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
                  const diffDays = Math.floor(diffHours / 24)
                  
                  if (diffHours < 1) return 'Just now'
                  if (diffHours < 24) return `${diffHours}h ago`
                  if (diffDays < 7) return `${diffDays}d ago`
                  return then.toLocaleDateString()
                }

                return (
                  <div 
                    key={activity.id} 
                    className={`activity-item ${selectedActivity?.id === activity.id ? 'active' : ''}`}
                    onClick={() => handleActivityClick(activity)}
                    style={{ cursor: 'pointer' }}
                  >
                    <div className="activity-avatar">
                      <span style={{ fontSize: '20px' }}>
                        {getActivityIcon(activity.activity_type)}
                      </span>
                    </div>
                    <div className="activity-content">
                      <div className="activity-text">
                        {activity.action || activity.description || 'Activity'}
                      </div>
                      {activity.is_read === false && <div className="unread-dot"></div>}
                    </div>
                    <div className="activity-time">
                      {getTimeAgo(activity.timestamp)}
                    </div>
                  </div>
                )
              })
            )}
          </div>
        </div>
      </div>
      </ResizableHandle>

      {/* Main Content - Dynamic Component Rendering */}
      <div className="activity-main-content">
        {selectedActivity && (
          <div className="activity-type-header">
            <span className="activity-type-badge">
              {selectedActivity.user_name || selectedActivity.user || 'Unknown'} {selectedActivity.action || selectedActivity.activity_type || 'activity'}
            </span>
          </div>
        )}
        <AnimatePresence mode="wait">
          {!selectedActivity ? (
            <motion.div
              key="welcome"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="activity-welcome"
            >
              <img 
                src="/src/assets/empty-activity-dark-3771651.svg" 
                alt="No activity selected"
                className="empty-state-svg"
              />
            </motion.div>
          ) : (
            <motion.div
              key={`${viewType}-${selectedActivity.contentId}`}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.2 }}
              style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}
            >
              {viewType === 'dm' ? (
                <DMPage userId={selectedActivity.contentId} />
              ) : viewType === 'channel' ? (
                <ChannelPage channelId={selectedActivity.contentId} />
              ) : null}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
