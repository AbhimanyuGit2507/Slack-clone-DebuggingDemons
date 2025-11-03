import React from 'react'

export default function ChevronRightIcon({ size = 20, className = '' }) {
  return (
    <svg 
      data-r2k="true" 
      data-qa="caret-right" 
      aria-hidden="true" 
      viewBox="0 0 20 20" 
      width={size} 
      height={size} 
      className={className}
      style={{ display: 'inline-block', verticalAlign: 'middle' }}
    >
      <path fill="currentColor" fillRule="evenodd" d="M7.72 5.72a.75.75 0 0 1 1.06 0l3.75 3.75a.75.75 0 0 1 0 1.06l-3.75 3.75a.75.75 0 0 1-1.06-1.06L10.94 10 7.72 6.78a.75.75 0 0 1 0-1.06" clipRule="evenodd"></path>
    </svg>
  )
}
