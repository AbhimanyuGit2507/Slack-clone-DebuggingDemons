import React, { useState, useEffect, useRef } from 'react'
import '../styles/ResizableHandle.css'

export default function ResizableHandle({ minWidth, maxWidth, defaultWidth, onResize, children }) {
  const [width, setWidth] = useState(defaultWidth)
  const [isResizing, setIsResizing] = useState(false)
  const sidebarRef = useRef(null)

  useEffect(() => {
    if (!isResizing) return

    const handleMouseMove = (e) => {
      if (!sidebarRef.current) return
      const newWidth = e.clientX - 72 // 72px is the IconNav width
      
      if (newWidth >= minWidth && newWidth <= maxWidth) {
        setWidth(newWidth)
        if (onResize) onResize(newWidth)
      }
    }

    const handleMouseUp = () => {
      setIsResizing(false)
      document.body.style.cursor = 'default'
      document.body.style.userSelect = 'auto'
    }

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)

    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
  }, [isResizing, minWidth, maxWidth, onResize])

  const handleMouseDown = () => {
    setIsResizing(true)
    document.body.style.cursor = 'col-resize'
    document.body.style.userSelect = 'none'
  }

  return (
    <div className="resizable-container" style={{ width: `${width}px` }} ref={sidebarRef}>
      {children}
      <div 
        className={`resize-handle ${isResizing ? 'resizing' : ''}`}
        onMouseDown={handleMouseDown}
      />
    </div>
  )
}
