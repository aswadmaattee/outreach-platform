# API Documentation - Business Outreach Platform

This document provides comprehensive documentation for all API endpoints in the Business Outreach Platform.

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API does not require authentication. For production use, implement JWT or API key authentication.

---

## 📊 Business Management

### GET /businesses
Get all businesses with pagination and filtering.

**Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)
- `status` (optional): Filter by status (pending_scan, scanned, active)
- `search` (optional): Search by business name

**Response:**
```json
{
  "businesses": [
    {
      "id": 1,
      "name": "Acme Corp",
      "website": "https://acme.com",
      "email": "info@acme.com",
      "phone": "+1-555-0123",
      "address": "123 Main St, City, State",
      "status": "scanned",
      "created_at": "2025-07-21T10:30:00Z",
      "contacts": [
        {
          "id": 1,
          "type": "email",
          "value": "info@acme.com",
          "platform": "email"
        }
      ]
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3
  }
}
```

### GET /businesses/{id}
Get a specific business by ID.

**Response:**
```json
{
  "id": 1,
  "name": "Acme Corp",
  "website": "https://acme.com",
  "email": "info@acme.com",
  "phone": "+1-555-0123",
  "address": "123 Main St, City, State",
  "status": "scanned",
  "created_at": "2025-07-21T10:30:00Z",
  "contacts": [
    {
      "id": 1,
      "type": "email",
      "value": "info@acme.com",
      "platform": "email"
    }
  ]
}
```

### POST /businesses
Create a new business.

**Request Body:**
```json
{
  "name": "New Business",
  "website": "https://newbusiness.com",
  "email": "contact@newbusiness.com",
  "phone": "+1-555-0456",
  "address": "456 Oak Ave, City, State"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "New Business",
  "website": "https://newbusiness.com",
  "email": "contact@newbusiness.com",
  "phone": "+1-555-0456",
  "address": "456 Oak Ave, City, State",
  "status": "pending_scan",
  "created_at": "2025-07-21T11:00:00Z",
  "contacts": []
}
```

### PUT /businesses/{id}
Update an existing business.

**Request Body:**
```json
{
  "name": "Updated Business Name",
  "website": "https://updated-website.com",
  "email": "new-email@business.com",
  "phone": "+1-555-0789",
  "address": "789 Pine St, City, State"
}
```

### DELETE /businesses/{id}
Delete a business and all associated contacts.

**Response:**
```json
{
  "message": "Business deleted successfully"
}
```

### POST /businesses/upload-csv
Upload a CSV file with business data.

**Request:**
- Content-Type: multipart/form-data
- Field name: `file`
- File format: CSV with headers

**CSV Format:**
```csv
Business Name,Website,Email,Phone Number,Address
Acme Corp,https://acme.com,info@acme.com,+1-555-0123,123 Main St
Tech Solutions,,contact@techsol.com,+1-555-0456,456 Oak Ave
```

**Response:**
```json
{
  "message": "CSV processed successfully",
  "businesses_created": 2,
  "businesses_skipped": 0,
  "errors": []
}
```

---

## 🔍 Contact Management

### POST /businesses/{id}/contacts
Add a new contact to a business.

**Request Body:**
```json
{
  "type": "email",
  "value": "sales@business.com",
  "platform": "email"
}
```

**Response:**
```json
{
  "id": 3,
  "business_id": 1,
  "type": "email",
  "value": "sales@business.com",
  "platform": "email",
  "created_at": "2025-07-21T11:30:00Z"
}
```

### DELETE /contacts/{id}
Delete a specific contact.

**Response:**
```json
{
  "message": "Contact deleted successfully"
}
```

---

## 🔎 Scanner Operations

### GET /scan/status
Get current scanning status and statistics.

**Response:**
```json
{
  "total_businesses": 25,
  "pending_scan": 5,
  "scanned": 18,
  "active": 2,
  "scan_progress": {
    "completion_rate": 72.0,
    "businesses_scanned": 18,
    "total_businesses": 25
  },
  "last_scan": "2025-07-21T10:45:00Z"
}
```

### POST /scan/business/{id}
Scan a specific business for online presence.

**Response:**
```json
{
  "message": "Scan completed for business",
  "business_id": 1,
  "contacts_found": 3,
  "social_media_found": ["instagram", "facebook"],
  "scan_duration": 2.5
}
```

