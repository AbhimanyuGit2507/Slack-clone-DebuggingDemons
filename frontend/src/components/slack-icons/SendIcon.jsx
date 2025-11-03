import React from 'react'

export default function SendIcon({ size = 20, className = '' }) {
  return (
    <svg 
      data-qa="send-filled" 
      aria-hidden="true" 
      viewBox="0 0 20 20" 
      width={size} 
      height={size}
      className={className}
    >
      <path 
        fill="currentColor" 
        d="M1.5 2.106c0-.462.498-.754.901-.528l15.7 7.714a.73.73 0 0 1 .006 1.307L2.501 18.46l-.07.017a.754.754 0 0 1-.931-.733v-4.572c0-1.22.971-2.246 2.213-2.268l6.547-.17c.27-.01.75-.243.75-.797 0-.553-.5-.795-.75-.795l-6.547-.171C2.47 8.95 1.5 7.924 1.5 6.704z"
      />
    </svg>
  )
}
