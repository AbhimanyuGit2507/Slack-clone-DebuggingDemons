import React, { useState, useEffect, useRef } from 'react'
import '../styles/ResizableHandle.css'

export default function ResizableHandleRight({ minWidth, maxWidth, defaultWidth, onResize, children }) {
  const [width, setWidth] = useState(defaultWidth)
  const [isResizing, setIsResizing] = useState(false)
  const sidebarRef = useRef(null)

  useEffect(() => {
    if (!isResizing) return

    const handleMouseMove = (e) => {
      if (!sidebarRef.current) return
      const newWidth = window.innerWidth - e.clientX
      
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
    <div className="resizable-container-right" style={{ width: `${width}px` }} ref={sidebarRef}>
      <div 
        className={`resize-handle-left ${isResizing ? 'resizing' : ''}`}
        onMouseDown={handleMouseDown}
      />
      {children}
    </div>
  )
}
