# Factor III: Config

## Store config in the environment

### Implementation in Python Boyce

Configuration is stored in environment variables, never in code:

- **Environment Variables**: All config comes from env vars
- **No Hardcoded Values**: No secrets or config in source code
- **Environment Specific**: Different values per deployment

### Configuration Variables

```python
# Database configuration
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Application settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
APP_VERSION=1.2.3
PORT=5000

# External services
REDIS_URL=redis://localhost:6379
CELERY_BROKER_URL=redis://localhost:6379
```

### Key Implementation

```python
# In app.py
app.config.update({
    'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
    'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-key-change-in-production'),
    'DATABASE_URL': os.getenv('DATABASE_URL', 'sqlite:///app.db'),
    'REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379'),
    'PORT': int(os.getenv('PORT', 5000)),
})
```

### Best Practices

1. Never commit secrets to version control
2. Use different config for each environment
3. Provide sensible defaults for development
4. Validate required configuration on startup
5. Use `.env` files for local development (not committed)

### Environment Files

Create `.env` for local development:
```bash
DEBUG=True
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///dev.db
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
```