from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import csv
import io
import os
from src.models.business import db, Business, Contact

business_bp = Blueprint('business', __name__)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_csv_sync(csv_data):
    """Process CSV data synchronously"""
    processed_count = 0
    error_count = 0
    errors = []
    
    for i, row in enumerate(csv_data):
        try:
            # Extract business data from CSV row
            business_name = row.get('Business Name', '').strip()
            if not business_name:
                error_count += 1
                errors.append(f"Row {i+1}: Missing business name")
                continue
            
            # Check if business already exists
            existing_business = Business.query.filter_by(name=business_name).first()
            if existing_business:
                continue
            
            # Create new business
            business = Business(
                name=business_name,
                website=row.get('Website', '').strip() or None,
                email=row.get('Email', '').strip() or None,
                phone_number=row.get('Phone Number', '').strip() or None,
                address=row.get('Address', '').strip() or None,
                status='pending_scan'
            )
            
            db.session.add(business)
            db.session.flush()  # Get the business ID
            
            # Create contacts from CSV data
            contacts_created = 0
            
            # Add email contact if provided
            if business.email:
                email_contact = Contact(
                    business_id=business.id,
                    type='email',
                    value=business.email,
                    source='csv',
                    is_primary=True
                )
                db.session.add(email_contact)
                contacts_created += 1
            
            # Add phone contact if provided
            if business.phone_number:
                phone_contact = Contact(
                    business_id=business.id,
                    type='phone',
                    value=business.phone_number,
                    source='csv',
                    is_primary=True
                )
                db.session.add(phone_contact)
                contacts_created += 1
            
            db.session.commit()
            processed_count += 1
            
        except Exception as e:
            db.session.rollback()
            error_count += 1
            error_msg = f"Row {i+1}: {str(e)}"
            errors.append(error_msg)
    
    return {
        'total_rows': len(csv_data),
        'processed': processed_count,
        'errors': error_count,
        'error_details': errors[:10],  # Limit error details to first 10
        'status': 'completed'
    }

@business_bp.route('/businesses/upload', methods=['POST'])
def upload_csv():
    """Upload and process CSV file containing business data"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400
    
    try:
        # Read CSV content
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        # Validate CSV headers
        required_headers = ['Business Name']
        optional_headers = ['Website', 'Email', 'Phone Number', 'Address']
        
        if not all(header in csv_input.fieldnames for header in required_headers):
            return jsonify({'error': f'CSV must contain required headers: {required_headers}'}), 400
        
        # Convert CSV to list for processing
        csv_data = []
        for row in csv_input:
            csv_data.append(row)
        
        if not csv_data:
            return jsonify({'error': 'CSV file is empty'}), 400
        
        # Process CSV synchronously
        result = process_csv_sync(csv_data)
        
        return jsonify({
            'message': 'CSV processing completed.',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error processing CSV: {str(e)}'}), 500

@business_bp.route('/businesses', methods=['GET'])
def get_businesses():
    """Retrieve list of businesses with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    search = request.args.get('search')
    
    # Build query
    query = Business.query
    
    if status:
        query = query.filter(Business.status == status)
    
    if search:
        query = query.filter(
            db.or_(
                Business.name.ilike(f'%{search}%'),
                Business.address.ilike(f'%{search}%')
            )
        )
    
    # Paginate results
    businesses = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'businesses': [business.to_dict() for business in businesses.items],
        'total_pages': businesses.pages,
        'current_page': businesses.page,
        'total_items': businesses.total,
        'has_next': businesses.has_next,
        'has_prev': businesses.has_prev
    })

@business_bp.route('/businesses/<int:business_id>', methods=['GET'])
def get_business(business_id):
    """Retrieve details for a single business"""
    business = Business.query.get_or_404(business_id)
    return jsonify(business.to_dict())

@business_bp.route('/businesses/<int:business_id>', methods=['PUT'])
def update_business(business_id):
    """Update details for a single business"""
    business = Business.query.get_or_404(business_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update allowed fields
    allowed_fields = ['name', 'website', 'email', 'phone_number', 'address', 'status']
    for field in allowed_fields:
        if field in data:
            setattr(business, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Business updated successfully.',
            'business': business.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating business: {str(e)}'}), 500

@business_bp.route('/businesses/<int:business_id>', methods=['DELETE'])
def delete_business(business_id):
    """Delete a business"""
    business = Business.query.get_or_404(business_id)
    
    try:
        db.session.delete(business)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting business: {str(e)}'}), 500

@business_bp.route('/businesses/<int:business_id>/contacts', methods=['POST'])
def add_contact(business_id):
    """Add a new contact to a business"""
    business = Business.query.get_or_404(business_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['type', 'value', 'source']
    if not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
    # Validate contact type
    valid_types = ['email', 'instagram', 'facebook', 'twitter', 'linkedin', 'phone', 'contact_form']
    if data['type'] not in valid_types:
        return jsonify({'error': f'Invalid contact type. Must be one of: {valid_types}'}), 400
    
    # Validate source
    valid_sources = ['csv', 'scanned_website', 'scanned_social_media', 'manual']
    if data['source'] not in valid_sources:
        return jsonify({'error': f'Invalid source. Must be one of: {valid_sources}'}), 400
    
    try:
        contact = Contact(
            business_id=business_id,
            type=data['type'],
            value=data['value'],
            source=data['source'],
            is_primary=data.get('is_primary', False)
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'message': 'Contact added successfully.',
            'contact': contact.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error adding contact: {str(e)}'}), 500

@business_bp.route('/businesses/<int:business_id>/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(business_id, contact_id):
    """Delete a contact from a business"""
    contact = Contact.query.filter_by(id=contact_id, business_id=business_id).first_or_404()
    
    try:
        db.session.delete(contact)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting contact: {str(e)}'}), 500

