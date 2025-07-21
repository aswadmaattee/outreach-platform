# Deployment Guide - Business Outreach Platform

This guide provides step-by-step instructions for deploying the Business Outreach Platform from scratch.

## 🎯 Deployment Options

### Option 1: Local Development Setup (Recommended for Testing)
### Option 2: Cloud Deployment (Recommended for Production)
### Option 3: VPS/Server Deployment

---

## 🖥 Option 1: Local Development Setup

### Prerequisites
- Python 3.11 or higher
- Node.js 20 or higher
- Git (optional, for version control)

### Step 1: Extract and Setup Project

1. Extract the ZIP file to your desired location
2. Open terminal/command prompt
3. Navigate to the project directory:
   ```bash
   cd business_outreach_platform
   ```

### Step 2: Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend/outreach_platform
   ```

2. Create Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   ```bash
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Initialize database:
   ```bash
   python src/main.py
   ```
   (This will create the database automatically on first run)

6. Keep the backend running (you should see "Running on http://127.0.0.1:5000")

### Step 3: Frontend Setup

1. Open a new terminal window
2. Navigate to frontend directory:
   ```bash
   cd business_outreach_platform/frontend/business-outreach-dashboard
   ```

3. Install Node.js dependencies:
   ```bash
   npm install
   ```
   Or if you prefer pnpm:
   ```bash
   pnpm install
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```
   Or with pnpm:
   ```bash
   pnpm dev
   ```

5. Open your browser and go to `http://localhost:5173`

### Step 4: Verify Installation

1. You should see the Business Outreach Platform dashboard
2. Try uploading the sample CSV file (create one with Business Name, Website, Email columns)
3. Test the scanner functionality
4. Create a test campaign

---

## ☁️ Option 2: Cloud Deployment

### Backend Deployment (Heroku Example)

1. **Prepare for Heroku deployment:**
   ```bash
   cd backend/outreach_platform
   ```

2. **Create Procfile:**
   ```bash
   echo "web: python src/main.py" > Procfile
   ```

3. **Create runtime.txt:**
   ```bash
   echo "python-3.11.0" > runtime.txt
   ```

4. **Update main.py for production:**
   ```python
   import os
   
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       app.run(host='0.0.0.0', port=port, debug=False)
   ```

5. **Deploy to Heroku:**
   ```bash
   heroku create your-app-name-backend
   heroku addons:create heroku-postgresql:hobby-dev
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

### Frontend Deployment (Netlify Example)

1. **Build the frontend:**
   ```bash
   cd frontend/business-outreach-dashboard
   npm run build
   ```

2. **Update API URL in frontend:**
   - Edit `src/App.jsx`
   - Change `http://localhost:5000` to your Heroku backend URL

3. **Deploy to Netlify:**
   - Drag and drop the `dist` folder to Netlify
   - Or connect your Git repository for automatic deployments

### Environment Variables for Production

Set these environment variables in your hosting platform:

```env
# Database
DATABASE_URL=postgresql://...

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Social Media APIs (obtain from respective platforms)
INSTAGRAM_ACCESS_TOKEN=your-token
FACEBOOK_ACCESS_TOKEN=your-token
LINKEDIN_ACCESS_TOKEN=your-token

# Security
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

---

## 🖥 Option 3: VPS/Server Deployment

### Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Root or sudo access
- Domain name (optional but recommended)

### Step 1: Server Setup

1. **Update system:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install required software:**
   ```bash
   sudo apt install python3.11 python3.11-venv python3-pip nodejs npm nginx postgresql postgresql-contrib -y
   ```

3. **Install PM2 for process management:**
   ```bash
   sudo npm install -g pm2
   ```

### Step 2: Database Setup

1. **Setup PostgreSQL:**
   ```bash
   sudo -u postgres createuser --interactive
   sudo -u postgres createdb outreach_platform
   ```

2. **Configure database connection in your app**

### Step 3: Backend Deployment

1. **Upload and extract project files:**
   ```bash
   cd /var/www/
   sudo mkdir outreach_platform
   sudo chown $USER:$USER outreach_platform
   # Upload and extract your ZIP file here
   ```

2. **Setup Python environment:**
   ```bash
   cd /var/www/outreach_platform/backend/outreach_platform
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create PM2 ecosystem file:**
   ```javascript
   // ecosystem.config.js
   module.exports = {
     apps: [{
       name: 'outreach-backend',
       script: 'src/main.py',
       interpreter: 'venv/bin/python',
       cwd: '/var/www/outreach_platform/backend/outreach_platform',
       env: {
         FLASK_ENV: 'production',
         DATABASE_URL: 'postgresql://user:password@localhost/outreach_platform'
       }
     }]
   };
   ```

