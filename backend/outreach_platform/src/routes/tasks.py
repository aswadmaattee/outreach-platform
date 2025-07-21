from flask import Blueprint, jsonify
from src.tasks.celery_app import celery

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/<task_id>/status', methods=['GET'])
def get_task_status(task_id):
    """Get the status of a Celery task"""
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
            'status': task.info.get('status', ''),
            'processed': task.info.get('processed', 0),
            'errors': task.info.get('errors', 0)
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # Task failed
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),
            'error': str(task.info)
        }
    
    return jsonify(response)

