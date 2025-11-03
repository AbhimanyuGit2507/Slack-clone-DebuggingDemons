import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Folder, FileText, List, SlidersHorizontal, Heart, Smile, PartyPopper } from 'lucide-react'
import { PlusIcon, StarIcon, SearchIcon, MoreVerticalIcon } from '../components/slack-icons'
import { motion } from 'framer-motion'
import ResizableHandle from '../components/ResizableHandle'
import api from '../api/axios'
import usePageTitle from '../hooks/usePageTitle'
import '../styles/FilesPage.css'

export default function FilesPage() {
  usePageTitle('Files')
  const navigate = useNavigate()
  const [activeSection, setActiveSection] = useState('All files')
  const [activeFilter, setActiveFilter] = useState('All')
  const [files, setFiles] = useState([])
  const [canvases, setCanvases] = useState([])
  const [starredFileIds, setStarredFileIds] = useState(() => {
    // Load starred file/canvas IDs from localStorage
    const saved = localStorage.getItem('starredFiles')
    return saved ? JSON.parse(saved) : []
  })
  const [recentlyViewed, setRecentlyViewed] = useState(() => {
    // Load recently viewed from localStorage (array of {id, timestamp})
    const saved = localStorage.getItem('recentlyViewed')
    return saved ? JSON.parse(saved) : []
  })

  const defaultWidth = 352
  const minWidth = 319.2
  const maxWidth = 719.2

  useEffect(() => {
    // Fetch files/attachments from API
    api.get('/api/attachments/')
      .then(res => {
        console.log('Files API response:', res.data)
        const fetchedFiles = res.data || []
        setFiles(fetchedFiles)
      })
      .catch(err => {
        console.error('Error fetching files:', err)
        setFiles([])
      })
    
    // Fetch canvases from API
    api.get('/api/canvas/')
      .then(res => {
        console.log('Canvas API response:', res.data)
        // Filter out empty canvases - only show those with real content (not just placeholder text)
        const nonEmptyCanvases = (res.data || []).filter(canvas => {
          try {
            const content = JSON.parse(canvas.content)
            // Check if there's at least one line with real text (not placeholder, not empty)
            return Array.isArray(content) && content.some(line => 
              line.text && 
              line.text.trim() !== '' && 
              !line.isPlaceholder
            )
          } catch (e) {
            console.error('Error parsing canvas content:', e)
            return false
          }
        })
        console.log('Filtered canvases with content:', nonEmptyCanvases)
        setCanvases(nonEmptyCanvases)
      })
      .catch(err => {
        console.error('Error fetching canvases:', err)
        setCanvases([])
      })
  }, [])

  const displayedFiles = activeSection === 'Canvases' ? canvases : activeSection === 'All files' ? [...files, ...canvases] : files

  // Handler to open canvas
  const handleCanvasClick = (canvas) => {
    if (canvas.channel_id) {
      // Track as recently viewed
      const newRecentlyViewed = [
        { id: canvas.id, timestamp: Date.now() },
        ...recentlyViewed.filter(item => item.id !== canvas.id)
      ].slice(0, 10) // Keep only last 10
      setRecentlyViewed(newRecentlyViewed)
      localStorage.setItem('recentlyViewed', JSON.stringify(newRecentlyViewed))
      
      // Save canvas ID to localStorage to auto-open it
      localStorage.setItem('openCanvasInChannel', canvas.id)
      // Navigate to the channel
      navigate(`/channel/${canvas.channel_id}`)
    }
  }

  // Handler to toggle star on files/canvases
  const handleStarFile = (e, fileId) => {
    e.stopPropagation() // Prevent file/canvas from opening
    setStarredFileIds(prev => {
      const newStarred = prev.includes(fileId) 
        ? prev.filter(id => id !== fileId)
        : [...prev, fileId]
      localStorage.setItem('starredFiles', JSON.stringify(newStarred))
      return newStarred
    })
  }

  return (
    <div className="files-page">
      {/* Left Sidebar */}
      <ResizableHandle minWidth={minWidth} maxWidth={maxWidth} defaultWidth={defaultWidth}>
        <div className="files-sidebar">
          <div className="files-sidebar-header">
            <h2>Files</h2>
            <button className="icon-btn-files">
              <PlusIcon size={16} />
            </button>
          </div>

          <div className="files-nav">
            <div 
              className={`files-nav-item ${activeSection === 'All files' ? 'active' : ''}`}
              onClick={() => setActiveSection('All files')}
            >
              <Folder size={18} />
              <span>All files</span>
            </div>
            <div 
              className={`files-nav-item ${activeSection === 'Canvases' ? 'active' : ''}`}
              onClick={() => setActiveSection('Canvases')}
            >
              <FileText size={18} />
              <span>Canvases</span>
            </div>
            <div 
              className={`files-nav-item ${activeSection === 'Lists' ? 'active' : ''}`}
              onClick={() => setActiveSection('Lists')}
            >
              <List size={18} />
              <span>Lists</span>
            </div>
          </div>

          <div className="starred-section">
            <h3>Recently viewed</h3>
            {recentlyViewed.length === 0 ? (
              <p className="starred-text">
                Your recently viewed canvases will appear here.
              </p>
            ) : (
              <div className="starred-items">
                {recentlyViewed
                  .map(item => [...files, ...canvases].find(f => f.id === item.id))
                  .filter(Boolean)
                  .map(file => {
                    const isCanvas = file.content && file.channel_id !== undefined
                    return (
                      <div 
                        key={file.id} 
                        className="starred-item"
                        onClick={() => isCanvas && handleCanvasClick(file)}
                        style={{ cursor: isCanvas ? 'pointer' : 'default' }}
                      >
                        <FileText size={16} />
                        <span>{file.title || file.file_name || file.name || 'Untitled'}</span>
                      </div>
                    )
                  })}
              </div>
            )}
          </div>

          <div className="starred-section">
            <h3>Starred</h3>
            {starredFileIds.length === 0 ? (
              <p className="starred-text">
                Click the <StarIcon size={14} className="inline-icon" /> star on any canvas or file to add it here for later.
              </p>
            ) : (
              <div className="starred-items">
                {[...files, ...canvases]
                  .filter(file => starredFileIds.includes(file.id))
                  .map(file => {
                    const isCanvas = file.content && file.channel_id !== undefined
                    return (
                      <div 
                        key={file.id} 
                        className="starred-item"
                        onClick={() => isCanvas && handleCanvasClick(file)}
                        style={{ cursor: isCanvas ? 'pointer' : 'default' }}
                      >
                        <FileText size={16} />
                        <span>{file.title || file.file_name || file.name || 'Untitled'}</span>
                      </div>
                    )
                  })}
              </div>
            )}
          </div>
        </div>
      </ResizableHandle>

      {/* Main Content */}
      <motion.div 
        className="files-main-content"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="files-content-header">
          <h1>{activeSection}</h1>
          <button className="btn-new-file">
            <PlusIcon size={16} />
            New
          </button>
        </div>

        <div className="files-filter-bar">
          <div className="filter-tabs">
            <button 
              className={`filter-tab ${activeFilter === 'All' ? 'active' : ''}`}
              onClick={() => setActiveFilter('All')}
            >
              All
            </button>
            <button 
              className={`filter-tab ${activeFilter === 'Created by you' ? 'active' : ''}`}
              onClick={() => setActiveFilter('Created by you')}
            >
              Created by you
            </button>
            <button 
              className={`filter-tab ${activeFilter === 'Shared with you' ? 'active' : ''}`}
              onClick={() => setActiveFilter('Shared with you')}
            >
              Shared with you
            </button>
          </div>
          <div className="filter-actions">
            <button className="filter-dropdown">
              <SlidersHorizontal size={14} />
              5 Types
              <span className="dropdown-arrow">▼</span>
            </button>
            <button className="filter-dropdown">
              Recently viewed
              <span className="dropdown-arrow">▼</span>
            </button>
            <button className="filter-icon-btn">
              <SlidersHorizontal size={16} />
            </button>
          </div>
        </div>

        <div className="files-list">
          {displayedFiles.length === 0 ? (
            <div style={{ padding: '40px 20px', textAlign: 'center', color: '#616061' }}>
              <FileText size={48} style={{ margin: '0 auto 16px', opacity: 0.3 }} />
              <p>No files found</p>
              <p style={{ fontSize: '14px', marginTop: '8px' }}>
                Files shared in channels and DMs will appear here
              </p>
            </div>
          ) : (
            displayedFiles.map((file, index) => {
              const isCanvas = file.content && file.channel_id !== undefined
              const isStarred = starredFileIds.includes(file.id)
              
              return (
                <motion.div 
                  key={file.id} 
                  className="file-list-item"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2, delay: index * 0.03 }}
                  onClick={() => isCanvas && handleCanvasClick(file)}
                  style={{ cursor: isCanvas ? 'pointer' : 'default' }}
                >
                  <div className="file-icon-container">
                    <div className="file-icon-circle">
                      <FileText size={20} />
                    </div>
                  </div>
                  <div className="file-info">
                    <div className="file-title-row">
                      <span className="file-title">{file.title || file.file_name || file.name || 'Untitled'}</span>
                      {file.is_template && <span className="template-badge">Template</span>}
                    </div>
                    <div className="file-meta-row">
                      <span className="file-owner">{file.owner?.username || file.uploader_name || file.owner || 'Unknown'}</span>
                      <span className="file-separator"> · </span>
                      <span className="file-date">
                        {file.created_at || file.uploaded_at ? 
                          new Date(file.created_at || file.uploaded_at).toLocaleDateString() : 
                          'Unknown date'}
                      </span>
                      {file.file_size && (
                        <>
                          <span className="file-separator"> · </span>
                          <span className="file-read-time">{(file.file_size / 1024).toFixed(1)} KB</span>
                        </>
                      )}
                    </div>
                  </div>
                  <div className="file-actions-row">
                    <button 
                      className={`file-action-btn ${isStarred ? 'starred' : ''}`}
                      onClick={(e) => handleStarFile(e, file.id)}
                    >
                      <StarIcon size={16} fill={isStarred ? '#e8912d' : 'none'} />
                    </button>
                    <button className="file-action-btn">
                      <MoreVerticalIcon size={16} />
                    </button>
                  </div>
                </motion.div>
              )
            })
          )}
        </div>
      </motion.div>
    </div>
  )
}
