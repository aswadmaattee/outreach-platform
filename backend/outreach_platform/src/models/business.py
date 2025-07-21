from src.models.user import db
from datetime import datetime

class Business(db.Model):
    __tablename__ = 'businesses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    website = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending_scan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contacts = db.relationship('Contact', backref='business', lazy=True, cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='business', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Business {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'contacts': [contact.to_dict() for contact in self.contacts]
        }

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # email, instagram, facebook, twitter, linkedin, phone, contact_form
    value = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(50), nullable=False)  # csv, scanned_website, scanned_social_media
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='contact', lazy=True, cascade='all, delete-orphan')
    
    # Unique constraint to prevent duplicate contacts
    __table_args__ = (db.UniqueConstraint('business_id', 'type', 'value', name='unique_business_contact'),)
    
    def __repr__(self):
        return f'<Contact {self.type}: {self.value}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'business_id': self.business_id,
            'type': self.type,
            'value': self.value,
            'source': self.source,
            'is_primary': self.is_primary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    message_template = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='draft')  # draft, scheduled, sending, paused, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='campaign', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Campaign {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'message_template': self.message_template,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # email, instagram, facebook, twitter, linkedin
    personalized_content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, sent, failed, opened, replied
    sent_at = db.Column(db.DateTime, nullable=True)
    opened_at = db.Column(db.DateTime, nullable=True)
    replied_at = db.Column(db.DateTime, nullable=True)
    
    # Unique constraint to prevent duplicate messages
    __table_args__ = (db.UniqueConstraint('campaign_id', 'business_id', 'contact_id', 'platform', name='unique_campaign_message'),)
    
    def __repr__(self):
        return f'<Message {self.id}: {self.platform} to {self.business.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'business_id': self.business_id,
            'contact_id': self.contact_id,
            'platform': self.platform,
            'personalized_content': self.personalized_content,
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None
        }