### POST /scan/all-pending
Scan all businesses with pending_scan status.

**Response:**
```json
{
  "message": "Bulk scan initiated",
  "businesses_to_scan": 5,
  "estimated_duration": "2-3 minutes"
}
```

---

## 📧 Campaign Management

### GET /campaigns
Get all campaigns.

**Response:**
```json
{
  "campaigns": [
    {
      "id": 1,
      "name": "Summer Outreach 2025",
      "message_template": "Hi {business_name}, we have a special offer...",
      "status": "completed",
      "created_at": "2025-07-21T09:00:00Z",
      "message_count": 15,
      "sent_count": 12,
      "success_rate": 80.0
    }
  ]
}
```

### GET /campaigns/{id}
Get a specific campaign with detailed message information.

**Response:**
```json
{
  "id": 1,
  "name": "Summer Outreach 2025",
  "message_template": "Hi {business_name}, we have a special offer...",
  "status": "completed",
  "created_at": "2025-07-21T09:00:00Z",
  "messages": [
    {
      "id": 1,
      "business_id": 1,
      "contact_id": 1,
      "platform": "email",
      "status": "sent",
      "sent_at": "2025-07-21T09:15:00Z",
      "personalized_message": "Hi Acme Corp, we have a special offer..."
    }
  ]
}
```

### POST /campaigns
Create a new campaign.

**Request Body:**
```json
{
  "name": "New Campaign",
  "message_template": "Hello {business_name}! We found your business at {website} and would love to connect.",
  "target_platforms": ["email", "instagram", "facebook"]
}
```

**Response:**
```json
{
  "id": 2,
  "name": "New Campaign",
  "message_template": "Hello {business_name}! We found your business at {website} and would love to connect.",
  "status": "draft",
  "created_at": "2025-07-21T12:00:00Z",
  "target_platforms": ["email", "instagram", "facebook"]
}
```

### POST /campaigns/{id}/preview
Preview personalized messages for a campaign.

**Response:**
```json
{
  "previews": [
    {
      "business_name": "Acme Corp",
      "platform": "email",
      "contact": "info@acme.com",
      "personalized_message": "Hello Acme Corp! We found your business at https://acme.com and would love to connect."
    }
  ],
  "total_messages": 15
}
```

### POST /campaigns/{id}/send
Send campaign messages to all eligible contacts.

**Request Body (optional):**
```json
{
  "platforms": ["email", "instagram"],
  "test_mode": false
}
```

**Response:**
```json
{
  "message": "Campaign sent successfully",
  "messages_sent": 12,
  "messages_failed": 3,
  "success_rate": 80.0,
  "details": [
    {
      "platform": "email",
      "sent": 8,
      "failed": 1
    },
    {
      "platform": "instagram",
      "sent": 4,
      "failed": 2
    }
  ]
}
```

### PUT /campaigns/{id}/pause
Pause an active campaign.

**Response:**
```json
{
  "message": "Campaign paused successfully",
  "status": "paused"
}
```

### PUT /campaigns/{id}/resume
Resume a paused campaign.

**Response:**
```json
{
  "message": "Campaign resumed successfully",
  "status": "active"
}
```

### DELETE /campaigns/{id}
Delete a campaign and all associated messages.

**Response:**
```json
{
  "message": "Campaign deleted successfully"
}
```

---

## 📊 Analytics

### GET /analytics/summary
Get analytics summary for a specified date range.

**Parameters:**
- `date_range` (optional): Number of days (default: 30)

**Response:**
```json
{
  "summary": {
    "total_businesses": 25,
    "total_campaigns": 3,
    "total_messages": 45,
    "sent_messages": 38,
    "failed_messages": 7,
    "opened_messages": 15,
    "replied_messages": 8,
    "success_rate": 84.4,
    "open_rate": 39.5,
    "reply_rate": 21.1
  },
  "campaign_performance": [
    {
      "name": "Summer Outreach 2025",
      "total": 15,
      "sent": 12,
      "opened": 6,
      "replied": 3,
      "success_rate": 80.0
    }
  ],
  "daily_performance": [
    {
      "date": "2025-07-20",
      "messages": 12
    },
    {
      "date": "2025-07-21",
      "messages": 8
    }
  ],
  "date_range": {
    "start": "2025-06-21T12:00:00Z",
    "end": "2025-07-21T12:00:00Z",
    "days": 30
  }
}
```

