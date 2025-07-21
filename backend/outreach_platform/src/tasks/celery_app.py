from celery import Celery
import os

def make_celery(app=None):
    """Create Celery instance"""
    celery = Celery(
        'outreach_platform',
        broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        include=['src.tasks.csv_processor', 'src.tasks.scanner', 'src.tasks.outreach']
    )
    
    # Update configuration
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_routes={
            'src.tasks.csv_processor.*': {'queue': 'csv_processing'},
            'src.tasks.scanner.*': {'queue': 'scanning'},
            'src.tasks.outreach.*': {'queue': 'outreach'},
        }
    )
    
    if app:
        # Update task base classes to be aware of Flask app context
        class ContextTask(celery.Task):
            """Make celery tasks work with Flask app context."""
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        
        celery.Task = ContextTask
    
    return celery

# Create celery instance
celery = make_celery()

