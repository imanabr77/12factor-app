# Python Boyce - 12-Factor App Implementation

A comprehensive Python application demonstrating all 12 factors of modern application development as defined by [The Twelve-Factor App](https://12factor.net/).

## Overview

Python Boyce is a Flask-based web application that serves as a practical implementation and learning resource for the 12-factor methodology. Each factor is implemented with best practices and documented with examples.

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone and start the application
git clone <repository-url>
cd python-boyce

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Access the application
curl http://localhost:5000
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=sqlite:///dev.db
export REDIS_URL=redis://localhost:6379
export DEBUG=True
export ENVIRONMENT=development

# Run the application
python app.py
```

## The 12 Factors Implementation

Each factor is implemented in the application and documented in its own folder:

### [Factor I: Codebase](factor-01/README.md)
- Single Git repository
- Multiple deployments from same codebase
- Version tracking with Git tags

### [Factor II: Dependencies](factor-02/README.md)
- Explicit dependency declaration in `requirements.txt`
- Virtual environment isolation
- No system-wide package dependencies

### [Factor III: Config](factor-03/README.md)
- All configuration via environment variables
- No hardcoded secrets or config
- Environment-specific settings

### [Factor IV: Backing Services](factor-04/README.md)
- PostgreSQL database via `DATABASE_URL`
- Redis cache/message broker via `REDIS_URL`
- Swappable service connections

### [Factor V: Build, Release, Run](factor-05/README.md)
- Separate build, release, and run stages
- Immutable releases with unique identifiers
- Automated deployment pipeline

### [Factor VI: Processes](factor-06/README.md)
- Stateless application processes
- No local state storage
- Horizontal scaling capability

### [Factor VII: Port Binding](factor-07/README.md)
- Self-contained web server
- Port configuration via environment
- Service export capability

### [Factor VIII: Concurrency](factor-08/README.md)
- Process-based scaling model
- Multiple process types (web, worker, scheduler)
- Horizontal scaling via process manager

### [Factor IX: Disposability](factor-09/README.md)
- Fast startup and graceful shutdown
- Signal handling for clean termination
- Robust process lifecycle management

### [Factor X: Dev/Prod Parity](factor-10/README.md)
- Identical backing services across environments
- Docker for environment consistency
- Automated deployment processes

### [Factor XI: Logs](factor-11/README.md)
- Logs as event streams to stdout
- Structured logging with JSON
- No log file management in application

### [Factor XII: Admin Processes](factor-12/README.md)
- One-off administrative tasks
- Same environment as regular processes
- Database migrations and maintenance scripts

## Application Structure

```
python-boyce/
├── app.py                 # Main application
├── tasks.py              # Background tasks (Celery)
├── manage.py             # Administrative tasks
├── requirements.txt      # Dependencies
├── Procfile             # Process definitions
├── Dockerfile           # Container definition
├── docker-compose.yml   # Local development setup
├── factor-01/           # Factor I documentation
├── factor-02/           # Factor II documentation
├── ...                  # Factors III-XII documentation
└── README.md           # This file
```

## API Endpoints

- `GET /` - Health check and application info
- `GET /config` - Show non-sensitive configuration
- `GET /logs` - Generate sample log entries
- `GET /health` - Health check for load balancers

## Process Types

The application defines multiple process types in the `Procfile`:

- **web**: HTTP server handling requests
- **worker**: Background task processor
- **scheduler**: Periodic task scheduler
- **release**: One-off deployment tasks

## Environment Variables

### Required
- `DATABASE_URL` - Database connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - Application secret key

### Optional
- `DEBUG` - Enable debug mode (default: False)
- `PORT` - Port to bind to (default: 5000)
- `ENVIRONMENT` - Environment name (default: development)
- `APP_VERSION` - Application version (default: 1.0.0)

## Deployment

### Heroku
```bash
# Create app
heroku create python-boyce

# Add addons
heroku addons:create heroku-postgresql:mini
heroku addons:create heroku-redis:mini

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

### Kubernetes
```bash
# Build and push image
docker build -t myregistry/python-boyce:v1.0.0 .
docker push myregistry/python-boyce:v1.0.0

# Deploy
kubectl apply -f k8s/
```

### Docker
```bash
# Build image
docker build -t python-boyce .

# Run with environment variables
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  python-boyce
```

## Administrative Tasks

Run administrative tasks using the management script:

```bash
# Database migrations
python manage.py migrate

# Seed initial data
python manage.py seed

# Generate reports
python manage.py report

# Show application status
python manage.py status

# Clean up old logs
python manage.py cleanup
```

## Background Tasks

The application uses Celery for background task processing:

```bash
# Start worker process
celery -A tasks worker --loglevel=info

# Start scheduler for periodic tasks
celery -A tasks beat --loglevel=info

# Monitor tasks
celery -A tasks flower
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Quality
```bash
# Linting
flake8 app.py tasks.py manage.py

# Type checking
mypy app.py

# Security scanning
bandit -r .
```

### Local Development with Docker
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Run commands in container
docker-compose exec web python manage.py status

# Stop environment
docker-compose down
```

## Monitoring and Observability

### Health Checks
- `GET /health` - Application health status
- `GET /ready` - Readiness probe for orchestrators

### Logging
- All logs output to stdout in JSON format
- Request/response logging with timing
- Structured event logging for monitoring

### Metrics
- Application metrics via Prometheus (when configured)
- Custom business metrics tracking
- Performance monitoring integration

## Security Considerations

- No hardcoded secrets or credentials
- Environment-based configuration
- Non-root container execution
- Input validation and sanitization
- Security headers in HTTP responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes following 12-factor principles
4. Add tests and documentation
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Resources

- [The Twelve-Factor App](https://12factor.net/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
