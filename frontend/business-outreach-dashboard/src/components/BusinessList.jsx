import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table'
import { 
  Building2, 
  Globe, 
  Mail, 
  Phone, 
  MapPin, 
  Search,
  ChevronLeft,
  ChevronRight,
  Eye,
  Edit
} from 'lucide-react'

const API_BASE_URL = 'http://localhost:5000/api'

export function BusinessList() {
  const [businesses, setBusinesses] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [selectedBusiness, setSelectedBusiness] = useState(null)

  useEffect(() => {
    fetchBusinesses()
  }, [currentPage, searchTerm, statusFilter])

  const fetchBusinesses = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams({
        page: currentPage,
        per_page: 10,
        ...(searchTerm && { search: searchTerm }),
        ...(statusFilter && { status: statusFilter })
      })

      const response = await fetch(`${API_BASE_URL}/businesses?${params}`)
      const data = await response.json()
      
      setBusinesses(data.businesses || [])
      setTotalPages(data.total_pages || 1)
    } catch (error) {
      console.error('Error fetching businesses:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'scanned': return 'bg-blue-100 text-blue-800'
      case 'pending_scan': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const formatStatus = (status) => {
    return status.replace('_', ' ').replace(/\\b\\w/g, l => l.toUpperCase())
  }

  const BusinessDetails = ({ business, onClose }) => (
    <Card className="mt-4">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Building2 className="h-5 w-5" />
            <span>{business.name}</span>
          </CardTitle>
          <Button variant="outline" size="sm" onClick={onClose}>
            Close
          </Button>
        </div>
        <CardDescription>Business details and contacts</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Business Info */}
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900">Business Information</h4>
            <div className="space-y-3">
              {business.website && (
                <div className="flex items-center space-x-2">
                  <Globe className="h-4 w-4 text-gray-500" />
                  <a 
                    href={business.website} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {business.website}
                  </a>
                </div>
              )}
              {business.email && (
                <div className="flex items-center space-x-2">
                  <Mail className="h-4 w-4 text-gray-500" />
                  <span>{business.email}</span>
                </div>
              )}
              {business.phone_number && (
                <div className="flex items-center space-x-2">
                  <Phone className="h-4 w-4 text-gray-500" />
                  <span>{business.phone_number}</span>
                </div>
              )}
              {business.address && (
                <div className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4 text-gray-500" />
                  <span>{business.address}</span>
                </div>
              )}
            </div>
          </div>

          {/* Contacts */}
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900">
              Contacts ({business.contacts?.length || 0})
            </h4>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {business.contacts?.map((contact) => (
                <div 
                  key={contact.id} 
                  className="p-3 border rounded-lg bg-gray-50"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline" className="text-xs">
                        {contact.type}
                      </Badge>
                      {contact.is_primary && (
                        <Badge variant="default" className="text-xs">
                          Primary
                        </Badge>
                      )}
                    </div>
                    <Badge variant="secondary" className="text-xs">
                      {contact.source}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-900 mt-1 break-all">
                    {contact.value}
                  </p>
                </div>
              )) || (
                <p className="text-gray-500 text-sm">No contacts found</p>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Businesses</h1>
        <p className="text-gray-600">Manage your business database</p>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search businesses..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Statuses</option>
              <option value="pending_scan">Pending Scan</option>
              <option value="scanned">Scanned</option>
              <option value="active">Active</option>
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Business Table */}
      <Card>
        <CardHeader>
          <CardTitle>Business List</CardTitle>
          <CardDescription>
            {businesses.length} businesses found
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
                </div>
              ))}
            </div>
          ) : (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Business Name</TableHead>
                    <TableHead>Website</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Contacts</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {businesses.map((business) => (
                    <TableRow key={business.id}>
                      <TableCell className="font-medium">
                        {business.name}
                      </TableCell>
                      <TableCell>
                        {business.website ? (
                          <a 
                            href={business.website} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline text-sm"
                          >
                            {business.website.length > 30 
                              ? business.website.substring(0, 30) + '...' 
                              : business.website
                            }
                          </a>
                        ) : (
                          <span className="text-gray-400">-</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {business.email || <span className="text-gray-400">-</span>}
                      </TableCell>
                      <TableCell>
                        <Badge className={getStatusColor(business.status)}>
                          {formatStatus(business.status)}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">
                          {business.contacts?.length || 0}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setSelectedBusiness(
                            selectedBusiness?.id === business.id ? null : business
                          )}
                        >
                          <Eye className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {/* Pagination */}
              <div className="flex items-center justify-between mt-4">
                <p className="text-sm text-gray-700">
                  Page {currentPage} of {totalPages}
                </p>
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                  >
                    <ChevronLeft className="h-4 w-4" />
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                  >
                    Next
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* Business Details */}
      {selectedBusiness && (
        <BusinessDetails 
          business={selectedBusiness} 
          onClose={() => setSelectedBusiness(null)} 
        />
      )}
    </div>
  )
}

