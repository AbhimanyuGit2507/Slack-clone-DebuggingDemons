import React from 'react'

export default function HistoryIcon({ size = 20, className = '' }) {
  return (
    <svg 
      data-r2k="true" 
      data-qa="history" 
      aria-hidden="true" 
      viewBox="0 0 20 20" 
      width={size} 
      height={size} 
      className={className}
      style={{ display: 'inline-block', verticalAlign: 'middle' }}
    >
      <path fill="currentColor" fillRule="evenodd" d="M2.5 2.5v2.524A9 9 0 1 1 10 19a.75.75 0 0 1 0-1.5A7.5 7.5 0 1 0 3.239 6.75H6.75a.75.75 0 0 1 0 1.5h-5A.75.75 0 0 1 1 7.5v-5a.75.75 0 0 1 1.5 0m11.363 3.333a.75.75 0 1 0-1.226-.866l-3.25 4.6a.75.75 0 0 0 .083.963l3 3a.75.75 0 1 0 1.06-1.06l-2.553-2.553zM1.875 12a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5m1.875 2.5a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0m2 3.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5" clipRule="evenodd"></path>
    </svg>
  )
}
