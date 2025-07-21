from flask import Blueprint, request, jsonify
from src.models.business import db, Business
from src.tasks.scanner import scan_business_sync, scan_all_pending_sync

scanner_bp = Blueprint('scanner', __name__)

@scanner_bp.route('/scan/business/<int:business_id>', methods=['POST'])
def scan_business(business_id):
    """Trigger scan for a specific business"""
    try:
        business = Business.query.get_or_404(business_id)
        
        # Perform scan
        success = scan_business_sync(business_id)
        
        if success:
            return jsonify({
                'message': f'Successfully scanned business: {business.name}',
                'business_id': business_id
            }), 200
        else:
            return jsonify({
                'error': f'Failed to scan business: {business.name}',
                'business_id': business_id
            }), 500
            
    except Exception as e:
        return jsonify({'error': f'Error scanning business: {str(e)}'}), 500

@scanner_bp.route('/scan/all-pending', methods=['POST'])
def scan_all_pending():
    """Trigger scan for all businesses with pending_scan status"""
    try:
        # Get count of pending businesses
        pending_count = Business.query.filter_by(status='pending_scan').count()
        
        if pending_count == 0:
            return jsonify({
                'message': 'No businesses with pending_scan status found',
                'scanned_count': 0,
                'total_pending': 0
            }), 200
        
        # Perform scan
        scanned_count = scan_all_pending_sync()
        
        return jsonify({
            'message': f'Scan completed. Scanned {scanned_count} out of {pending_count} businesses.',
            'scanned_count': scanned_count,
            'total_pending': pending_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error scanning businesses: {str(e)}'}), 500

@scanner_bp.route('/scan/status', methods=['GET'])
def get_scan_status():
    """Get scanning status and statistics"""
    try:
        total_businesses = Business.query.count()
        pending_scan = Business.query.filter_by(status='pending_scan').count()
        scanned = Business.query.filter_by(status='scanned').count()
        active = Business.query.filter_by(status='active').count()
        
        return jsonify({
            'total_businesses': total_businesses,
            'pending_scan': pending_scan,
            'scanned': scanned,
            'active': active,
            'scan_completion_rate': round((scanned + active) / total_businesses * 100, 2) if total_businesses > 0 else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error getting scan status: {str(e)}'}), 500

