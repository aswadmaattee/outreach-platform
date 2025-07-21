import { useState, useCallback } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Upload, FileText, CheckCircle, AlertCircle, Download } from 'lucide-react'

const API_BASE_URL = 'http://localhost:5000/api'

export function CSVUpload() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [error, setError] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.type === 'text/csv' || droppedFile.name.endsWith('.csv')) {
        setFile(droppedFile)
        setError(null)
      } else {
        setError('Please select a CSV file')
      }
    }
  }, [])

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      if (selectedFile.type === 'text/csv' || selectedFile.name.endsWith('.csv')) {
        setFile(selectedFile)
        setError(null)
      } else {
        setError('Please select a CSV file')
      }
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first')
      return
    }

    setUploading(true)
    setError(null)
    setUploadResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_BASE_URL}/businesses/upload`, {
        method: 'POST',
        body: formData,
      })

      const result = await response.json()

      if (response.ok) {
        setUploadResult(result)
        setFile(null)
        // Reset file input
        const fileInput = document.getElementById('file-upload')
        if (fileInput) fileInput.value = ''
      } else {
        setError(result.error || 'Upload failed')
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setUploading(false)
    }
  }

  const downloadSampleCSV = () => {
    const sampleData = [
      ['Business Name', 'Website', 'Email', 'Phone Number', 'Address'],
      ['Acme Corp', 'https://acme.com', 'info@acme.com', '555-0123', '123 Main St'],
      ['Tech Solutions', '', 'contact@techsol.com', '555-0456', '456 Oak Ave'],
      ['Local Bakery', 'https://localbakery.com', '', '555-0789', '789 Pine St']
    ]

    const csvContent = sampleData.map(row => row.join(',')).join('\\n')
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'sample_businesses.csv'
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">CSV Upload</h1>
        <p className="text-gray-600">Upload a CSV file containing business information</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upload Section */}
        <Card>
          <CardHeader>
            <CardTitle>Upload CSV File</CardTitle>
            <CardDescription>
              Upload a CSV file with business data. Required column: Business Name. 
              Optional columns: Website, Email, Phone Number, Address.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Drag and Drop Area */}
            <div
              className={`
                border-2 border-dashed rounded-lg p-8 text-center transition-colors
                ${dragActive 
                  ? 'border-blue-500 bg-blue-50' 
                  : 'border-gray-300 hover:border-gray-400'
                }
              `}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <div className="space-y-2">
                <p className="text-lg font-medium text-gray-900">
                  Drop your CSV file here
                </p>
                <p className="text-gray-500">or</p>
                <label htmlFor="file-upload">
                  <Button variant="outline" className="cursor-pointer">
                    Choose File
                  </Button>
                  <input
                    id="file-upload"
                    type="file"
                    accept=".csv"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                </label>
              </div>
            </div>

            {/* Selected File */}
            {file && (
              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <FileText className="h-5 w-5 text-gray-500" />
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>
            )}

            {/* Upload Button */}
            <Button 
              onClick={handleUpload} 
              disabled={!file || uploading}
              className="w-full"
            >
              {uploading ? 'Uploading...' : 'Upload CSV'}
            </Button>

            {/* Error Display */}
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Upload Result */}
            {uploadResult && (
              <Alert>
                <CheckCircle className="h-4 w-4" />
                <AlertDescription>
                  <div className="space-y-2">
                    <p className="font-medium">{uploadResult.message}</p>
                    {uploadResult.result && (
                      <div className="text-sm">
                        <p>• Total rows: {uploadResult.result.total_rows}</p>
                        <p>• Processed: {uploadResult.result.processed}</p>
                        <p>• Errors: {uploadResult.result.errors}</p>
                      </div>
                    )}
                  </div>
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Instructions and Sample */}
        <Card>
          <CardHeader>
            <CardTitle>CSV Format Instructions</CardTitle>
            <CardDescription>Follow these guidelines for best results</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div>
                <h4 className="font-medium text-gray-900">Required Column:</h4>
                <ul className="text-sm text-gray-600 ml-4">
                  <li>• <strong>Business Name</strong> - Name of the business</li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900">Optional Columns:</h4>
                <ul className="text-sm text-gray-600 ml-4">
                  <li>• <strong>Website</strong> - Business website URL</li>
                  <li>• <strong>Email</strong> - Primary contact email</li>
                  <li>• <strong>Phone Number</strong> - Contact phone number</li>
                  <li>• <strong>Address</strong> - Business address or location</li>
                </ul>
              </div>

              <div>
                <h4 className="font-medium text-gray-900">Tips:</h4>
                <ul className="text-sm text-gray-600 ml-4">
                  <li>• Use exact column names as shown above</li>
                  <li>• Empty cells are allowed for optional columns</li>
                  <li>• Duplicate business names will be skipped</li>
                  <li>• File size limit: 10MB</li>
                </ul>
              </div>
            </div>

            <Button 
              variant="outline" 
              onClick={downloadSampleCSV}
              className="w-full"
            >
              <Download className="mr-2 h-4 w-4" />
              Download Sample CSV
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

