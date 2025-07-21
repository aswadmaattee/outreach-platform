# Business Outreach Platform - API Specification

This document provides detailed API specifications for the Business Outreach Platform.

## 1. Authentication

All API endpoints will require token-based authentication. A user will first log in to receive an access token, which must be included in the `Authorization` header of all subsequent requests.

## 2. Data Models

### Business

Represents a business entity.

| Field          | Type     | Description                                     | Constraints       |
| :------------- | :------- | :---------------------------------------------- | :---------------- |
| `id`           | `integer`| Unique identifier for the business              | Primary Key, Auto-increment |
| `name`         | `string` | Name of the business                            | Required, Unique  |
| `website`      | `string` | Official website URL                            | Optional, URL format |
| `email`        | `string` | Primary contact email                           | Optional, Email format |
| `phone_number` | `string` | Primary contact phone number                    | Optional          |
| `address`      | `string` | Physical address or location                    | Optional          |
| `status`       | `string` | Current status of the business in the system    | Enum: `pending_scan`, `scanned`, `active`, `archived` |
| `created_at`   | `datetime`| Timestamp of creation                           | Auto-generated    |
| `updated_at`   | `datetime`| Timestamp of last update                        | Auto-generated    |

### Contact

Represents a contact method for a business.

| Field          | Type     | Description                                     | Constraints       |
| :------------- | :------- | :---------------------------------------------- | :---------------- |
| `id`           | `integer`| Unique identifier for the contact               | Primary Key, Auto-increment |
| `business_id`  | `integer`| Foreign key to the `Business` table             | Required, Foreign Key |
| `type`         | `string` | Type of contact (e.g., email, Instagram, phone) | Enum: `email`, `instagram`, `facebook`, `twitter`, `linkedin`, `phone`, `contact_form` |
| `value`        | `string` | The contact detail itself (e.g., email address, URL) | Required          |
| `source`       | `string` | How the contact was obtained                    | Enum: `csv`, `scanned_website`, `scanned_social_media` |
| `is_primary`   | `boolean`| Indicates if this is the primary contact for its type | Default: `false`  |
| `created_at`   | `datetime`| Timestamp of creation                           | Auto-generated    |
| `updated_at`   | `datetime`| Timestamp of last update                        | Auto-generated    |

### Campaign

Represents an outreach campaign.

| Field            | Type     | Description                                     | Constraints       |
| :--------------- | :------- | :---------------------------------------------- | :---------------- |
| `id`             | `integer`| Unique identifier for the campaign              | Primary Key, Auto-increment |
| `name`           | `string` | Name of the campaign                            | Required, Unique  |
| `message_template`| `text`   | Template for the outreach message               | Required          |
| `status`         | `string` | Current status of the campaign                  | Enum: `draft`, `scheduled`, `sending`, `paused`, `completed`, `cancelled` |
| `created_at`     | `datetime`| Timestamp of creation                           | Auto-generated    |
| `updated_at`     | `datetime`| Timestamp of last update                        | Auto-generated    |

### Message

Represents an individual message sent as part of a campaign.

| Field              | Type     | Description                                     | Constraints       |
| :----------------- | :------- | :---------------------------------------------- | :---------------- |
| `id`               | `integer`| Unique identifier for the message               | Primary Key, Auto-increment |
| `campaign_id`      | `integer`| Foreign key to the `Campaign` table             | Required, Foreign Key |
| `business_id`      | `integer`| Foreign key to the `Business` table             | Required, Foreign Key |
| `contact_id`       | `integer`| Foreign key to the `Contact` table              | Required, Foreign Key |
| `platform`         | `string` | Platform used for sending (e.g., email, Instagram) | Enum: `email`, `instagram`, `facebook`, `twitter`, `linkedin` |
| `personalized_content`| `text`   | The actual content sent after personalization   | Required          |
| `status`           | `string` | Delivery status of the message                  | Enum: `pending`, `sent`, `failed`, `opened`, `replied` |
| `sent_at`          | `datetime`| Timestamp when the message was sent             | Optional          |
| `opened_at`        | `datetime`| Timestamp when the message was opened           | Optional          |
| `replied_at`       | `datetime`| Timestamp when a reply was detected             | Optional          |

