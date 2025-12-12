# Factor II: Dependencies

## Explicitly declare and isolate dependencies

### Implementation in Python Boyce

This application properly manages dependencies through:

- **Explicit Declaration**: All dependencies listed in `requirements.txt`
- **Isolation**: Uses virtual environments to avoid system-wide pollution
- **No System Dependencies**: Doesn't rely on implicit system packages

### Key Files

- `requirements.txt` - Explicit dependency declarations
- `Pipfile` or `pyproject.toml` - Alternative dependency management
- Virtual environment isolation

### Dependencies Used

```
Flask==2.3.3          # Web framework
gunicorn==21.2.0       # WSGI server
redis==5.0.1           # Caching and message broker
psycopg2-binary==2.9.7 # PostgreSQL adapter
python-dotenv==1.0.0   # Environment variable loading
celery==5.3.4          # Background task processing
```

### Best Practices

1. Pin exact versions in production
2. Use virtual environments
3. Never rely on system packages
4. Document all dependencies
5. Regularly update dependencies

### Setup Commands

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Freeze current environment
pip freeze > requirements.txt
```