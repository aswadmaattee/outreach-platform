from src.tasks.celery_app import celery
from src.models.business import db, Business, Contact
import logging

logger = logging.getLogger(__name__)

@celery.task(bind=True)
def process_csv_task(self, csv_data):
    """Process CSV data and create business records"""
    try:
        processed_count = 0
        error_count = 0
        errors = []
        
        total_rows = len(csv_data)
        
        for i, row in enumerate(csv_data):
            try:
                # Update task progress
                self.update_state(
                    state='PROGRESS',
                    meta={
                        'current': i + 1,
                        'total': total_rows,
                        'processed': processed_count,
                        'errors': error_count
                    }
                )
                
                # Extract business data from CSV row
                business_name = row.get('Business Name', '').strip()
                if not business_name:
                    error_count += 1
                    errors.append(f"Row {i+1}: Missing business name")
                    continue
                
                # Check if business already exists
                existing_business = Business.query.filter_by(name=business_name).first()
                if existing_business:
                    logger.info(f"Business '{business_name}' already exists, skipping")
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
                
                logger.info(f"Created business '{business_name}' with {contacts_created} contacts")
                
            except Exception as e:
                db.session.rollback()
                error_count += 1
                error_msg = f"Row {i+1}: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
        
        # Final result
        result = {
            'total_rows': total_rows,
            'processed': processed_count,
            'errors': error_count,
            'error_details': errors[:10],  # Limit error details to first 10
            'status': 'completed'
        }
        
        logger.info(f"CSV processing completed: {processed_count} processed, {error_count} errors")
        return result
        
    except Exception as e:
        logger.error(f"CSV processing failed: {str(e)}")
        return {
            'status': 'failed',
            'error': str(e),
            'processed': processed_count,
            'errors': error_count
        }

@celery.task
def get_task_status(task_id):
    """Get the status of a task"""
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),
        }
    return response

