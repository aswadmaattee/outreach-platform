import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Building2, Mail, BarChart3, Users, TrendingUp, Clock } from 'lucide-react'
import { Link } from 'react-router-dom'

const API_BASE_URL = 'http://localhost:5000/api'

export function Dashboard() {
  const [stats, setStats] = useState({
    totalBusinesses: 0,
    totalCampaigns: 0,
    totalMessages: 0,
    scanStatus: { pending_scan: 0, scanned: 0, scan_completion_rate: 0 }
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardStats()
  }, [])

  const fetchDashboardStats = async () => {
    try {
      setLoading(true)
      
      // Fetch businesses
      const businessesResponse = await fetch(`${API_BASE_URL}/businesses`)
      const businessesData = await businessesResponse.json()
      
      // Fetch campaigns
      const campaignsResponse = await fetch(`${API_BASE_URL}/campaigns`)
      const campaignsData = await campaignsResponse.json()
      
      // Fetch scan status
      const scanResponse = await fetch(`${API_BASE_URL}/scan/status`)
      const scanData = await scanResponse.json()
      
      // Calculate total messages from campaigns
      const totalMessages = campaignsData.campaigns?.reduce((total, campaign) => {
        return total + (campaign.messages_summary?.total || 0)
      }, 0) || 0
      
      setStats({
        totalBusinesses: businessesData.total_items || 0,
        totalCampaigns: campaignsData.total_items || 0,
        totalMessages,
        scanStatus: scanData
      })
    } catch (error) {
      console.error('Error fetching dashboard stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: 'Total Businesses',
      value: stats.totalBusinesses,
      description: 'Businesses in database',
      icon: Building2,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Active Campaigns',
      value: stats.totalCampaigns,
      description: 'Outreach campaigns',
      icon: Mail,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Messages Sent',
      value: stats.totalMessages,
      description: 'Total messages sent',
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    {
      title: 'Scan Progress',
      value: `${stats.scanStatus.scan_completion_rate}%`,
      description: `${stats.scanStatus.scanned} of ${stats.scanStatus.scanned + stats.scanStatus.pending_scan} scanned`,
      icon: BarChart3,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    }
  ]

  const quickActions = [
    {
      title: 'Upload CSV',
      description: 'Add new businesses from CSV file',
      href: '/upload',
      icon: Building2,
      color: 'bg-blue-600 hover:bg-blue-700'
    },
    {
      title: 'Create Campaign',
      description: 'Start a new outreach campaign',
      href: '/campaigns',
      icon: Mail,
      color: 'bg-green-600 hover:bg-green-700'
    },
    {
      title: 'Run Scanner',
      description: 'Scan for social media profiles',
      href: '/scanner',
      icon: BarChart3,
      color: 'bg-purple-600 hover:bg-purple-700'
    }
  ]

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-full"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome to your business outreach platform</p>
        </div>
        <Button onClick={fetchDashboardStats} variant="outline">
          <Clock className="mr-2 h-4 w-4" />
          Refresh
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                  <p className="text-sm text-gray-500">{stat.description}</p>
                </div>
                <div className={`p-3 rounded-full ${stat.bgColor}`}>
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Get started with common tasks</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {quickActions.map((action, index) => (
                <Link key={index} to={action.href}>
                  <Button 
                    className={`w-full h-auto p-4 flex flex-col items-center space-y-2 ${action.color} text-white`}
                  >
                    <action.icon className="h-8 w-8" />
                    <div className="text-center">
                      <div className="font-semibold">{action.title}</div>
                      <div className="text-xs opacity-90">{action.description}</div>
                    </div>
                  </Button>
                </Link>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Latest platform updates</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <div className="text-sm">
                  <p className="font-medium">System Online</p>
                  <p className="text-gray-500">All services running</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div className="text-sm">
                  <p className="font-medium">Database Connected</p>
                  <p className="text-gray-500">Ready for operations</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <div className="text-sm">
                  <p className="font-medium">Scanner Ready</p>
                  <p className="text-gray-500">Ready to find contacts</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

