# Factor IV: Backing Services

## Treat backing services as attached resources

### Implementation in Python Boyce

Backing services are accessed via URLs and can be swapped without code changes:

- **Database**: PostgreSQL via `DATABASE_URL`
- **Cache**: Redis via `REDIS_URL`  
- **Message Queue**: Redis/RabbitMQ via `CELERY_BROKER_URL`

### Backing Services Used

1. **PostgreSQL Database**
   - Connection: `DATABASE_URL` environment variable
   - Easily swappable between local/staging/production

2. **Redis Cache & Message Broker**
   - Connection: `REDIS_URL` environment variable
   - Used for caching and Celery task queue

### Key Implementation

```python
# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')

# Redis connection  
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# Message broker for Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
```

### Service Swapping Examples

**Development**:
```bash
DATABASE_URL=sqlite:///dev.db
REDIS_URL=redis://localhost:6379
```

**Production**:
```bash
DATABASE_URL=postgresql://user:pass@prod-db:5432/myapp
REDIS_URL=redis://prod-redis:6379
```

### Best Practices

1. Access services only via URLs from config
2. No distinction between local and third-party services
3. Services should be swappable without code changes
4. Use connection pooling for performance
5. Implement graceful degradation when services are unavailable

### Service Health Checks

```python
def check_backing_services():
    """Verify all backing services are accessible."""
    # Database check
    # Redis check  
    # External API checks
    pass
```