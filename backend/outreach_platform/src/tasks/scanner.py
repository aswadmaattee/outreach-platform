import requests
from bs4 import BeautifulSoup
import re
import time
import logging
from urllib.parse import urljoin, urlparse
from src.models.business import db, Business, Contact

logger = logging.getLogger(__name__)

class OnlinePresenceScanner:
    """Scanner for finding business websites and social media profiles"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Social media patterns
        self.social_patterns = {
            'instagram': [
                r'instagram\.com/([a-zA-Z0-9_.]+)',
                r'instagr\.am/([a-zA-Z0-9_.]+)'
            ],
            'facebook': [
                r'facebook\.com/([a-zA-Z0-9_.]+)',
                r'fb\.com/([a-zA-Z0-9_.]+)',
                r'facebook\.com/pages/([^/]+/[0-9]+)'
            ],
            'twitter': [
                r'twitter\.com/([a-zA-Z0-9_]+)',
                r'x\.com/([a-zA-Z0-9_]+)'
            ],
            'linkedin': [
                r'linkedin\.com/company/([a-zA-Z0-9-]+)',
                r'linkedin\.com/in/([a-zA-Z0-9-]+)'
            ]
        }
        
        # Email pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Phone patterns
        self.phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # International
        ]
    
    def search_business_website(self, business_name, location=None):
        """Search for business website using search engines"""
        try:
            # Simple search query
            query = f'"{business_name}"'
            if location:
                query += f' {location}'
            query += ' site:'
            
            # For now, we'll simulate a search result
            # In a real implementation, you would use Google Custom Search API
            logger.info(f"Searching for website of: {business_name}")
            
            # Return None for now - would implement actual search API here
            return None
            
        except Exception as e:
            logger.error(f"Error searching for business website: {str(e)}")
            return None
    
    def extract_social_media_links(self, url):
        """Extract social media links from a website"""
        social_links = {}
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get all links
            links = soup.find_all('a', href=True)
            
            # Extract social media links
            for link in links:
                href = link['href']
                
                for platform, patterns in self.social_patterns.items():
                    for pattern in patterns:
                        match = re.search(pattern, href, re.IGNORECASE)
                        if match:
                            # Clean up the URL
                            if not href.startswith('http'):
                                href = urljoin(url, href)
                            
                            if platform not in social_links:
                                social_links[platform] = []
                            
                            if href not in social_links[platform]:
                                social_links[platform].append(href)
                            break
            
            logger.info(f"Found social media links for {url}: {social_links}")
            return social_links
            
        except Exception as e:
            logger.error(f"Error extracting social media links from {url}: {str(e)}")
            return {}
    
    def extract_contact_info(self, url):
        """Extract contact information from a website"""
        contact_info = {
            'emails': [],
            'phones': [],
            'contact_forms': []
        }
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text()
            
            # Extract emails
            emails = re.findall(self.email_pattern, text_content)
            contact_info['emails'] = list(set(emails))
            
            # Extract phone numbers
            phones = []
            for pattern in self.phone_patterns:
                found_phones = re.findall(pattern, text_content)
                phones.extend(found_phones)
            contact_info['phones'] = list(set(phones))
            
            # Look for contact forms
            forms = soup.find_all('form')
            for form in forms:
                # Check if form has email input or contact-related fields
                inputs = form.find_all(['input', 'textarea'])
                has_email_field = any(
                    'email' in input.get('name', '').lower() or 
                    'email' in input.get('type', '').lower() or
                    'email' in input.get('id', '').lower()
                    for input in inputs
                )
                
                if has_email_field:
                    form_action = form.get('action', '')
                    if form_action:
                        if not form_action.startswith('http'):
                            form_action = urljoin(url, form_action)
                        contact_info['contact_forms'].append(form_action)
            
            logger.info(f"Found contact info for {url}: {contact_info}")
            return contact_info
            
        except Exception as e:
            logger.error(f"Error extracting contact info from {url}: {str(e)}")
            return contact_info
    
    def scan_business(self, business_id):
        """Scan a business for online presence"""
        try:
            business = Business.query.get(business_id)
            if not business:
                logger.error(f"Business with ID {business_id} not found")
                return False
            
            logger.info(f"Scanning business: {business.name}")
            
            # If no website, try to find one
            if not business.website:
                website = self.search_business_website(business.name, business.address)
                if website:
                    business.website = website
                    db.session.commit()
            
            # If we have a website, scan it for social media and contact info
            if business.website:
                # Extract social media links
                social_links = self.extract_social_media_links(business.website)
                
                # Add social media contacts
                for platform, urls in social_links.items():
                    for url in urls:
                        # Check if contact already exists
                        existing_contact = Contact.query.filter_by(
                            business_id=business.id,
                            type=platform,
                            value=url
                        ).first()
                        
                        if not existing_contact:
                            contact = Contact(
                                business_id=business.id,
                                type=platform,
                                value=url,
                                source='scanned_website'
                            )
                            db.session.add(contact)
                
                # Extract contact information
                contact_info = self.extract_contact_info(business.website)
                
                # Add email contacts
                for email in contact_info['emails']:
                    existing_contact = Contact.query.filter_by(
                        business_id=business.id,
                        type='email',
                        value=email
                    ).first()
                    
                    if not existing_contact:
                        contact = Contact(
                            business_id=business.id,
                            type='email',
                            value=email,
                            source='scanned_website'
                        )
                        db.session.add(contact)
                
                # Add phone contacts
                for phone in contact_info['phones']:
                    existing_contact = Contact.query.filter_by(
                        business_id=business.id,
                        type='phone',
                        value=phone
                    ).first()
                    
                    if not existing_contact:
                        contact = Contact(
                            business_id=business.id,
                            type='phone',
                            value=phone,
                            source='scanned_website'
                        )
                        db.session.add(contact)
                
                # Add contact form contacts
                for form_url in contact_info['contact_forms']:
                    existing_contact = Contact.query.filter_by(
                        business_id=business.id,
                        type='contact_form',
                        value=form_url
                    ).first()
                    
                    if not existing_contact:
                        contact = Contact(
                            business_id=business.id,
                            type='contact_form',
                            value=form_url,
                            source='scanned_website'
                        )
                        db.session.add(contact)
            
            # Update business status
            business.status = 'scanned'
            db.session.commit()
            
            logger.info(f"Successfully scanned business: {business.name}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error scanning business {business_id}: {str(e)}")
            return False
    
    def scan_all_pending_businesses(self):
        """Scan all businesses with pending_scan status"""
        try:
            pending_businesses = Business.query.filter_by(status='pending_scan').all()
            
            scanned_count = 0
            for business in pending_businesses:
                if self.scan_business(business.id):
                    scanned_count += 1
                
                # Add delay to avoid overwhelming servers
                time.sleep(2)
            
            logger.info(f"Scanned {scanned_count} out of {len(pending_businesses)} businesses")
            return scanned_count
            
        except Exception as e:
            logger.error(f"Error scanning pending businesses: {str(e)}")
            return 0

# Synchronous function for immediate use
def scan_business_sync(business_id):
    """Synchronously scan a business for online presence"""
    scanner = OnlinePresenceScanner()
    return scanner.scan_business(business_id)

def scan_all_pending_sync():
    """Synchronously scan all pending businesses"""
    scanner = OnlinePresenceScanner()
    return scanner.scan_all_pending_businesses()

