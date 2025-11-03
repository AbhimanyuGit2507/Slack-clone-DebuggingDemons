import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { GripVertical, Type, Smile, Paperclip, CheckSquare, Table, Code, Save } from 'lucide-react'
import { PlusIcon } from './slack-icons'
import api from '../api/axios'
import '../styles/Canvas.css'

export default function Canvas({ channelId = null, canvasId = null }) {
  const [title, setTitle] = useState('Your canvas title')
  const [lines, setLines] = useState([
    { id: 1, text: 'Once upon a time...', isPlaceholder: true }
  ])
  const [draggedItem, setDraggedItem] = useState(null)
  const [editingLine, setEditingLine] = useState(null)
  const [hasContent, setHasContent] = useState(false)
  const [savedCanvasId, setSavedCanvasId] = useState(canvasId)
  const [saving, setSaving] = useState(false)
  const [lastSaved, setLastSaved] = useState(null)

  // Load existing canvas for this channel - runs on mount and when IDs change
  useEffect(() => {
    console.log('Canvas: useEffect triggered', { channelId, canvasId })
    
    if (!channelId && !canvasId) {
      console.log('Canvas: No channelId or canvasId provided')
      return
    }
    
    if (canvasId) {
      // Load specific canvas by ID
      console.log('Canvas: Loading by canvas ID', canvasId)
      api.get(`/api/canvas/${canvasId}`)
        .then(res => {
          console.log('Canvas: Loaded canvas data', res.data)
          setSavedCanvasId(res.data.id)
          setTitle(res.data.title || 'Your canvas title')
          try {
            const content = JSON.parse(res.data.content)
            console.log('Canvas: Parsed content', content)
            if (Array.isArray(content) && content.length > 0) {
              setLines(content)
              setHasContent(content.some(line => line.text && !line.isPlaceholder))
            }
          } catch (e) {
            console.error('Error parsing canvas content:', e)
          }
        })
        .catch(err => console.error('Error loading canvas:', err))
    } else if (channelId) {
      // Load canvas by channel_id
      console.log('Canvas: Loading by channel ID', channelId)
      api.get(`/api/canvas/?channel_id=${channelId}`)
        .then(res => {
          console.log('Canvas: Loaded canvases for channel', res.data)
          if (res.data && res.data.length > 0) {
            const canvas = res.data[0] // Get first canvas for this channel
            console.log('Canvas: Using canvas', canvas)
            setSavedCanvasId(canvas.id)
            setTitle(canvas.title || 'Your canvas title')
            try {
              const content = JSON.parse(canvas.content)
              console.log('Canvas: Parsed content', content)
              if (Array.isArray(content) && content.length > 0) {
                setLines(content)
                setHasContent(content.some(line => line.text && !line.isPlaceholder))
              } else {
                console.log('Canvas: Content is empty or not an array')
              }
            } catch (e) {
              console.error('Error parsing canvas content:', e)
            }
          } else {
            console.log('Canvas: No existing canvas found for this channel')
          }
        })
        .catch(err => console.error('Error loading canvas for channel:', err))
    }
  }, [channelId, canvasId])

  // Auto-save after 2 seconds of inactivity
  useEffect(() => {
    const hasNonEmptyContent = lines.some(line => line.text && !line.isPlaceholder)
    if (!hasNonEmptyContent) {
      console.log('Canvas: Skipping auto-save - no content')
      return
    }

    console.log('Canvas: Setting up auto-save timer')
    const timer = setTimeout(() => {
      console.log('Canvas: Auto-save triggered')
      saveCanvas()
    }, 2000)

    return () => {
      console.log('Canvas: Clearing auto-save timer')
      clearTimeout(timer)
    }
  }, [title, lines, savedCanvasId, channelId])

  const saveCanvas = async () => {
    const content = JSON.stringify(lines)
    const hasNonEmptyContent = lines.some(line => line.text && !line.isPlaceholder)
    
    if (!hasNonEmptyContent) {
      console.log('Canvas: Skipping save - no content')
      return // Don't save empty canvases
    }

    console.log('Canvas: Saving...', { 
      savedCanvasId, 
      channelId, 
      title, 
      linesCount: lines.length,
      lines: lines,
      contentLength: content.length 
    })
    
    setSaving(true)
    try {
      if (savedCanvasId) {
        // Update existing canvas
        console.log('Canvas: Updating existing canvas', savedCanvasId, 'with content:', content)
        const response = await api.put(`/api/canvas/${savedCanvasId}`, {
          title,
          content,
          channel_id: channelId,
          is_public: false
        })
        console.log('Canvas: Updated successfully', response.data)
      } else {
        // Create new canvas
        console.log('Canvas: Creating new canvas with content:', content)
        const res = await api.post('/api/canvas/', {
          title,
          content,
          channel_id: channelId,
          is_public: false
        })
        console.log('Canvas: Created successfully', res.data)
        setSavedCanvasId(res.data.id)
      }
      setLastSaved(new Date())
    } catch (error) {
      console.error('Error saving canvas:', error)
      alert('Failed to save canvas: ' + (error.response?.data?.detail || error.message))
    } finally {
      setSaving(false)
    }
  }

  const handleAddLine = (index) => {
    const newLine = { id: Date.now(), text: '' }
    const newLines = [...lines]
    newLines.splice(index + 1, 0, newLine)
    setLines(newLines)
    setEditingLine(newLine.id)
  }

  const handleLineChange = (id, newText) => {
    setLines(lines.map(line => 
      line.id === id ? { ...line, text: newText, isPlaceholder: false } : line
    ))
    
    // Check if any line has content to show toolbar
    const hasAnyContent = lines.some(line => line.text !== '' || newText !== '')
    setHasContent(hasAnyContent)
  }

  const handleLineFocus = (id) => {
    // Remove placeholder text when focused
    setLines(lines.map(line => 
      line.id === id && line.isPlaceholder ? { ...line, text: '', isPlaceholder: false } : line
    ))
  }

  const handleDragStart = (e, index) => {
    setDraggedItem(index)
    e.dataTransfer.effectAllowed = 'move'
  }

  const handleDragOver = (e, index) => {
    e.preventDefault()
    if (draggedItem === null || draggedItem === index) return

    const newLines = [...lines]
    const draggedLine = newLines[draggedItem]
    newLines.splice(draggedItem, 1)
    newLines.splice(index, 0, draggedLine)
    
    setLines(newLines)
    setDraggedItem(index)
  }

  const handleDragEnd = () => {
    setDraggedItem(null)
  }

  const handleKeyDown = (e, id, index) => {
    // Only allow Enter on last line
    if (e.key === 'Enter' && index === lines.length - 1) {
      e.preventDefault()
      handleAddLine(index)
    } else if (e.key === 'Backspace' && lines[index].text === '' && lines.length > 1) {
      e.preventDefault()
      const newLines = lines.filter(line => line.id !== id)
      setLines(newLines)
      if (index > 0) {
        setEditingLine(lines[index - 1].id)
      }
      
      // Update hasContent
      const hasAnyContent = newLines.some(line => line.text !== '')
      setHasContent(hasAnyContent)
    }
  }

  // Toolbar actions
  const handleAddElement = (type) => {
    const lastIndex = lines.length - 1
    const newLine = { 
      id: Date.now(), 
      text: '',
      type: type // 'text', 'todo', 'table', 'code'
    }
    const newLines = [...lines]
    newLines.splice(lastIndex, 0, newLine)
    setLines(newLines)
    setEditingLine(newLine.id)
  }

  const handleAddEmoji = () => {
    // Simple emoji insertion - can be enhanced with emoji picker
    const emojis = ['😊', '👍', '❤️', '🎉', '✅', '🔥', '💡', '📝']
    const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)]
    const lastLineIndex = lines.length - 1
    const lastLine = lines[lastLineIndex]
    handleLineChange(lastLine.id, lastLine.text + randomEmoji)
  }

  const handleTextFormat = (format) => {
    // Text formatting - bold, italic, etc.
    console.log('Text format:', format)
    // Can be enhanced with rich text editor
  }

  return (
    <div className="canvas-page">
      <div className="canvas-container">
        <div className="canvas-header">
          <input
            type="text"
            className="canvas-title-input"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Your canvas title"
          />
          <div className="canvas-save-status">
            {saving && <span className="saving-indicator">Saving...</span>}
            {!saving && lastSaved && (
              <span className="saved-indicator">
                <Save size={14} /> Saved {new Date(lastSaved).toLocaleTimeString()}
              </span>
            )}
          </div>
        </div>

        <div className="canvas-content">
          {lines.map((line, index) => {
            const isLastLine = index === lines.length - 1
            return (
              <div
                key={line.id}
                className={`canvas-line ${draggedItem === index ? 'dragging' : ''} ${!isLastLine ? 'movable-line' : 'fixed-line'}`}
                draggable={!isLastLine}
                onDragStart={(e) => !isLastLine && handleDragStart(e, index)}
                onDragOver={(e) => !isLastLine && handleDragOver(e, index)}
                onDragEnd={handleDragEnd}
              >
                {!isLastLine && (
                  <div className="canvas-line-grip">
                    <GripVertical size={16} />
                  </div>
                )}
                <div className="canvas-line-bullet">⁝</div>
                <input
                  type="text"
                  className="canvas-line-input"
                  value={line.text}
                  onChange={(e) => handleLineChange(line.id, e.target.value)}
                  onFocus={() => handleLineFocus(line.id)}
                  onKeyDown={(e) => handleKeyDown(e, line.id, index)}
                  placeholder={isLastLine ? "Type / to insert..." : ""}
                  autoFocus={editingLine === line.id}
                />
              </div>
            )
          })}
        </div>

        {/* Show templates only when no content */}
        <AnimatePresence mode="wait">
          {!hasContent && (
            <motion.div 
              className="canvas-footer"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="canvas-templates">
                <span className="templates-label">Explore templates</span>
                <div className="template-buttons">
                  <motion.button 
                    className="template-btn"
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2, delay: 0.1 }}
                  >
                    Channel overview
                  </motion.button>
                  <motion.button 
                    className="template-btn"
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2, delay: 0.15 }}
                  >
                    Weekly sync
                  </motion.button>
                  <motion.button 
                    className="template-btn"
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2, delay: 0.2 }}
                  >
                    Shared resources
                  </motion.button>
                  <motion.button 
                    className="template-link"
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2, delay: 0.25 }}
                  >
                    Explore more...
                  </motion.button>
                </div>
              </div>
            </motion.div>
          )}

          {/* Show toolbar when content exists */}
          {hasContent && (
            <motion.div 
              className="canvas-toolbar"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <motion.button 
                className="canvas-toolbar-btn" 
                title="Add new line"
                onClick={() => handleAddElement('text')}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2, delay: 0.05 }}
              >
                <PlusIcon size={18} />
              </motion.button>
              <motion.button 
                className="canvas-toolbar-btn" 
                title="Text formatting"
                onClick={() => handleTextFormat('bold')}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2, delay: 0.1 }}
              >
                <Type size={18} />
              </motion.button>
              <motion.button 
                className="canvas-toolbar-btn" 
                title="Add emoji"
                onClick={handleAddEmoji}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2, delay: 0.15 }}
              >
                <Smile size={18} />
              </motion.button>
              <motion.button 
                className="canvas-toolbar-btn" 
                title="Attach file (coming soon)"
                onClick={() => alert('File attachment coming soon!')}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2, delay: 0.2 }}
              >
                <Paperclip size={18} />
              </motion.button>
              <motion.button 
                className="canvas-toolbar-btn" 
                title="Add to-do list"
                onClick={() => handleAddElement('todo')}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2, delay: 0.25 }}
              >
                <CheckSquare size={18} />
              </motion.button>
              <motion.button 
                className="canvas-toolbar-btn" 
                title="Add table"
                onClick={() => handleAddElement('table')}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2, delay: 0.3 }}
              >
                <Table size={18} />
              </motion.button>
              <motion.button 
                className="canvas-toolbar-btn" 
                title="Add code block"
                onClick={() => handleAddElement('code')}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2, delay: 0.35 }}
              >
                <Code size={18} />
              </motion.button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
