# Factor IX: Disposability

## Maximize robustness with fast startup and graceful shutdown

### Implementation in Python Boyce

Processes are disposable - they can be started or stopped at any moment:

- **Fast Startup**: Application starts quickly
- **Graceful Shutdown**: Handles SIGTERM signals properly
- **Robust**: Survives unexpected termination

### Fast Startup Implementation

```python
def create_app():
    """Fast application factory - minimal startup time."""
    app = Flask(__name__)
    
    # Lazy loading of heavy resources
    # Minimal initialization
    # Quick configuration loading
    
    return app

def main():
    """Quick startup process."""
    logger.info("Starting Python Boyce application")
    app = create_app()
    
    # Fast startup - no heavy initialization
    app.run(host='0.0.0.0', port=app.config['PORT'])
```

### Graceful Shutdown

```python
import signal
import sys

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Received shutdown signal, cleaning up...")
    
    # Finish current requests
    # Close database connections
    # Save any pending work
    
    logger.info("Shutdown complete")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

### Worker Process Disposability

```python
# Celery worker graceful shutdown
from celery.signals import worker_shutdown

@worker_shutdown.connect
def worker_shutdown_handler(sender=None, **kwargs):
    """Handle worker shutdown gracefully."""
    logger.info("Worker shutting down gracefully")
    # Finish current tasks
    # Clean up resources
```

### Process Characteristics

**✅ Good Process Behavior**:
- Starts in < 5 seconds
- Responds to SIGTERM within 30 seconds
- Finishes current work before exiting
- Releases resources properly

**❌ Bad Process Behavior**:
- Long startup times
- Ignores shutdown signals
- Leaves work in inconsistent state
- Resource leaks

### Container Optimization

```dockerfile
# Dockerfile optimized for fast startup
FROM python:3.11-slim

# Pre-install dependencies for faster startup
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Fast startup command
CMD ["gunicorn", "--preload", "app:create_app()"]
```

### Best Practices

1. Minimize startup time
2. Handle SIGTERM gracefully
3. Finish current work before shutdown
4. Use health checks for readiness
5. Design for sudden termination
6. Avoid long-running initialization

### Health Checks

```python
@app.route('/health')
def health():
    """Quick health check for orchestrators."""
    return jsonify({'status': 'healthy'}), 200

@app.route('/ready')  
def ready():
    """Readiness check - app is ready to serve traffic."""
    # Check backing services
    return jsonify({'status': 'ready'}), 200
```