## 3. API Endpoints

### 3.1. Business Endpoints

#### `POST /api/businesses/upload`

Uploads a CSV file containing business data.

*   **Request:** `multipart/form-data`
    *   `file`: CSV file
*   **Response:** `202 Accepted` if processing started, `400 Bad Request` on error.
    ```json
    {
        

    "message": "CSV processing initiated.",
        "task_id": "<celery_task_id>"
    }
    ```

#### `GET /api/businesses`

Retrieves a list of businesses.

*   **Query Parameters:**
    *   `page`: Page number (default: 1)
    *   `per_page`: Items per page (default: 20)
    *   `status`: Filter by business status (e.g., `scanned`)
    *   `search`: Search by business name or address
*   **Response:** `200 OK`
    ```json
    {
        "businesses": [
            { "id": 1, "name": "Business A", "website": "http://businessa.com", ... },
            // ...
        ],
        "total_pages": 5,
        "current_page": 1,
        "total_items": 98
    }
    ```

#### `GET /api/businesses/{id}`

Retrieves details for a single business.

*   **Path Parameters:**
    *   `id`: Business ID
*   **Response:** `200 OK` or `404 Not Found`
    ```json
    {
        "id": 1,
        "name": "Business A",
        "website": "http://businessa.com",
        "email": "info@businessa.com",
        "phone_number": "123-456-7890",
        "address": "123 Main St",
        "status": "active",
        "contacts": [
            { "type": "email", "value": "info@businessa.com", "source": "csv" },
            { "type": "instagram", "value": "http://instagram.com/businessa", "source": "scanned_social_media" }
        ]
    }
    ```

#### `PUT /api/businesses/{id}`

Updates details for a single business.

*   **Path Parameters:**
    *   `id`: Business ID
*   **Request:** `application/json`
    ```json
    {
        "name": "Updated Business A",
        "website": "http://newbusinessa.com"
    }
    ```
*   **Response:** `200 OK` or `404 Not Found`
    ```json
    {
        "message": "Business updated successfully.",
        "business": { "id": 1, "name": "Updated Business A", ... }
    }
    ```

#### `DELETE /api/businesses/{id}`

Deletes a business.

*   **Path Parameters:**
    *   `id`: Business ID
*   **Response:** `204 No Content` or `404 Not Found`

### 3.2. Campaign Endpoints

#### `POST /api/campaigns`

Creates a new outreach campaign.

*   **Request:** `application/json`
    ```json
    {
        "name": "Summer Promotion 2025",
        "message_template": "Hi {business_name}, check out our new offer at {website_link}!"
    }
    ```
*   **Response:** `201 Created`
    ```json
    {
        "message": "Campaign created successfully.",
        "campaign": { "id": 1, "name": "Summer Promotion 2025", ... }
    }
    ```

#### `GET /api/campaigns`

Retrieves a list of campaigns.

*   **Query Parameters:**
    *   `page`: Page number (default: 1)
    *   `per_page`: Items per page (default: 20)
    *   `status`: Filter by campaign status
*   **Response:** `200 OK`
    ```json
    {
        "campaigns": [
            { "id": 1, "name": "Summer Promotion 2025", "status": "draft", ... },
            // ...
        ],
        "total_pages": 2,
        "current_page": 1,
        "total_items": 15
    }
    ```

#### `GET /api/campaigns/{id}`

Retrieves details for a single campaign, including message statuses.

*   **Path Parameters:**
    *   `id`: Campaign ID
*   **Response:** `200 OK` or `404 Not Found`
    ```json
    {
        "id": 1,
        "name": "Summer Promotion 2025",
        "message_template": "Hi {business_name}, ...",
        "status": "sending",
        "messages_summary": {
            "total": 100,
            "sent": 80,
            "failed": 5,
            "opened": 30,
            "replied": 10
        },
        "messages": [
            { "id": 101, "business_name": "Business X", "platform": "email", "status": "sent", ... },
            // ... (detailed message list, possibly paginated in a real app)
        ]
    }
    ```

#### `POST /api/campaigns/{id}/send`

Manually triggers message sending for a campaign.

