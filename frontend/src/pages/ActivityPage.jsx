import React, { useState, useEffect } from 'react'
import ResizableHandle from '../components/ResizableHandle'
import { PartyPopper, Mail } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import DMPage from './DMPage'
import ChannelPage from './ChannelPage'
import api from '../api/axios'
import emptyActivitySvg from '../assets/empty-activity-dark-3771651.svg'
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
        const data = res.data || []
        if (!data || data.length === 0) {
          // try public endpoint as fallback
          return api.get('/api/activity/public')
        }
        return { data }
      })
      .then(res2 => {
        const data = res2?.data || []
        setActivities(data)
        setLoading(false)
      })
      .catch(err => {
        console.warn('Error fetching activities, trying public endpoint:', err)
        // attempt public endpoint
        api.get('/api/activity/public').then(pub => {
          setActivities(pub.data || [])
          setLoading(false)
        }).catch(e => {
          console.error('Public activities fetch failed too:', e)
          setActivities([])
          setLoading(false)
        })
      })
  }, [])

  // New useEffect to fetch DM conversations
  useEffect(() => {
    // Fetch conversations for DMs
    setLoading(true);
    api.get('/api/direct-messages/conversations')
      .then((res) => {
        const conversations = res.data.map((conv) => ({
          id: conv.user_id,
          contentType: 'dm',
          contentId: conv.user_id,
          description: conv.last_message?.content || 'No messages yet',
          user_id: conv.user_id,
          action: `DM with ${conv.username}`,
          timestamp: conv.last_message?.timestamp || new Date().toISOString(),
        }));

        setActivities((prev) => [...prev, ...conversations]);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching DM conversations:', err);
        setLoading(false);
      });
  }, []);

  // New useEffect to fetch user data for activities
  useEffect(() => {
    // Fetch user data for activities
    const fetchUserAvatars = async () => {
      const updatedActivities = await Promise.all(
        activities.map(async (activity) => {
          if (!activity.avatarUrl) {
            try {
              const res = await api.get(`/api/users/${activity.user_id}`);
              return {
                ...activity,
                avatarUrl: res.data.profile_picture || res.data.avatar || null,
              };
            } catch (err) {
              console.error(`Error fetching user data for user_id ${activity.user_id}:`, err);
              return activity; // Return the activity as is if the fetch fails
            }
          }
          return activity; // Skip if avatarUrl already exists
        })
      );
      setActivities(updatedActivities);
    };

    if (activities.length > 0) {
      fetchUserAvatars();
    }
  }, [activities]);

  const handleActivityClick = (activity) => {
    setSelectedActivity(activity)
    setViewType(activity.contentType)
  }

  useEffect(() => {
    if (selectedActivity) {
      console.log('Selected Activity:', selectedActivity)
      console.log('View Type:', viewType)
    }
  }, [selectedActivity, viewType])

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
                activities
                  .filter(activity => activity.contentType) // Filter out activities with undefined contentType
                  .map((activity, index) => (
                    <div 
                      key={`${activity.id}-${activity.contentType}-${index}`} 
                      className={`activity-item ${selectedActivity?.id === activity.id ? 'active' : ''}`}
                      onClick={() => handleActivityClick(activity)}
                      style={{ cursor: 'pointer' }}
                    >
                      <div className="dm-avatar-img" style={{ width: '36px', height: '36px', borderRadius: '50%', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <img 
                          src={activity.avatarUrl || `https://i.pravatar.cc/150?img=${activity.user_id}`} 
                          alt="Avatar" 
                          style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
                        />
                      </div>
                      <div className="activity-content">
                        <div className="activity-text">
                          {activity.action || activity.description || 'Activity'}
                        </div>
                        {activity.is_read === false && <div className="unread-dot"></div>}
                      </div>
                      <div className="activity-time">
                        {new Date(activity.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  ))
              )}
            </div>
          </div>
        </div>
      </ResizableHandle>

      {/* Main Content - Dynamic Component Rendering */}
      <div className="activity-main-content">
        <AnimatePresence mode="wait">
          {selectedActivity ? (
            viewType === 'dm' ? (
              <DMPage userId={selectedActivity.contentId} />
            ) : viewType === 'channel' ? (
              <ChannelPage channelId={selectedActivity.contentId} />
            ) : null
          ) : (
            <motion.div
              key="welcome"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="activity-welcome"
            >
              <img
                src={emptyActivitySvg}
                alt="No activity selected"
                className="empty-state-svg"
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
