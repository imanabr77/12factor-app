# Factor XII: Admin Processes

## Run admin/management tasks as one-off processes

### Implementation in Python Boyce

Administrative tasks run as one-off processes in the same environment:

- **Same Environment**: Admin tasks use same codebase and config
- **One-off Processes**: Tasks run once and exit
- **Same Runtime**: Use identical runtime environment as regular processes

### Admin Task Implementation

```python
# manage.py - Administrative tasks
#!/usr/bin/env python3
import os
import sys
from app import create_app

def migrate_database():
    """Run database migrations."""
    print("Running database migrations...")
    # Migration logic here
    print("Migrations completed successfully")

def seed_data():
    """Seed initial data."""
    app = create_app()
    with app.app_context():
        # Seed database with initial data
        print("Seeding initial data...")
        print("Data seeding completed")

def cleanup_old_logs():
    """Clean up old log entries."""
    print("Cleaning up old logs...")
    # Cleanup logic
    print("Log cleanup completed")

def generate_report():
    """Generate administrative reports."""
    app = create_app()
    with app.app_context():
        # Generate reports
        print("Generating administrative report...")
        print("Report generated successfully")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        print("Commands: migrate, seed, cleanup, report")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'migrate':
        migrate_database()
    elif command == 'seed':
        seed_data()
    elif command == 'cleanup':
        cleanup_old_logs()
    elif command == 'report':
        generate_report()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
```

### Procfile Integration

```
# Procfile
web: gunicorn app:create_app()
worker: celery -A tasks worker --loglevel=info
release: python manage.py migrate  # One-off process for releases
```

### Database Migrations

```python
# migrations.py
from app import create_app
import psycopg2

def run_migration_001():
    """Create users table."""
    app = create_app()
    conn = psycopg2.connect(app.config['DATABASE_URL'])
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Migration 001 completed: Created users table")
```

### Data Import/Export

```python
# data_tasks.py
import csv
import json
from app import create_app

def import_users_csv(filename):
    """Import users from CSV file."""
    app = create_app()
    with app.app_context():
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Import user data
                print(f"Imported user: {row['username']}")

def export_users_json(filename):
    """Export users to JSON file."""
    app = create_app()
    with app.app_context():
        # Export user data
        users = []  # Fetch from database
        with open(filename, 'w') as file:
            json.dump(users, file, indent=2)
        print(f"Exported {len(users)} users to {filename}")
```

### Running Admin Tasks

**Local Development**:
```bash
python manage.py migrate
python manage.py seed
python manage.py cleanup
```

**Heroku**:
```bash
heroku run python manage.py migrate --app myapp
heroku run python manage.py seed --app myapp
```

**Kubernetes**:
```bash
kubectl run migration --rm -i --tty --image=myapp:latest -- python manage.py migrate
```

**Docker**:
```bash
docker run --rm myapp:latest python manage.py migrate
```

### Best Practices

1. Use same codebase as web processes
2. Access same configuration and backing services
3. Run in identical environment
4. Make tasks idempotent (safe to run multiple times)
5. Log all administrative actions
6. Include proper error handling

### Scheduled Admin Tasks

```python
# For periodic admin tasks, use a scheduler process
# scheduler.py
import schedule
import time
from manage import cleanup_old_logs, generate_report

schedule.every().day.at("02:00").do(cleanup_old_logs)
schedule.every().week.do(generate_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```