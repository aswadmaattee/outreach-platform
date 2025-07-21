# Business Outreach Platform - Development Environment Setup

This document provides instructions for setting up the development environment for the Business Outreach Platform.

## 1. Prerequisites

Ensure you have the following installed on your system:

*   **Python 3.9+**
*   **pip** (Python package installer)
*   **PostgreSQL** database server
*   **Redis** server (for Celery broker and backend)
*   **Node.js and npm/yarn** (for frontend development)

## 2. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd business_outreach_platform/backend
    ```

2.  **Create a Python virtual environment:**
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install Python dependencies:**
    Create a `requirements.txt` file in the `backend` directory with the following content:
    ```
    Flask
    Flask-SQLAlchemy
    psycopg2-binary
    python-dotenv
    Flask-Migrate
    Celery
    redis
    requests
    beautifulsoup4
    lxml
    python-decouple
    Flask-CORS
    Flask-JWT-Extended
    gunicorn
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Variables:**
    Create a `.env` file in the `backend` directory:
    ```
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    REDIS_URL="redis://localhost:6379/0"
    SECRET_KEY="your_super_secret_key_here"
    MAILGUN_API_KEY="your_mailgun_api_key"
    MAILGUN_DOMAIN="your_mailgun_domain"
    GOOGLE_CSE_API_KEY="your_google_cse_api_key"
    GOOGLE_CSE_CX="your_google_cse_cx"
    SCRAPINGBEE_API_KEY="your_scrapingbee_api_key"
    ```
    *   Replace placeholders with your actual database, Redis, and API credentials.
    *   `SECRET_KEY` should be a strong, random string.

6.  **Database Setup and Migrations:**
    *   Initialize Flask-Migrate:
        ```bash
        flask db init
        ```
    *   Create a migration:
        ```bash
        flask db migrate -m "Initial migration"
        ```
    *   Apply migrations:
        ```bash
        flask db upgrade
        ```

7.  **Run the Flask Application:**
    ```bash
    flask run
    ```
    The API server will typically run on `http://127.0.0.1:5000`.

8.  **Run Celery Worker:**
    In a separate terminal, activate the virtual environment and run:
    ```bash
    celery -A app.celery worker --loglevel=info
    ```

## 3. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd business_outreach_platform/frontend
    ```

2.  **Create a React application:**
    ```bash
    npx create-react-app .
    ```
    (Note: `.` means create in the current directory)

3.  **Install Node.js dependencies:**
    ```bash
    npm install # or yarn install
    ```

4.  **Environment Variables:**
    Create a `.env` file in the `frontend` directory:
    ```
    REACT_APP_API_BASE_URL="http://127.0.0.1:5000/api"
    ```

5.  **Run the React Application:**
    ```bash
    npm start # or yarn start
    ```
    The frontend development server will typically run on `http://localhost:3000`.

## 4. Testing

*   Access the frontend application in your browser (`http://localhost:3000`).
*   Interact with the UI to test CSV upload, business management, campaign creation, and analytics display.
*   Monitor backend logs and Celery worker logs for any errors or issues.

This setup provides a complete local development environment for the Business Outreach Platform.

