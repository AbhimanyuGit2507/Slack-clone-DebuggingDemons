import React from 'react'

export default function ArrowLeftIcon({ size = 20, className = '' }) {
  return (
    <svg 
      data-r2k="true"
      data-qa="arrow-left" 
      aria-hidden="true" 
      viewBox="0 0 20 20" 
      width={size} 
      height={size}
      className={className}
    >
      <path 
        fill="currentColor" 
        fillRule="evenodd" 
        d="M9.768 5.293a.75.75 0 0 0-1.036-1.086l-5.5 5.25a.75.75 0 0 0 0 1.085l5.5 5.25a.75.75 0 1 0 1.036-1.085L5.622 10.75H16.25a.75.75 0 0 0 0-1.5H5.622z" 
        clipRule="evenodd"
      />
    </svg>
  )
}
