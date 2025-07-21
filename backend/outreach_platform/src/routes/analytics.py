from flask import Blueprint, request, jsonify, make_response
from src.models.business import db, Business, Contact, Campaign, Message
from datetime import datetime, timedelta
import csv
import io

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/export', methods=['GET'])
def export_analytics():
    """Export analytics data as CSV"""
    try:
        # Get query parameters
        format_type = request.args.get('format', 'csv')
        date_range = request.args.get('date_range', '30')  # days
        
        # Calculate date filter
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=int(date_range))
        
        # Get campaigns data
        campaigns = Campaign.query.filter(
            Campaign.created_at >= start_date
        ).all()
        
        if format_type == 'csv':
            # Create CSV data
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow([
                'Campaign Name',
                'Status',
                'Created Date',
                'Total Messages',
                'Sent Messages',
                'Failed Messages',
                'Opened Messages',
                'Replied Messages',
                'Success Rate (%)'
            ])
            
            # Write campaign data
            for campaign in campaigns:
                # Get message statistics
                total_messages = Message.query.filter_by(campaign_id=campaign.id).count()
                sent_messages = Message.query.filter_by(campaign_id=campaign.id, status='sent').count()
                failed_messages = Message.query.filter_by(campaign_id=campaign.id, status='failed').count()
                opened_messages = Message.query.filter_by(campaign_id=campaign.id, status='opened').count()
                replied_messages = Message.query.filter_by(campaign_id=campaign.id, status='replied').count()
                
                success_rate = round((sent_messages / total_messages * 100), 2) if total_messages > 0 else 0
                
                writer.writerow([
                    campaign.name,
                    campaign.status,
                    campaign.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    total_messages,
                    sent_messages,
                    failed_messages,
                    opened_messages,
                    replied_messages,
                    success_rate
                ])
            
            # Create response
            output.seek(0)
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=analytics_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
            return response
        
        else:
            return jsonify({'error': 'Unsupported format'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@analytics_bp.route('/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary data"""
    try:
        # Get query parameters
        date_range = request.args.get('date_range', '30')  # days
        
        # Calculate date filter
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=int(date_range))
        
        # Get basic counts
        total_businesses = Business.query.count()
        total_campaigns = Campaign.query.filter(
            Campaign.created_at >= start_date
        ).count()
        
        # Get message statistics
        messages_query = Message.query.join(Campaign).filter(
            Campaign.created_at >= start_date
        )
        
        total_messages = messages_query.count()
        sent_messages = messages_query.filter(Message.status == 'sent').count()
        failed_messages = messages_query.filter(Message.status == 'failed').count()
        opened_messages = messages_query.filter(Message.status == 'opened').count()
        replied_messages = messages_query.filter(Message.status == 'replied').count()
        
        # Calculate rates
        success_rate = round((sent_messages / total_messages * 100), 2) if total_messages > 0 else 0
        open_rate = round((opened_messages / sent_messages * 100), 2) if sent_messages > 0 else 0
        reply_rate = round((replied_messages / sent_messages * 100), 2) if sent_messages > 0 else 0
        
        # Get campaign performance data
        campaigns = Campaign.query.filter(
            Campaign.created_at >= start_date
        ).all()
        
        campaign_performance = []
        for campaign in campaigns:
            campaign_messages = Message.query.filter_by(campaign_id=campaign.id)
            campaign_total = campaign_messages.count()
            campaign_sent = campaign_messages.filter_by(status='sent').count()
            campaign_opened = campaign_messages.filter_by(status='opened').count()
            campaign_replied = campaign_messages.filter_by(status='replied').count()
            
            campaign_performance.append({
                'name': campaign.name,
                'total': campaign_total,
                'sent': campaign_sent,
                'opened': campaign_opened,
                'replied': campaign_replied,
                'success_rate': round((campaign_sent / campaign_total * 100), 2) if campaign_total > 0 else 0
            })
        
        # Get daily performance data (last 7 days)
        daily_performance = []
        for i in range(7):
            day_start = end_date - timedelta(days=i+1)
            day_end = end_date - timedelta(days=i)
            
            day_messages = Message.query.join(Campaign).filter(
                Message.sent_at >= day_start,
                Message.sent_at < day_end
            ).count()
            
            daily_performance.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'messages': day_messages
            })
        
        daily_performance.reverse()  # Show oldest to newest
        
        return jsonify({
            'summary': {
                'total_businesses': total_businesses,
                'total_campaigns': total_campaigns,
                'total_messages': total_messages,
                'sent_messages': sent_messages,
                'failed_messages': failed_messages,
                'opened_messages': opened_messages,
                'replied_messages': replied_messages,
                'success_rate': success_rate,
                'open_rate': open_rate,
                'reply_rate': reply_rate
            },
            'campaign_performance': campaign_performance,
            'daily_performance': daily_performance,
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': int(date_range)
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get analytics summary: {str(e)}'}), 500

@analytics_bp.route('/analytics/business-stats', methods=['GET'])
def get_business_stats():
    """Get business-related statistics"""
    try:
        # Business status distribution
        total_businesses = Business.query.count()
        pending_scan = Business.query.filter_by(status='pending_scan').count()
        scanned = Business.query.filter_by(status='scanned').count()
        active = Business.query.filter_by(status='active').count()
        
        # Contact type distribution
        contact_types = db.session.query(
            Contact.type,
            db.func.count(Contact.id).label('count')
        ).group_by(Contact.type).all()
        
        contact_distribution = [
            {'type': contact_type, 'count': count}
            for contact_type, count in contact_types
        ]
        
        # Businesses with contacts
        businesses_with_contacts = db.session.query(Business.id).join(Contact).distinct().count()
        businesses_without_contacts = total_businesses - businesses_with_contacts
        
        return jsonify({
            'business_status': {
                'total': total_businesses,
                'pending_scan': pending_scan,
                'scanned': scanned,
                'active': active
            },
            'contact_distribution': contact_distribution,
            'contact_coverage': {
                'with_contacts': businesses_with_contacts,
                'without_contacts': businesses_without_contacts,
                'coverage_rate': round((businesses_with_contacts / total_businesses * 100), 2) if total_businesses > 0 else 0
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get business stats: {str(e)}'}), 500

