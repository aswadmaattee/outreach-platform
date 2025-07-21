# Business Outreach Platform

A complete web-based platform for automated business outreach, contact discovery, and campaign management.

## 🚀 Features

### CSV Upload System
- Upload CSV files with business information
- Support for hundreds of entries at once
- Automatic data validation and duplicate detection
- Required: Business Name | Optional: Website, Email, Phone, Address

### Online Presence Scanner
- Automatically finds official websites
- Discovers social media accounts (Instagram, Facebook, Twitter/X, LinkedIn)
- Extracts contact information (emails, phone numbers, contact forms)
- Smart rate limiting and error handling

### Personalized Outreach System
- Send custom messages to all available contact options
- Email integration (SMTP/API ready)
- Social media messaging (Instagram DMs, Facebook Pages, LinkedIn)
- Auto-personalization with business name and website

### Dashboard UI
- Clean, responsive interface
- Real-time status updates for all platforms
- Filtering by platform, status, and date
- Add/Edit/Delete contacts functionality
- Import new CSVs without losing existing data

### Analytics & Reporting
- Open rates, reply rates, click-through metrics
- Interactive charts and visualizations
- Export analytics as CSV
- Performance tracking and comparisons

## 🛠 Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **API**: RESTful with JSON responses
- **Task Processing**: Celery (for background jobs)
- **Web Scraping**: BeautifulSoup, Requests

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **Build Tool**: Vite

### Key Libraries
- Flask-CORS for cross-origin requests
- SQLAlchemy for database ORM
- Werkzeug for file uploads
- React Router for navigation

## 📋 Prerequisites

- Python 3.11+
- Node.js 20+
- npm or pnpm

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend/outreach_platform
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

Backend will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
cd frontend/business-outreach-dashboard
npm install  # or pnpm install
npm run dev  # or pnpm dev
```

Frontend will run on `http://localhost:5173`

### 3. Access the Platform

Open your browser and navigate to `http://localhost:5173`

## 📁 Project Structure

```
business_outreach_platform/
├── backend/
│   └── outreach_platform/
│       ├── src/
│       │   ├── models/          # Database models
│       │   ├── routes/          # API endpoints
│       │   ├── tasks/           # Background tasks
│       │   └── main.py          # Flask application
│       ├── venv/                # Python virtual environment
│       └── requirements.txt     # Python dependencies
├── frontend/
│   └── business-outreach-dashboard/
│       ├── src/
│       │   ├── components/      # React components
│       │   └── App.jsx          # Main application
│       ├── package.json         # Node dependencies
│       └── vite.config.js       # Build configuration
├── docs/                        # Documentation
├── test_results.md             # Testing results
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Email Configuration (for production)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Social Media API Keys (for production)
INSTAGRAM_ACCESS_TOKEN=your-token
FACEBOOK_ACCESS_TOKEN=your-token
LINKEDIN_ACCESS_TOKEN=your-token

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost/outreach_db
```

### API Keys Setup

For production deployment, you'll need to obtain API keys for:

1. **Email Service**: Gmail App Password, Mailgun API, or SendGrid
2. **Social Media APIs**:
   - Instagram Basic Display API
   - Facebook Graph API
   - LinkedIn API
3. **Search APIs** (optional): Google Custom Search API

## 📊 Usage Guide

### 1. Upload Business Data

1. Navigate to "CSV Upload" in the sidebar
2. Download the sample CSV template
3. Fill in your business data (Business Name is required)
4. Upload the CSV file
5. Review the imported businesses in the "Businesses" section

### 2. Scan for Online Presence

1. Go to "Scanner" in the sidebar
2. Click "Scan All Pending Businesses"
3. Monitor the progress as the system finds social media profiles and contacts
4. Review discovered contacts in the "Businesses" section

### 3. Create and Send Campaigns

1. Navigate to "Campaigns"
2. Click "New Campaign"
3. Enter campaign name and message template
4. Use placeholders like `{business_name}` and `{website}` for personalization
5. Click "Create Campaign"
6. Click the play button to send messages

### 4. Monitor Analytics

1. Go to "Analytics" to view performance metrics
2. See campaign performance charts and message status distribution
3. Export detailed reports using the "Export" button
4. Filter by date ranges for specific time periods

## 🔒 Security Features

- File upload validation and size limits
- SQL injection prevention with SQLAlchemy ORM
- CORS configuration for secure API access
- Input validation and sanitization
- Error handling without information leakage

## 🚀 Deployment Options

### Option 1: Local Development
- Follow the Quick Start guide above
- Suitable for testing and small-scale use

### Option 2: Cloud Deployment
- Deploy backend to services like Heroku, DigitalOcean, or AWS
- Deploy frontend to Netlify, Vercel, or similar
- Use PostgreSQL for production database

### Option 3: Docker Deployment
- Containerize both frontend and backend
- Use docker-compose for easy deployment
- Suitable for VPS or cloud instances

## 📈 Scaling Considerations

### For High Volume Usage:
1. **Database**: Migrate from SQLite to PostgreSQL
2. **Task Queue**: Set up Redis for Celery background tasks
3. **Caching**: Implement Redis caching for API responses
4. **Load Balancing**: Use nginx for multiple backend instances
5. **Monitoring**: Add logging and monitoring tools

## 🐛 Troubleshooting

### Common Issues:

1. **Backend won't start**:
   - Ensure Python 3.11+ is installed
   - Activate virtual environment
   - Install all requirements: `pip install -r requirements.txt`

2. **Frontend won't start**:
   - Ensure Node.js 20+ is installed
   - Install dependencies: `npm install`
   - Check for port conflicts

3. **API connection issues**:
   - Verify backend is running on port 5000
   - Check CORS configuration
   - Ensure no firewall blocking

4. **CSV upload fails**:
   - Check file format (must be CSV)
   - Verify "Business Name" column exists
   - Ensure file size is under 10MB

## 📞 Support

For technical support or questions:
1. Check the troubleshooting section above
2. Review the documentation in the `docs/` folder
3. Check the test results in `test_results.md`

## 📄 License

This project is provided as-is for the specified use case. All rights reserved.

## 🎯 Next Steps

1. Set up production environment variables
2. Obtain necessary API keys for email and social media
3. Configure your preferred email service
4. Deploy to your chosen hosting platform
5. Start uploading your business data and creating campaigns!

---

**Built with ❤️ for efficient business outreach automation**