4. **Start with PM2:**
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

### Step 4: Frontend Deployment

1. **Build frontend:**
   ```bash
   cd /var/www/outreach_platform/frontend/business-outreach-dashboard
   npm install
   npm run build
   ```

2. **Configure Nginx:**
   ```nginx
   # /etc/nginx/sites-available/outreach_platform
   server {
       listen 80;
       server_name your-domain.com;
       
       # Frontend
       location / {
           root /var/www/outreach_platform/frontend/business-outreach-dashboard/dist;
           try_files $uri $uri/ /index.html;
       }
       
       # Backend API
       location /api/ {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Enable site:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/outreach_platform /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Step 5: SSL Certificate (Optional but Recommended)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔧 Configuration Files

### Backend Environment Variables (.env)

Create `/var/www/outreach_platform/backend/outreach_platform/.env`:

```env
DATABASE_URL=postgresql://username:password@localhost/outreach_platform
SECRET_KEY=your-very-secret-key-here
FLASK_ENV=production

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Social Media APIs
INSTAGRAM_ACCESS_TOKEN=your-instagram-token
FACEBOOK_ACCESS_TOKEN=your-facebook-token
LINKEDIN_ACCESS_TOKEN=your-linkedin-token
```

### Frontend Configuration

Update `frontend/business-outreach-dashboard/src/App.jsx`:

```javascript
// Change this line:
const API_BASE_URL = 'http://localhost:5000';

// To your production URL:
const API_BASE_URL = 'https://your-domain.com';
```

---

## 🔍 Verification Steps

### 1. Backend Health Check
```bash
curl http://your-domain.com/api/businesses
```
Should return JSON response with businesses data.

### 2. Frontend Access
Visit `http://your-domain.com` in your browser.
You should see the dashboard interface.

### 3. Full Workflow Test
1. Upload a CSV file
2. Run the scanner
3. Create a campaign
4. Check analytics

---

## 🚨 Troubleshooting

### Common Issues:

1. **Database Connection Error:**
   - Check PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify database credentials in .env file
   - Ensure database exists: `sudo -u postgres psql -l`

2. **Permission Errors:**
   - Check file ownership: `sudo chown -R www-data:www-data /var/www/outreach_platform`
   - Verify Python virtual environment activation

3. **Nginx 502 Error:**
   - Check backend is running: `pm2 status`
   - Verify proxy_pass URL in Nginx config
   - Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`

4. **Frontend Build Issues:**
   - Ensure Node.js version is 20+: `node --version`
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### Log Files:
- Backend logs: `pm2 logs outreach-backend`
- Nginx logs: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`
- System logs: `journalctl -u nginx`

---

## 📊 Performance Optimization

### For High Traffic:

1. **Database Optimization:**
   - Add database indexes
   - Use connection pooling
   - Consider read replicas

2. **Caching:**
   - Install Redis: `sudo apt install redis-server`
   - Configure Flask-Caching
   - Cache API responses

3. **Load Balancing:**
   - Run multiple backend instances
   - Configure Nginx upstream
   - Use PM2 cluster mode

4. **Monitoring:**
   - Set up monitoring with PM2 Plus
   - Configure log rotation
   - Monitor database performance

---

## 🔐 Security Checklist

- [ ] Change default passwords
- [ ] Configure firewall (ufw)
- [ ] Set up SSL certificates
- [ ] Regular security updates
- [ ] Backup strategy
- [ ] Monitor access logs
- [ ] Use environment variables for secrets
- [ ] Configure rate limiting

---

## 📞 Support

If you encounter issues during deployment:

1. Check the troubleshooting section above
2. Review log files for specific error messages
3. Ensure all prerequisites are installed correctly
4. Verify network connectivity and firewall settings

---

**Deployment completed successfully! Your Business Outreach Platform is now live and ready for use.**

