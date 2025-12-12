#!/usr/bin/env python3
"""
Python Boyce - A 12-Factor App Example
A demonstration application implementing all 12 factors of modern app development.
"""

import os
import sys
import json
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern for better testability."""
    app = Flask(__name__)
    
    # Trust proxy headers (Factor XII - Admin processes)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Configuration from environment (Factor III - Config)
    app.config.update({
        'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
        'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-key-change-in-production'),
        'DATABASE_URL': os.getenv('DATABASE_URL', 'sqlite:///app.db'),
        'REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379'),
        'PORT': int(os.getenv('PORT', 5000)),
    })
    
    @app.route('/')
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': os.getenv('APP_VERSION', '1.0.0'),
            'environment': os.getenv('ENVIRONMENT', 'development')
        })
    
    @app.route('/config')
    def show_config():
        """Show non-sensitive configuration."""
        safe_config = {
            'debug': app.config['DEBUG'],
            'environment': os.getenv('ENVIRONMENT', 'development'),
            'version': os.getenv('APP_VERSION', '1.0.0'),
            'port': app.config['PORT']
        }
        return jsonify(safe_config)
    
    @app.route('/logs')
    def generate_logs():
        """Generate sample log entries."""
        logger.info("Info log generated via API")
        logger.warning("Warning log generated via API")
        logger.error("Error log generated via API")
        return jsonify({'message': 'Logs generated successfully'})
    
    return app

def main():
    """Main application entry point."""
    app = create_app()
    port = app.config['PORT']
    
    logger.info(f"Starting Python Boyce application on port {port}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    # Factor VII - Port binding
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])

if __name__ == '__main__':
    main()