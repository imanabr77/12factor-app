# Factor V: Build, Release, Run

## Strictly separate build and run stages

### Implementation in Python Boyce

Clear separation between build, release, and run stages:

### Build Stage
Converts code into an executable bundle:

```bash
# Install dependencies
pip install -r requirements.txt

# Compile assets (if any)
# Run tests
python -m pytest

# Create deployment package
tar -czf app-v1.2.3.tar.gz app.py requirements.txt Procfile
```

### Release Stage
Combines build with config to create a release:

```bash
# Tag the release
git tag v1.2.3

# Deploy with environment-specific config
export DATABASE_URL=postgresql://...
export SECRET_KEY=prod-secret
export ENVIRONMENT=production

# Create release artifact
docker build -t myapp:v1.2.3 .
```

### Run Stage
Executes the release in the execution environment:

```bash
# Start the application
gunicorn app:create_app()

# Or with Docker
docker run -p 5000:5000 myapp:v1.2.3
```

### Key Files

- `Procfile` - Defines how to run the application
- `requirements.txt` - Build dependencies
- `app.py` - Runtime code

### Deployment Pipeline

1. **Build**: `pip install -r requirements.txt`
2. **Test**: `python -m pytest`
3. **Release**: Combine code + config
4. **Deploy**: Start processes defined in Procfile

### Best Practices

1. Automate the build process
2. Make releases immutable
3. Use unique release identifiers
4. Enable rollback to previous releases
5. Separate build and runtime dependencies

### Process Types (Procfile)

```
web: gunicorn app:create_app()
worker: celery -A tasks worker --loglevel=info
release: python manage.py migrate
```