import React from 'react'
import usePageTitle from '../hooks/usePageTitle'
import '../styles/LaterPage.css'

export default function LaterPage(){
  usePageTitle('Later')
  
  return (
    <div className="later-page">
      <div className="later-header">
        <h1>Later</h1>
        <p className="later-subtitle">Save things for later and get reminders</p>
      </div>
      
      <div className="later-content">
        <div className="later-empty">
          <div className="later-icon">🕐</div>
          <h2>Nothing saved for later yet</h2>
          <p>You can save messages and files to return to them when you're ready.</p>
          <button className="later-learn-more">Learn about saving items for later</button>
        </div>
      </div>

      <div className="later-section">
        <h3>Reminders</h3>
        <div className="later-empty-small">
          <p>No upcoming reminders</p>
        </div>
      </div>
    </div>
  )
}
