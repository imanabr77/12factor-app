# Factor VI: Processes

## Execute the app as one or more stateless processes

### Implementation in Python Boyce

The application runs as stateless processes that share nothing:

- **Stateless**: No local state stored in memory or filesystem
- **Share-Nothing**: Each process is independent
- **Sticky Sessions**: Not used - any process can handle any request

### Process Architecture

```python
def create_app():
    """Application factory - creates stateless app instances."""
    app = Flask(__name__)
    
    # No global state
    # No session affinity required
    # All state in backing services (database, cache)
    
    return app
```

### State Management

**❌ Bad - Stateful**:
```python
# Don't do this - stores state in process memory
user_sessions = {}
cached_data = {}
```

**✅ Good - Stateless**:
```python
# Store state in backing services
import redis
cache = redis.from_url(os.getenv('REDIS_URL'))

def get_user_session(session_id):
    return cache.get(f"session:{session_id}")
```

### Process Types

1. **Web Processes**: Handle HTTP requests
2. **Worker Processes**: Handle background jobs
3. **Scheduler Processes**: Trigger periodic tasks

### Scaling

Horizontal scaling by adding more processes:

```bash
# Scale web processes
heroku ps:scale web=3

# Scale worker processes  
heroku ps:scale worker=2
```

### Best Practices

1. Store all persistent state in backing services
2. Use session stores (Redis, database) not memory
3. Design for horizontal scaling
4. Avoid filesystem storage for persistent data
5. Make processes disposable and fast to start

### Session Management

```python
from flask_session import Session
import redis

# Configure session to use Redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.getenv('REDIS_URL'))
Session(app)
```