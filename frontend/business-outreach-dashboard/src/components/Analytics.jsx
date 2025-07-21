import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { 
  TrendingUp, 
  Mail, 
  Users, 
  Target,
  Download,
  Calendar
} from 'lucide-react'

const API_BASE_URL = 'http://localhost:5000/api'

export function Analytics() {
  const [analytics, setAnalytics] = useState({
    totalBusinesses: 0,
    totalCampaigns: 0,
    totalMessages: 0,
    overallSuccessRate: 0
  })
  const [campaigns, setCampaigns] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      
      // Fetch businesses
      const businessesResponse = await fetch(`${API_BASE_URL}/businesses`)
      const businessesData = await businessesResponse.json()
      
      // Fetch campaigns
      const campaignsResponse = await fetch(`${API_BASE_URL}/campaigns`)
      const campaignsData = await campaignsResponse.json()
      
      const campaignsList = campaignsData.campaigns || []
      setCampaigns(campaignsList)
      
      // Calculate analytics
      const totalMessages = campaignsList.reduce((total, campaign) => {
        return total + (campaign.messages_summary?.total || 0)
      }, 0)
      
      const totalSent = campaignsList.reduce((total, campaign) => {
        return total + (campaign.messages_summary?.sent || 0)
      }, 0)
      
      const overallSuccessRate = totalMessages > 0 ? Math.round((totalSent / totalMessages) * 100) : 0
      
      setAnalytics({
        totalBusinesses: businessesData.total_items || 0,
        totalCampaigns: campaignsList.length,
        totalMessages,
        overallSuccessRate
      })
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  // Prepare chart data
  const campaignChartData = campaigns.map(campaign => ({
    name: campaign.name.length > 15 ? campaign.name.substring(0, 15) + '...' : campaign.name,
    sent: campaign.messages_summary?.sent || 0,
    failed: campaign.messages_summary?.failed || 0,
    opened: campaign.messages_summary?.opened || 0,
    replied: campaign.messages_summary?.replied || 0
  }))

  const statusData = campaigns.reduce((acc, campaign) => {
    const summary = campaign.messages_summary || {}
    acc.sent += summary.sent || 0
    acc.failed += summary.failed || 0
    acc.opened += summary.opened || 0
    acc.replied += summary.replied || 0
    return acc
  }, { sent: 0, failed: 0, opened: 0, replied: 0 })

  const pieData = [
    { name: 'Sent', value: statusData.sent, color: '#10B981' },
    { name: 'Failed', value: statusData.failed, color: '#EF4444' },
    { name: 'Opened', value: statusData.opened, color: '#3B82F6' },
    { name: 'Replied', value: statusData.replied, color: '#8B5CF6' }
  ].filter(item => item.value > 0)

  const statCards = [
    {
      title: 'Total Businesses',
      value: analytics.totalBusinesses,
      description: 'In your database',
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Active Campaigns',
      value: analytics.totalCampaigns,
      description: 'Running campaigns',
      icon: Mail,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Messages Sent',
      value: analytics.totalMessages,
      description: 'Total outreach messages',
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    {
      title: 'Success Rate',
      value: `${analytics.overallSuccessRate}%`,
      description: 'Overall delivery rate',
      icon: Target,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    }
  ]

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
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
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600">Track your outreach performance</p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline">
            <Calendar className="mr-2 h-4 w-4" />
            Last 30 Days
          </Button>
          <Button variant="outline">
            <Download className="mr-2 h-4 w-4" />
            Export
          </Button>
        </div>
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

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Campaign Performance Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Campaign Performance</CardTitle>
            <CardDescription>Messages sent, opened, and replied by campaign</CardDescription>
          </CardHeader>
          <CardContent>
            {campaignChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={campaignChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="sent" fill="#10B981" name="Sent" />
                  <Bar dataKey="opened" fill="#3B82F6" name="Opened" />
                  <Bar dataKey="replied" fill="#8B5CF6" name="Replied" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-64 text-gray-500">
                No campaign data available
              </div>
            )}
          </CardContent>
        </Card>

        {/* Message Status Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Message Status Distribution</CardTitle>
            <CardDescription>Breakdown of message statuses</CardDescription>
          </CardHeader>
          <CardContent>
            {pieData.length > 0 ? (
              <div className="flex items-center justify-center">
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}`}
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="flex items-center justify-center h-64 text-gray-500">
                No message data available
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Campaign Details Table */}
      <Card>
        <CardHeader>
          <CardTitle>Campaign Details</CardTitle>
          <CardDescription>Detailed performance metrics for each campaign</CardDescription>
        </CardHeader>
        <CardContent>
          {campaigns.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Campaign</th>
                    <th className="text-left p-2">Status</th>
                    <th className="text-left p-2">Total</th>
                    <th className="text-left p-2">Sent</th>
                    <th className="text-left p-2">Opened</th>
                    <th className="text-left p-2">Replied</th>
                    <th className="text-left p-2">Success Rate</th>
                  </tr>
                </thead>
                <tbody>
                  {campaigns.map((campaign) => {
                    const summary = campaign.messages_summary || {}
                    const successRate = summary.total > 0 
                      ? Math.round((summary.sent / summary.total) * 100) 
                      : 0

                    return (
                      <tr key={campaign.id} className="border-b hover:bg-gray-50">
                        <td className="p-2 font-medium">{campaign.name}</td>
                        <td className="p-2">
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            campaign.status === 'completed' ? 'bg-green-100 text-green-800' :
                            campaign.status === 'sending' ? 'bg-blue-100 text-blue-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {campaign.status}
                          </span>
                        </td>
                        <td className="p-2">{summary.total || 0}</td>
                        <td className="p-2">{summary.sent || 0}</td>
                        <td className="p-2">{summary.opened || 0}</td>
                        <td className="p-2">{summary.replied || 0}</td>
                        <td className="p-2">{successRate}%</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              No campaigns found. Create a campaign to see analytics.
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

