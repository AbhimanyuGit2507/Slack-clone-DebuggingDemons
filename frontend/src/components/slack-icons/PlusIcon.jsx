import React from 'react'

export default function PlusIcon({ size = 20, className = '' }) {
  return (
    <svg 
      data-r2k="true"
      data-qa="plus-filled" 
      aria-hidden="true" 
      viewBox="0 0 20 20" 
      width={size} 
      height={size}
      className={className}
    >
      <path 
        fill="currentColor" 
        fillRule="evenodd" 
        d="M11 3.5a1 1 0 1 0-2 0V9H3.5a1 1 0 0 0 0 2H9v5.5a1 1 0 1 0 2 0V11h5.5a1 1 0 1 0 0-2H11z" 
        clipRule="evenodd"
      />
    </svg>
  )
}
