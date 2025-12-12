"""
Background tasks for Python Boyce application.
Implements Factor VIII - Concurrency through worker processes.
"""

import os
import time
import logging
from celery import Celery

# Configure Celery
celery = Celery(
    'tasks',
    broker=os.getenv('CELERY_BROKER_URL', os.getenv('REDIS_URL', 'redis://localhost:6379')),
    backend=os.getenv('CELERY_RESULT_BACKEND', os.getenv('REDIS_URL', 'redis://localhost:6379'))
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task
def process_data(data):
    """Process data in background."""
    logger.info(f"Processing data: {data}")
    
    # Simulate processing time
    time.sleep(2)
    
    result = {
        'processed_at': time.time(),
        'input_data': data,
        'status': 'completed'
    }
    
    logger.info(f"Data processing completed: {result}")
    return result

@celery.task
def send_email(to_email, subject, body):
    """Send email in background."""
    logger.info(f"Sending email to {to_email}")
    
    # Simulate email sending
    time.sleep(1)
    
    logger.info(f"Email sent successfully to {to_email}")
    return {'status': 'sent', 'to': to_email}

@celery.task
def generate_report_task(report_type):
    """Generate report in background."""
    logger.info(f"Generating {report_type} report")
    
    # Simulate report generation
    time.sleep(5)
    
    report_data = {
        'type': report_type,
        'generated_at': time.time(),
        'status': 'completed'
    }
    
    logger.info(f"Report generation completed: {report_data}")
    return report_data

@celery.task
def cleanup_task():
    """Periodic cleanup task."""
    logger.info("Running cleanup task")
    
    # Simulate cleanup operations
    time.sleep(3)
    
    logger.info("Cleanup task completed")
    return {'status': 'cleaned', 'items_removed': 42}

# Periodic tasks configuration
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'daily-cleanup': {
        'task': 'tasks.cleanup_task',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
    'weekly-report': {
        'task': 'tasks.generate_report_task',
        'schedule': crontab(hour=1, minute=0, day_of_week=1),  # Weekly on Monday
        'args': ('weekly',)
    },
}

celery.conf.timezone = 'UTC'