import React from 'react'
import { Link } from 'react-router-dom'
import '../styles/MorePage.css'

export default function MorePage(){
  return (
    <div className="more-page">
      <div className="more-header">
        <h1>More</h1>
      </div>
      
      <div className="more-sections">
        <div className="more-section">
          <h3>Collaboration</h3>
          <Link to="/channels" className="more-item">
            <span className="more-item-icon">💬</span>
            <div className="more-item-content">
              <h4>Channels</h4>
              <p>Browse all channels in your workspace</p>
            </div>
          </Link>
          <Link to="/dms" className="more-item">
            <span className="more-item-icon">✉️</span>
            <div className="more-item-content">
              <h4>Direct messages</h4>
              <p>View all your DMs</p>
            </div>
          </Link>
          <div className="more-item">
            <span className="more-item-icon">🔔</span>
            <div className="more-item-content">
              <h4>Mentions & reactions</h4>
              <p>Catch up on mentions and reactions</p>
            </div>
          </div>
        </div>

        <div className="more-section">
          <h3>Tools</h3>
          <div className="more-item">
            <span className="more-item-icon">📊</span>
            <div className="more-item-content">
              <h4>Analytics</h4>
              <p>See workspace insights</p>
            </div>
          </div>
          <div className="more-item">
            <span className="more-item-icon">🔍</span>
            <div className="more-item-content">
              <h4>Search</h4>
              <p>Search messages and files</p>
            </div>
          </div>
          <div className="more-item">
            <span className="more-item-icon">⚙️</span>
            <div className="more-item-content">
              <h4>Preferences</h4>
              <p>Manage your settings</p>
            </div>
          </div>
        </div>

        <div className="more-section">
          <h3>Apps</h3>
          <div className="more-item">
            <span className="more-item-icon">🧩</span>
            <div className="more-item-content">
              <h4>Browse apps</h4>
              <p>Discover apps for your workspace</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
