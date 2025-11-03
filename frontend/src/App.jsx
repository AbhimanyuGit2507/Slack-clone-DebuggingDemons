import React, { useEffect, useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import ChannelPage from './pages/ChannelPage'
import DMPage from './pages/DMPage'
import DMsListPage from './pages/DMsListPage'
import HomePage from './pages/HomePage'
import ActivityPage from './pages/ActivityPage'
import FilesPage from './pages/FilesPage'
import LaterPage from './pages/LaterPage'
import DirectoriesPage from './pages/DirectoriesPage'
import TopNav from './components/TopNav'
import IconNav from './components/IconNav'
import Sidebar from './components/Sidebar'
import DMsListSidebar from './components/DMsListSidebar'
import ResizableHandle from './components/ResizableHandle'
import './styles/App.css'

function AppLayout() {
  return (
    <>
      <TopNav />
      <div className="main-container">
        <IconNav />
        <Routes>
          <Route path="/" element={<Navigate to="/home" replace />} />
          <Route path="/home" element={<><Sidebar /><HomePage /></>} />
          <Route path="/dms" element={<DMsListPage />} />
          <Route path="/activity" element={<ActivityPage />} />
          <Route path="/files" element={<FilesPage />} />
          <Route path="/later" element={<><Sidebar /><LaterPage /></>} />
          <Route path="/directories" element={<><Sidebar /><DirectoriesPage /></>} />
          <Route path="/channel/:name" element={<><Sidebar /><ChannelPage /></>} />
          <Route path="/dm/:id" element={
            <>
              <ResizableHandle minWidth={319.2} maxWidth={719.2} defaultWidth={352}>
                <DMsListSidebar />
              </ResizableHandle>
              <DMPage />
            </>
          } />
        </Routes>
      </div>
    </>
  )
}

export default function App(){
  const [dark, setDark] = useState(() => localStorage.getItem('dark') === '1')
  
  useEffect(()=>{
    document.body.classList.toggle('dark', dark)
    localStorage.setItem('dark', dark ? '1' : '0')
  }, [dark])

  return <AppLayout />
}
