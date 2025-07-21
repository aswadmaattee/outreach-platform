# Business Outreach Platform - Technical Architecture

## 1. Overview

This document outlines the technical architecture for a web-based platform designed to automate business outreach. The platform will handle CSV uploads of business data, perform online presence scanning, facilitate personalized outreach via multiple channels, and provide a dashboard with analytics.

## 2. Core Components

The platform will consist of the following main components:

*   **Frontend (React.js):** A single-page application (SPA) providing the user interface for CSV upload, dashboard, contact management, campaign creation, and analytics visualization. It will communicate with the backend via RESTful APIs.

*   **Backend (Flask/Python):** A robust backend API server responsible for:
    *   Handling CSV file uploads and parsing.
    *   Managing business data storage (database interactions).
    *   Orchestrating the online presence scanning process.
    *   Managing outreach campaigns and message sending.
    *   Collecting and processing analytics data.
    *   Interacting with third-party APIs.

*   **Database (PostgreSQL):** A relational database to store business information, contact details, social media links, campaign data, message statuses, and analytics metrics.

*   **Task Queue (Celery with Redis):** For handling long-running and asynchronous tasks such as CSV processing, online presence scanning, and sending outreach messages. This ensures the main application remains responsive.

*   **Third-Party APIs:** Integration with various external services for:
    *   **Web Search:** Google Search API or similar for finding websites and social media profiles.
    *   **Email:** SMTP, Mailgun, SendGrid, or similar for sending personalized emails.
    *   **Social Media:** APIs for Instagram, Facebook, Twitter/X, LinkedIn (if available and permissible for automated messaging).

## 3. Data Flow

1.  **CSV Upload:** User uploads a CSV file via the Frontend. The Frontend sends the file to a dedicated Backend API endpoint.
2.  **CSV Processing:** The Backend receives the CSV, validates it, and dispatches a task to the Task Queue for asynchronous processing. The Task Queue parses the CSV and stores business data in the Database.
3.  **Online Presence Scanning:** For each business, a task is added to the Task Queue. This task involves:
    *   Searching for official websites (if not provided).
    *   Searching for social media profiles (Instagram, Facebook, Twitter/X, LinkedIn).
    *   Extracting contact information (emails, phone numbers, contact forms).
    *   Updating the Database with the discovered information.
4.  **Outreach Campaign Creation:** User creates an outreach campaign via the Frontend, selecting businesses and customizing message templates. The Frontend sends this data to the Backend.
5.  **Message Generation & Sending:** The Backend generates personalized messages for each contact based on templates and business data. These messages are then dispatched as tasks to the Task Queue.
6.  **Third-Party API Interaction:** The Task Queue workers interact with the respective third-party APIs (Email, Social Media) to send messages.
7.  **Status Updates:** Message delivery statuses (Sent, Failed, Opened, Replied) are updated in the Database, either via webhooks from third-party services or direct API responses.
8.  **Dashboard & Analytics:** The Frontend fetches data from the Backend APIs to display real-time message statuses, campaign performance, and analytics charts.

## 4. API Specifications (High-Level)

### Business Management
*   `POST /api/businesses/upload`: Upload CSV for new businesses.
*   `GET /api/businesses`: Retrieve all businesses with filtering and pagination.
*   `GET /api/businesses/{id}`: Retrieve a single business.
*   `PUT /api/businesses/{id}`: Update business details.
*   `DELETE /api/businesses/{id}`: Delete a business.

### Campaign Management
*   `POST /api/campaigns`: Create a new outreach campaign.
*   `GET /api/campaigns`: Retrieve all campaigns.
*   `GET /api/campaigns/{id}`: Retrieve a single campaign with message statuses.
*   `POST /api/campaigns/{id}/send`: Manually trigger message sending for a campaign.
*   `POST /api/campaigns/{id}/pause`: Pause a campaign.
*   `POST /api/campaigns/{id}/resume`: Resume a campaign.

### Analytics
*   `GET /api/analytics/summary`: Get overall analytics summary.
*   `GET /api/analytics/campaigns/{id}`: Get analytics for a specific campaign.
*   `GET /api/analytics/export`: Export analytics data (CSV/PDF).

## 5. Database Schema (Conceptual)

*   **Businesses Table:**
    *   `id` (PK)
    *   `name`
    *   `website`
    *   `email`
    *   `phone_number`
    *   `address`
    *   `status` (e.g., 'pending_scan', 'scanned', 'active')

*   **Contacts Table:**
    *   `id` (PK)
    *   `business_id` (FK to Businesses)
    *   `type` (e.g., 'email', 'instagram', 'facebook', 'linkedin', 'phone', 'contact_form')
    *   `value` (e.g., email address, social media URL, phone number)
    *   `source` (e.g., 'csv', 'scanned_website', 'scanned_social_media')

*   **Campaigns Table:**
    *   `id` (PK)
    *   `name`
    *   `message_template`
    *   `status` (e.g., 'draft', 'scheduled', 'sending', 'paused', 'completed')
    *   `created_at`
    *   `updated_at`

*   **Messages Table:**
    *   `id` (PK)
    *   `campaign_id` (FK to Campaigns)
    *   `business_id` (FK to Businesses)
    *   `contact_id` (FK to Contacts)
    *   `platform` (e.g., 'email', 'instagram', 'facebook', 'linkedin')
    *   `personalized_content`
    *   `status` (e.g., 'sent', 'failed', 'opened', 'replied')
    *   `sent_at`
    *   `opened_at`
    *   `replied_at`

## 6. Technology Stack

*   **Backend:** Python 3.x, Flask, SQLAlchemy (ORM), Celery, Redis
*   **Frontend:** React.js, HTML5, CSS3, JavaScript
*   **Database:** PostgreSQL
*   **Deployment:** Docker (for containerization), Nginx (reverse proxy)

## 7. Development Environment Setup

Instructions for setting up the development environment will be provided in a separate `DEVELOPMENT.md` file.

