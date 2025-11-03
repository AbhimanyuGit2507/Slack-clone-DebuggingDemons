import React from 'react'

export default function MoreHorizontalIcon({ size = 20, className = '' }) {
  return (
    <svg 
      data-r2k="true" 
      data-qa="ellipsis-horizontal-filled" 
      aria-hidden="true" 
      viewBox="0 0 20 20" 
      width={size} 
      height={size} 
      className={className}
      style={{ display: 'inline-block', verticalAlign: 'middle' }}
    >
      <path fill="currentColor" d="M14.5 10a1.75 1.75 0 1 1 3.5 0 1.75 1.75 0 0 1-3.5 0m-6.25 0a1.75 1.75 0 1 1 3.5 0 1.75 1.75 0 0 1-3.5 0M2 10a1.75 1.75 0 1 1 3.5 0A1.75 1.75 0 0 1 2 10"></path>
    </svg>
  )
}
