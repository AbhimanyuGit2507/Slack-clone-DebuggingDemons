import React, { useState } from 'react'
import '../styles/CreateChannelModal.css'

export default function CreateChannelModal({ isOpen, onClose, onCreate }) {
  const [channelName, setChannelName] = useState('')
  const [selectedTemplate, setSelectedTemplate] = useState('blank')

  const templates = [
    { id: 'blank', name: 'Blank channel' },
    { id: 'project', name: 'Project starter kit' },
    { id: 'help', name: 'Help requests process' },
    { id: 'team', name: 'Team support' },
    { id: 'feedback', name: 'Feedback intake and triage' },
    { id: 'onboarding', name: 'New hire onboarding' },
    { id: 'coaching', name: '1:1 coaching' },
    { id: 'sales', name: 'Sales deal tracking' }
  ]

  const handleCreate = () => {
    if (channelName.trim()) {
      onCreate({ name: channelName, template: selectedTemplate })
      setChannelName('')
      setSelectedTemplate('blank')
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        
        <div className="modal-layout">
          <div className="modal-sidebar">
            <h2>Create a channel</h2>
            
            <div className="template-list">
              {templates.map(template => (
                <button
                  key={template.id}
                  className={`template-item ${selectedTemplate === template.id ? 'active' : ''}`}
                  onClick={() => setSelectedTemplate(template.id)}
                >
                  {template.name}
                </button>
              ))}
              <a href="#" className="show-all-link">Show all templates</a>
            </div>

            <button className="modal-next-btn" onClick={handleCreate}>Next</button>
          </div>

          <div className="modal-preview">
            <img 
              src="/channel-preview.png" 
              alt="Channel preview" 
              className="preview-image"
            />
          </div>
        </div>
      </div>
    </div>
  )
}
