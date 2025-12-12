# Factor VII: Port Binding

## Export services via port binding

### Implementation in Python Boyce

The application is self-contained and exports HTTP as a service via port binding:

- **Self-Contained**: Includes web server (no external web server required)
- **Port Binding**: Binds to a port and listens for requests
- **Service Export**: Can be used by other applications

### Key Implementation

```python
def main():
    """Main application entry point."""
    app = create_app()
    port = app.config['PORT']  # From environment variable
    
    # Bind to port and listen for requests
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
```

### Port Configuration

```bash
# Environment variable controls port
PORT=5000  # Development
PORT=8080  # Production
PORT=3000  # Alternative
```

### Production Deployment

```bash
# Using Gunicorn WSGI server
gunicorn --bind 0.0.0.0:$PORT app:create_app()

# Multiple workers
gunicorn --bind 0.0.0.0:$PORT --workers 4 app:create_app()
```

### Service Composition

This app can become a backing service for other apps:

```python
# Another app can use this as a service
PYTHON_BOYCE_URL = "http://python-boyce-app:5000"

response = requests.get(f"{PYTHON_BOYCE_URL}/api/data")
```

### Container Deployment

```dockerfile
# Dockerfile
EXPOSE $PORT
CMD gunicorn --bind 0.0.0.0:$PORT app:create_app()
```

### Best Practices

1. Never hardcode ports in the application
2. Use environment variables for port configuration
3. Bind to 0.0.0.0 to accept connections from any interface
4. Include a web server in the application
5. Make the app usable as a backing service

### Health Check Endpoint

```python
@app.route('/health')
def health_check():
    """Health check for load balancers."""
    return jsonify({'status': 'healthy'})
```

### Process Definition

```
# Procfile
web: gunicorn --bind 0.0.0.0:$PORT app:create_app()
```