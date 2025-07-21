import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import { Dashboard } from './components/Dashboard'
import { BusinessList } from './components/BusinessList'
import { CampaignList } from './components/CampaignList'
import { Analytics } from './components/Analytics'
import { CSVUpload } from './components/CSVUpload'
import { Scanner } from './components/Scanner'
import './App.css'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">
            <div className="container mx-auto px-6 py-8">
              <Routes>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/businesses" element={<BusinessList />} />
                <Route path="/campaigns" element={<CampaignList />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/upload" element={<CSVUpload />} />
                <Route path="/scanner" element={<Scanner />} />
              </Routes>
            </div>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App

