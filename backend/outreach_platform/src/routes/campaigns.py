from flask import Blueprint, request, jsonify
from src.models.business import db, Business, Contact, Campaign, Message
from src.tasks.outreach import send_campaign_messages_sync, generate_personalized_message
from datetime import datetime

campaigns_bp = Blueprint('campaigns', __name__)

@campaigns_bp.route('/campaigns', methods=['POST'])
def create_campaign():
    """Create a new outreach campaign"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'message_template']
    if not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
    try:
        # Check if campaign name already exists
        existing_campaign = Campaign.query.filter_by(name=data['name']).first()
        if existing_campaign:
            return jsonify({'error': 'Campaign name already exists'}), 400
        
        campaign = Campaign(
            name=data['name'],
            message_template=data['message_template'],
            status='draft'
        )
        
        db.session.add(campaign)
        db.session.commit()
        
        return jsonify({
            'message': 'Campaign created successfully.',
            'campaign': campaign.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error creating campaign: {str(e)}'}), 500

@campaigns_bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    """Retrieve list of campaigns with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    
    # Build query
    query = Campaign.query
    
    if status:
        query = query.filter(Campaign.status == status)
    
    # Paginate results
    campaigns = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    # Add message statistics for each campaign
    campaign_list = []
    for campaign in campaigns.items:
        campaign_dict = campaign.to_dict()
        
        # Get message statistics
        total_messages = Message.query.filter_by(campaign_id=campaign.id).count()
        sent_messages = Message.query.filter_by(campaign_id=campaign.id, status='sent').count()
        failed_messages = Message.query.filter_by(campaign_id=campaign.id, status='failed').count()
        opened_messages = Message.query.filter_by(campaign_id=campaign.id, status='opened').count()
        replied_messages = Message.query.filter_by(campaign_id=campaign.id, status='replied').count()
        
        campaign_dict['messages_summary'] = {
            'total': total_messages,
            'sent': sent_messages,
            'failed': failed_messages,
            'opened': opened_messages,
            'replied': replied_messages
        }
        
        campaign_list.append(campaign_dict)
    
    return jsonify({
        'campaigns': campaign_list,
        'total_pages': campaigns.pages,
        'current_page': campaigns.page,
        'total_items': campaigns.total,
        'has_next': campaigns.has_next,
        'has_prev': campaigns.has_prev
    })

@campaigns_bp.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Retrieve details for a single campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    campaign_dict = campaign.to_dict()
    
    # Get detailed message information
    messages = Message.query.filter_by(campaign_id=campaign_id).all()
    campaign_dict['messages'] = [message.to_dict() for message in messages]
    
    # Get message statistics
    total_messages = len(messages)
    sent_messages = sum(1 for m in messages if m.status == 'sent')
    failed_messages = sum(1 for m in messages if m.status == 'failed')
    opened_messages = sum(1 for m in messages if m.status == 'opened')
    replied_messages = sum(1 for m in messages if m.status == 'replied')
    
    campaign_dict['messages_summary'] = {
        'total': total_messages,
        'sent': sent_messages,
        'failed': failed_messages,
        'opened': opened_messages,
        'replied': replied_messages
    }
    
    return jsonify(campaign_dict)

@campaigns_bp.route('/campaigns/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    """Update campaign details"""
    campaign = Campaign.query.get_or_404(campaign_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Update allowed fields
        allowed_fields = ['name', 'message_template', 'status']
        for field in allowed_fields:
            if field in data:
                setattr(campaign, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Campaign updated successfully.',
            'campaign': campaign.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating campaign: {str(e)}'}), 500

@campaigns_bp.route('/campaigns/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """Delete a campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    try:
        db.session.delete(campaign)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting campaign: {str(e)}'}), 500

@campaigns_bp.route('/campaigns/<int:campaign_id>/send', methods=['POST'])
def send_campaign(campaign_id):
    """Send messages for a campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    data = request.get_json() or {}
    
    # Get optional parameters
    business_ids = data.get('business_ids')  # If specified, only send to these businesses
    platforms = data.get('platforms', ['email'])  # Default to email only
    
    try:
        # Update campaign status
        campaign.status = 'sending'
        db.session.commit()
        
        # Send messages
        result = send_campaign_messages_sync(campaign_id, business_ids, platforms)
        
        # Update campaign status based on result
        if result['success']:
            campaign.status = 'completed' if result['sent_count'] > 0 else 'draft'
        else:
            campaign.status = 'draft'
        
        db.session.commit()
        
        return jsonify({
            'message': f'Campaign sending completed. Sent {result["sent_count"]} messages.',
            'result': result
        }), 200
        
    except Exception as e:
        # Reset campaign status on error
        campaign.status = 'draft'
        db.session.commit()
        return jsonify({'error': f'Error sending campaign: {str(e)}'}), 500

@campaigns_bp.route('/campaigns/<int:campaign_id>/pause', methods=['POST'])
def pause_campaign(campaign_id):
    """Pause an active campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if campaign.status != 'sending':
        return jsonify({'error': 'Campaign is not currently sending'}), 400
    
    try:
        campaign.status = 'paused'
        db.session.commit()
        
        return jsonify({'message': 'Campaign paused.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error pausing campaign: {str(e)}'}), 500

@campaigns_bp.route('/campaigns/<int:campaign_id>/resume', methods=['POST'])
def resume_campaign(campaign_id):
    """Resume a paused campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if campaign.status != 'paused':
        return jsonify({'error': 'Campaign is not currently paused'}), 400
    
    try:
        campaign.status = 'sending'
        db.session.commit()
        
        return jsonify({'message': 'Campaign resumed.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error resuming campaign: {str(e)}'}), 500

@campaigns_bp.route('/campaigns/<int:campaign_id>/preview', methods=['POST'])
def preview_campaign_messages(campaign_id):
    """Preview personalized messages for a campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    data = request.get_json() or {}
    
    # Get optional parameters
    business_ids = data.get('business_ids')
    platforms = data.get('platforms', ['email'])
    limit = data.get('limit', 5)  # Limit preview to 5 messages
    
    try:
        # Get businesses to preview
        query = Business.query
        if business_ids:
            query = query.filter(Business.id.in_(business_ids))
        
        businesses = query.limit(limit).all()
        
        previews = []
        for business in businesses:
            for platform in platforms:
                # Find contact for this platform
                contact = Contact.query.filter_by(
                    business_id=business.id,
                    type=platform
                ).first()
                
                if contact:
                    personalized_message = generate_personalized_message(
                        campaign.message_template,
                        business,
                        contact
                    )
                    
                    previews.append({
                        'business_name': business.name,
                        'platform': platform,
                        'contact_value': contact.value,
                        'personalized_message': personalized_message
                    })
        
        return jsonify({
            'campaign_name': campaign.name,
            'previews': previews
        })
        
    except Exception as e:
        return jsonify({'error': f'Error generating preview: {str(e)}'}), 500

