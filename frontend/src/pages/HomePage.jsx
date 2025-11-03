import React from 'react'
import { useNavigate } from 'react-router-dom'
import usePageTitle from '../hooks/usePageTitle'
import '../styles/HomePage.css'

export default function HomePage() {
  usePageTitle('Home')
  const navigate = useNavigate()

  // Redirect to the first channel on mount
  React.useEffect(() => {
    navigate('/channel/2')
  }, [navigate])

  return null
}
