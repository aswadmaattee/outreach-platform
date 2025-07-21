import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  Search, 
  Play, 
  RefreshCw, 
  CheckCircle, 
  AlertCircle,
  Users,
  Globe,
  Mail,
  Phone
} from 'lucide-react'

const API_BASE_URL = 'http://localhost:5000/api'

export function Scanner() {
  const [scanStatus, setScanStatus] = useState({
    total_businesses: 0,
    pending_scan: 0,
    scanned: 0,
    active: 0,
    scan_completion_rate: 0
  })
  const [scanning, setScanning] = useState(false)
  const [scanResult, setScanResult] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchScanStatus()
  }, [])

  const fetchScanStatus = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/scan/status`)
      const data = await response.json()
      setScanStatus(data)
    } catch (error) {
      console.error('Error fetching scan status:', error)
    } finally {
      setLoading(false)
    }
  }

  const startScan = async () => {
    try {
      setScanning(true)
      setScanResult(null)
      
      const response = await fetch(`${API_BASE_URL}/scan/all-pending`, {
        method: 'POST'
      })
      
      const result = await response.json()
      setScanResult(result)
      
      // Refresh status after scan
      await fetchScanStatus()
    } catch (error) {
      console.error('Error starting scan:', error)
      setScanResult({ error: 'Failed to start scan: ' + error.message })
    } finally {
      setScanning(false)
    }
  }

  const scanSingleBusiness = async (businessId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/scan/business/${businessId}`, {
        method: 'POST'
      })
      
      const result = await response.json()
      console.log('Single business scan result:', result)
      
      // Refresh status after scan
      await fetchScanStatus()
    } catch (error) {
      console.error('Error scanning business:', error)
    }
  }

  const statusCards = [
    {
      title: 'Total Businesses',
      value: scanStatus.total_businesses,
      description: 'In your database',
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Pending Scan',
      value: scanStatus.pending_scan,
      description: 'Awaiting scan',
      icon: Search,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100'
    },
    {
      title: 'Scanned',
      value: scanStatus.scanned,
      description: 'Scan completed',
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Active',
      value: scanStatus.active,
      description: 'Ready for outreach',
      icon: Globe,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    }
  ]

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">Scanner</h1>
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
          <h1 className="text-3xl font-bold text-gray-900">Online Presence Scanner</h1>
          <p className="text-gray-600">Automatically find social media profiles and contact information</p>
        </div>
        <Button onClick={fetchScanStatus} variant="outline">
          <RefreshCw className="mr-2 h-4 w-4" />
          Refresh
        </Button>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statusCards.map((stat, index) => (
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

      {/* Progress Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Scan Progress</CardTitle>
          <CardDescription>
            Overall scanning progress for your business database
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">
              Completion Rate
            </span>
            <span className="text-sm text-gray-500">
              {scanStatus.scanned + scanStatus.active} of {scanStatus.total_businesses} businesses
            </span>
          </div>
          <Progress value={scanStatus.scan_completion_rate} className="w-full" />
          <p className="text-sm text-gray-600">
            {scanStatus.scan_completion_rate}% of businesses have been scanned for online presence
          </p>
        </CardContent>
      </Card>

      {/* Scanner Controls */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Bulk Scanner</CardTitle>
            <CardDescription>
              Scan all pending businesses for social media profiles and contact information
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Search className="h-4 w-4 text-gray-500" />
                <span className="text-sm">Find social media profiles (Instagram, Facebook, Twitter, LinkedIn)</span>
              </div>
              <div className="flex items-center space-x-2">
                <Mail className="h-4 w-4 text-gray-500" />
                <span className="text-sm">Extract contact emails and forms</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="h-4 w-4 text-gray-500" />
                <span className="text-sm">Find additional phone numbers</span>
              </div>
              <div className="flex items-center space-x-2">
                <Globe className="h-4 w-4 text-gray-500" />
                <span className="text-sm">Verify website information</span>
              </div>
            </div>

            <Button 
              onClick={startScan} 
              disabled={scanning || scanStatus.pending_scan === 0}
              className="w-full"
            >
              {scanning ? (
                <>
                  <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                  Scanning...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  Scan {scanStatus.pending_scan} Pending Businesses
                </>
              )}
            </Button>

            {scanStatus.pending_scan === 0 && (
              <p className="text-sm text-gray-500 text-center">
                No businesses pending scan. All businesses have been processed.
              </p>
            )}
          </CardContent>
        </Card>

        {/* Scanner Features */}
        <Card>
          <CardHeader>
            <CardTitle>Scanner Features</CardTitle>
            <CardDescription>What the scanner looks for</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-medium text-gray-900">Social Media Detection</h4>
                <p className="text-sm text-gray-600">
                  Automatically finds Instagram, Facebook, Twitter/X, and LinkedIn profiles
                </p>
              </div>
              
              <div className="border-l-4 border-green-500 pl-4">
                <h4 className="font-medium text-gray-900">Contact Extraction</h4>
                <p className="text-sm text-gray-600">
                  Extracts email addresses, phone numbers, and contact forms from websites
                </p>
              </div>
              
              <div className="border-l-4 border-purple-500 pl-4">
                <h4 className="font-medium text-gray-900">Website Verification</h4>
                <p className="text-sm text-gray-600">
                  Verifies and updates website URLs, checks for redirects
                </p>
              </div>
              
              <div className="border-l-4 border-orange-500 pl-4">
                <h4 className="font-medium text-gray-900">Smart Rate Limiting</h4>
                <p className="text-sm text-gray-600">
                  Respects website rate limits and implements intelligent delays
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Scan Results */}
      {scanResult && (
        <Card>
          <CardHeader>
            <CardTitle>Scan Results</CardTitle>
            <CardDescription>Latest scan operation results</CardDescription>
          </CardHeader>
          <CardContent>
            {scanResult.error ? (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{scanResult.error}</AlertDescription>
              </Alert>
            ) : (
              <Alert>
                <CheckCircle className="h-4 w-4" />
                <AlertDescription>
                  <div className="space-y-2">
                    <p className="font-medium">{scanResult.message}</p>
                    <div className="text-sm">
                      <p>• Businesses scanned: {scanResult.scanned_count}</p>
                      <p>• Total pending: {scanResult.total_pending}</p>
                    </div>
                  </div>
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}

