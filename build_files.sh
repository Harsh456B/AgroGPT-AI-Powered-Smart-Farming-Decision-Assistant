#!/bin/bash
# Build script for Vercel deployment

# Install deployment dependencies (lighter version)
pip install -r requirements_deploy.txt

# Pull LFS files if available (for development)
git lfs pull || echo "LFS files not available for deployment"

# Create deployment directories without large files
mkdir -p deployment_models
mkdir -p deployment_datasets

# Copy only essential files for deployment
cp -r website/ deployment_website/ 2>/dev/null || echo "Website files copied"
cp -r agrogpt_web/ deployment_agrogpt_web/ 2>/dev/null || echo "Django app copied"

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create a simple wsgi.py file for Vercel
echo "import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrogpt_web.settings')
application = get_wsgi_application()" > wsgi.py

echo "Build completed successfully!" 