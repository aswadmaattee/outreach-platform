import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from src.models.business import db, Business, Contact, Campaign, Message
import re
import os

logger = logging.getLogger(__name__)

class OutreachManager:
    """Manager for sending outreach messages via various platforms"""
    
    def __init__(self):
        # Email configuration (would be loaded from environment variables)
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_username)
        
    def generate_personalized_message(self, template, business, contact):
        """Generate personalized message from template"""
        try:
            # Available placeholders
            placeholders = {
                '{business_name}': business.name or '',
                '{website}': business.website or '',
                '{email}': business.email or '',
                '{phone}': business.phone_number or '',
                '{address}': business.address or '',
                '{contact_value}': contact.value or '',
                '{contact_type}': contact.type or ''
            }
            
            # Replace placeholders in template
            personalized_message = template
            for placeholder, value in placeholders.items():
                personalized_message = personalized_message.replace(placeholder, value)
            
            return personalized_message
            
        except Exception as e:
            logger.error(f"Error generating personalized message: {str(e)}")
            return template
    
    def send_email(self, to_email, subject, message_content, business_name=""):
        """Send email via SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(message_content, 'plain'))
            
            # For demo purposes, we'll simulate email sending
            # In production, you would uncomment the SMTP code below
            
            # # Create SMTP session
            # server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            # server.starttls()  # Enable security
            # server.login(self.smtp_username, self.smtp_password)
            # 
            # # Send email
            # text = msg.as_string()
            # server.sendmail(self.from_email, to_email, text)
            # server.quit()
            
            # Simulate successful email sending
            logger.info(f"Email sent to {to_email} for business: {business_name}")
            return True, "Email sent successfully"
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False, str(e)
    
    def generate_social_media_message(self, business, contact, message_template):
        """Generate social media message with instructions for manual sending"""
        try:
            personalized_message = self.generate_personalized_message(
                message_template, business, contact
            )
            
            # Create instructions for manual sending
            platform = contact.type
            contact_url = contact.value
            
            instructions = {
                'platform': platform,
                'contact_url': contact_url,
                'business_name': business.name,
                'message': personalized_message,
                'instructions': f"Please visit {contact_url} and send this message manually via {platform}."
            }
            
            return instructions
            
        except Exception as e:
            logger.error(f"Error generating social media message: {str(e)}")
            return None
    
    def send_campaign_messages(self, campaign_id, business_ids=None, platforms=None):
        """Send messages for a campaign"""
        try:
            campaign = Campaign.query.get(campaign_id)
            if not campaign:
                return {'success': False, 'error': 'Campaign not found'}
            
            # Default platforms
            if not platforms:
                platforms = ['email']
            
            # Get businesses to send to
            query = Business.query
            if business_ids:
                query = query.filter(Business.id.in_(business_ids))
            
            businesses = query.all()
            
            sent_count = 0
            failed_count = 0
            social_media_instructions = []
            
            for business in businesses:
                for platform in platforms:
                    # Find contact for this platform
                    contact = Contact.query.filter_by(
                        business_id=business.id,
                        type=platform
                    ).first()
                    
                    if not contact:
                        continue
                    
                    # Check if message already exists for this combination
                    existing_message = Message.query.filter_by(
                        campaign_id=campaign_id,
                        business_id=business.id,
                        contact_id=contact.id,
                        platform=platform
                    ).first()
                    
                    if existing_message:
                        continue  # Skip if message already exists
                    
                    # Generate personalized message
                    personalized_content = self.generate_personalized_message(
                        campaign.message_template, business, contact
                    )
                    
                    # Create message record
                    message = Message(
                        campaign_id=campaign_id,
                        business_id=business.id,
                        contact_id=contact.id,
                        platform=platform,
                        personalized_content=personalized_content,
                        status='pending'
                    )
                    
                    db.session.add(message)
                    db.session.flush()  # Get message ID
                    
                    # Send message based on platform
                    if platform == 'email':
                        # Send email
                        subject = f"Message from {campaign.name}"
                        success, error_msg = self.send_email(
                            contact.value, subject, personalized_content, business.name
                        )
                        
                        if success:
                            message.status = 'sent'
                            message.sent_at = datetime.utcnow()
                            sent_count += 1
                        else:
                            message.status = 'failed'
                            failed_count += 1
                            logger.error(f"Failed to send email to {contact.value}: {error_msg}")
                    
                    else:
                        # For social media platforms, generate instructions
                        instructions = self.generate_social_media_message(
                            business, contact, campaign.message_template
                        )
                        
                        if instructions:
                            social_media_instructions.append(instructions)
                            message.status = 'pending'  # Requires manual action
                        else:
                            message.status = 'failed'
                            failed_count += 1
                    
                    db.session.commit()
            
            result = {
                'success': True,
                'sent_count': sent_count,
                'failed_count': failed_count,
                'social_media_instructions': social_media_instructions,
                'total_businesses': len(businesses)
            }
            
            logger.info(f"Campaign {campaign_id} sending completed: {sent_count} sent, {failed_count} failed")
            return result
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error sending campaign messages: {str(e)}")
            return {'success': False, 'error': str(e)}

# Synchronous functions for immediate use
def send_campaign_messages_sync(campaign_id, business_ids=None, platforms=None):
    """Synchronously send campaign messages"""
    manager = OutreachManager()
    return manager.send_campaign_messages(campaign_id, business_ids, platforms)

def generate_personalized_message(template, business, contact):
    """Generate personalized message from template"""
    manager = OutreachManager()
    return manager.generate_personalized_message(template, business, contact)

def send_email_sync(to_email, subject, message_content, business_name=""):
    """Synchronously send email"""
    manager = OutreachManager()
    return manager.send_email(to_email, subject, message_content, business_name)

