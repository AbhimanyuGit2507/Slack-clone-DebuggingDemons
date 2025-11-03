import React from 'react'
import '../styles/HoverCard.css'

export default function HoverCard({ children, isVisible }) {
  if (!isVisible) return null

  return (
    <div className="hover-card">
      {children}
    </div>
  )
}