### GET /analytics/business-stats
Get business-related statistics.

**Response:**
```json
{
  "business_status": {
    "total": 25,
    "pending_scan": 5,
    "scanned": 18,
    "active": 2
  },
  "contact_distribution": [
    {
      "type": "email",
      "count": 20
    },
    {
      "type": "phone",
      "count": 15
    },
    {
      "type": "instagram",
      "count": 8
    },
    {
      "type": "facebook",
      "count": 6
    }
  ],
  "contact_coverage": {
    "with_contacts": 22,
    "without_contacts": 3,
    "coverage_rate": 88.0
  }
}
```

### GET /analytics/export
Export analytics data as CSV.

**Parameters:**
- `format` (optional): Export format (default: csv)
- `date_range` (optional): Number of days (default: 30)

**Response:**
- Content-Type: text/csv
- File download with campaign performance data

---

## 🔧 Task Management

### GET /tasks/status
Get status of background tasks.

**Response:**
```json
{
  "active_tasks": 2,
  "completed_tasks": 15,
  "failed_tasks": 1,
  "tasks": [
    {
      "id": "scan-business-123",
      "type": "business_scan",
      "status": "running",
      "progress": 75,
      "started_at": "2025-07-21T12:00:00Z"
    }
  ]
}
```

---

## 📝 Error Responses

All endpoints return consistent error responses:

### 400 Bad Request
```json
{
  "error": "Invalid request data",
  "details": {
    "field": "business_name",
    "message": "Business name is required"
  }
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "Business with ID 999 not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

---

## 🔄 Rate Limiting

The API implements rate limiting to prevent abuse:

- **General endpoints**: 100 requests per minute
- **Upload endpoints**: 10 requests per minute
- **Scan endpoints**: 5 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642781400
```

---

## 📋 Data Models

### Business Model
```json
{
  "id": "integer",
  "name": "string (required)",
  "website": "string (optional)",
  "email": "string (optional)",
  "phone": "string (optional)",
  "address": "string (optional)",
  "status": "enum (pending_scan, scanned, active)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Contact Model
```json
{
  "id": "integer",
  "business_id": "integer (foreign key)",
  "type": "enum (email, phone, instagram, facebook, twitter, linkedin)",
  "value": "string (contact value)",
  "platform": "string (platform name)",
  "created_at": "datetime"
}
```

### Campaign Model
```json
{
  "id": "integer",
  "name": "string (required)",
  "message_template": "text (required)",
  "status": "enum (draft, active, paused, completed)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Message Model
```json
{
  "id": "integer",
  "campaign_id": "integer (foreign key)",
  "business_id": "integer (foreign key)",
  "contact_id": "integer (foreign key)",
  "platform": "string",
  "status": "enum (pending, sent, failed, opened, replied)",
  "personalized_message": "text",
  "sent_at": "datetime",
  "opened_at": "datetime (optional)",
  "replied_at": "datetime (optional)"
}
```

---

## 🧪 Testing the API

### Using cURL

**Get all businesses:**
```bash
curl -X GET "http://localhost:5000/api/businesses"
```

**Create a new business:**
```bash
curl -X POST "http://localhost:5000/api/businesses" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Business", "website": "https://test.com"}'
```

**Upload CSV:**
```bash
curl -X POST "http://localhost:5000/api/businesses/upload-csv" \
  -F "file=@businesses.csv"
```

### Using JavaScript (Frontend)

```javascript
// Get businesses
const response = await fetch('/api/businesses');
const data = await response.json();

// Create campaign
const campaign = await fetch('/api/campaigns', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'New Campaign',
    message_template: 'Hello {business_name}!'
  })
});
```

---

## 🔐 Security Considerations

1. **Input Validation**: All inputs are validated and sanitized
2. **File Upload Security**: CSV files are validated for format and size
3. **SQL Injection Prevention**: Using SQLAlchemy ORM with parameterized queries
4. **CORS Configuration**: Properly configured for frontend access
5. **Error Handling**: No sensitive information leaked in error messages

For production deployment, consider adding:
- JWT authentication
- API key management
- Request logging
- Input rate limiting per user
- HTTPS enforcement

---

**API Documentation Version 1.0 - Last Updated: July 21, 2025**

