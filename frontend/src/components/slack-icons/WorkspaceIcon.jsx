import React from 'react'

export default function WorkspaceIcon({ text = 'DD', size = 36, className = '' }) {
  return (
    <svg 
      data-qa="team-icon" 
      aria-hidden="false" 
      viewBox="0 0 20 20" 
      width={size} 
      height={size}
      className={className}
      style={{ minWidth: size }}
    >
      <text 
        x="50%" 
        y="50%" 
        dominantBaseline="middle" 
        textAnchor="middle" 
        fontSize="12" 
        fill="currentColor"
      >
        {text}
      </text>
    </svg>
  )
}
