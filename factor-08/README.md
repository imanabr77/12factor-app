# Factor VIII: Concurrency

## Scale out via the process model

### Implementation in Python Boyce

Scaling is achieved through the process model, not threading:

- **Process Types**: Different types of processes for different workloads
- **Horizontal Scaling**: Add more processes to handle load
- **Process Manager**: Use system process manager (systemd, Docker, etc.)

### Process Types

```
# Procfile defines process types
web: gunicorn app:create_app()           # HTTP requests
worker: celery -A tasks worker           # Background jobs  
scheduler: celery -A tasks beat          # Periodic tasks
release: python manage.py migrate       # One-time tasks
```

### Scaling Strategy

**Web Processes** (CPU-bound):
```bash
# Scale web processes for HTTP traffic
heroku ps:scale web=4
```

**Worker Processes** (I/O-bound):
```bash
# Scale workers for background jobs
heroku ps:scale worker=2
```

### Concurrency Implementation

```python
# Gunicorn with multiple workers
gunicorn --workers 4 --worker-class gevent app:create_app()

# Celery with multiple worker processes
celery -A tasks worker --concurrency=4
```

### Process Architecture

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Web #1    │  │   Web #2    │  │   Web #3    │
│   Port 5000 │  │   Port 5001 │  │   Port 5002 │
└─────────────┘  └─────────────┘  └─────────────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
              ┌─────────────────┐
              │  Load Balancer  │
              └─────────────────┘
                         │
              ┌─────────────────┐
              │   Worker #1     │
              └─────────────────┘
              ┌─────────────────┐
              │   Worker #2     │
              └─────────────────┘
```

### Background Tasks

```python
# tasks.py - Celery tasks
from celery import Celery

celery = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL'))

@celery.task
def process_data(data):
    """CPU-intensive background task."""
    # Process data
    return result
```

### Best Practices

1. Use process model, not threading
2. Design for horizontal scaling
3. Separate process types by workload
4. Use a process manager in production
5. Monitor process health and restart failed processes

### Docker Scaling

```yaml
# docker-compose.yml
version: '3'
services:
  web:
    build: .
    command: gunicorn app:create_app()
    scale: 3
  
  worker:
    build: .
    command: celery -A tasks worker
    scale: 2
```