*   **Path Parameters:**
    *   `id`: Campaign ID
*   **Response:** `202 Accepted` or `404 Not Found`
    ```json
    {
        "message": "Campaign sending initiated.",
        "task_id": "<celery_task_id>"
    }
    ```

#### `POST /api/campaigns/{id}/pause`

Pauses an active campaign.

*   **Path Parameters:**
    *   `id`: Campaign ID
*   **Response:** `200 OK` or `404 Not Found`
    ```json
    {
        "message": "Campaign paused."
    }
    ```

#### `POST /api/campaigns/{id}/resume`

Resumes a paused campaign.

*   **Path Parameters:**
    *   `id`: Campaign ID
*   **Response:** `200 OK` or `404 Not Found`
    ```json
    {
        "message": "Campaign resumed."
    }
    ```

### 3.3. Analytics Endpoints

#### `GET /api/analytics/summary`

Retrieves overall analytics summary.

*   **Query Parameters:**
    *   `start_date`: YYYY-MM-DD
    *   `end_date`: YYYY-MM-DD
*   **Response:** `200 OK`
    ```json
    {
        "total_businesses": 1000,
        "total_campaigns": 50,
        "total_messages_sent": 5000,
        "overall_open_rate": 0.65,
        "overall_reply_rate": 0.15,
        "overall_click_through_rate": 0.05,
        "performance_by_platform": {
            "email": { "sent": 3000, "opened": 2000, "replied": 300 },
            "instagram": { "sent": 1000, "opened": 500, "replied": 100 }
        },
        "daily_performance": [
            { "date": "2025-07-01", "sent": 100, "opened": 60, "replied": 10 },
            // ...
        ]
    }
    ```

#### `GET /api/analytics/campaigns/{id}`

Retrieves analytics for a specific campaign.

*   **Path Parameters:**
    *   `id`: Campaign ID
*   **Query Parameters:**
    *   `start_date`: YYYY-MM-DD
    *   `end_date`: YYYY-MM-DD
*   **Response:** `200 OK` or `404 Not Found`
    ```json
    {
        "campaign_id": 1,
        "campaign_name": "Summer Promotion 2025",
        "total_messages_sent": 200,
        "open_rate": 0.70,
        "reply_rate": 0.20,
        "click_through_rate": 0.08,
        "performance_by_platform": {
            "email": { "sent": 150, "opened": 100, "replied": 20 },
            "linkedin": { "sent": 50, "opened": 30, "replied": 5 }
        },
        "message_status_distribution": {
            "sent": 180,
            "failed": 20,
            "opened": 120,
            "replied": 25
        }
    }
    ```

#### `GET /api/analytics/export`

Exports analytics data as CSV or PDF.

*   **Query Parameters:**
    *   `format`: `csv` or `pdf` (default: `csv`)
    *   `campaign_id`: (Optional) Export for a specific campaign
    *   `start_date`: YYYY-MM-DD
    *   `end_date`: YYYY-MM-DD
*   **Response:** `200 OK` with file download (CSV or PDF content)

## 4. Error Handling

API errors will return appropriate HTTP status codes and a JSON body with an `error` message.

```json
{
    "error": "Resource not found."
}
```

## 5. Authentication

(Reiterating for clarity)

All API requests will require a valid JWT (JSON Web Token) in the `Authorization` header:

`Authorization: Bearer <your_jwt_token>`

Login endpoint:

#### `POST /api/auth/login`

Authenticates a user and returns a JWT.

*   **Request:** `application/json`
    ```json
    {
        "username": "user",
        "password": "password"
    }
    ```
*   **Response:** `200 OK`
    ```json
    {
        "access_token": "<your_jwt_token>",
        "token_type": "bearer"
    }
    ```

## 6. Webhooks (Optional but Recommended)

To ensure real-time updates for message statuses (e.g., email opens, replies), the system can be configured to receive webhooks from integrated third-party services. This would involve:

*   Dedicated webhook endpoints on the Backend (e.g., `/webhooks/mailgun`, `/webhooks/instagram`).
*   Validation of incoming webhook requests (e.g., signature verification).
*   Asynchronous processing of webhook data via the Task Queue to update message statuses in the database.

