# Factor XI: Logs

## Treat logs as event streams

### Implementation in Python Boyce

Logs are treated as time-ordered event streams written to stdout:

- **Event Streams**: Logs are continuous streams of events
- **Stdout**: Write all logs to stdout, never to files
- **No Routing**: App doesn't manage log routing or storage

### Logging Implementation

```python
import logging
import sys

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # Always stdout, never files
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Python Boyce application")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    app = create_app()
    app.run(host='0.0.0.0', port=app.config['PORT'])
```

### Structured Logging

```python
import json
from datetime import datetime

def log_event(event_type, **kwargs):
    """Log structured events as JSON."""
    event = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'level': 'INFO',
        **kwargs
    }
    print(json.dumps(event))

# Usage
log_event('user_login', user_id=123, ip_address='192.168.1.1')
log_event('api_request', method='GET', path='/api/users', duration_ms=45)
```

### Request Logging

```python
from flask import request
import time

@app.before_request
def log_request():
    """Log incoming requests."""
    request.start_time = time.time()
    logger.info(f"Request started: {request.method} {request.path}")

@app.after_request  
def log_response(response):
    """Log request completion."""
    duration = time.time() - request.start_time
    logger.info(f"Request completed: {request.method} {request.path} "
               f"Status: {response.status_code} Duration: {duration:.3f}s")
    return response
```

### Log Aggregation (External)

The application doesn't handle log routing - that's done by the execution environment:

**Development**:
```bash
# View logs directly
python app.py

# Or with Docker
docker logs container_name
```

**Production**:
```bash
# Kubernetes
kubectl logs deployment/myapp

# Docker Swarm  
docker service logs myapp

# Systemd
journalctl -u myapp -f
```

### Log Levels

```python
# Different log levels for different events
logger.debug("Detailed debugging information")
logger.info("General application flow")
logger.warning("Something unexpected happened")
logger.error("Error occurred but app continues")
logger.critical("Serious error, app may not continue")
```

### Best Practices

1. Always log to stdout/stderr
2. Never write log files directly
3. Use structured logging (JSON) for machine parsing
4. Include correlation IDs for request tracing
5. Log at appropriate levels
6. Don't log sensitive information

### Log Routing Examples

**Heroku**:
```bash
heroku logs --tail --app myapp
```

**AWS CloudWatch**:
```bash
aws logs tail /aws/lambda/myapp --follow
```

**ELK Stack**:
- Filebeat collects from stdout
- Logstash processes and routes
- Elasticsearch stores and indexes
- Kibana provides visualization