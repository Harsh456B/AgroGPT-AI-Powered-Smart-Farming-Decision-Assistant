#!/usr/bin/env python3
"""
Deployment Helper Script for AgroGPT Web
This script helps prepare your project for deployment on free platforms.
"""

import os
import sys
from django.core.management.utils import get_random_secret_key

def generate_secret_key():
    """Generate a new Django secret key"""
    return get_random_secret_key()

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'manage.py',
        'agrogpt_web/settings.py',
        'agrogpt_web/wsgi.py',
        'website/views.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found!")
    return True

def check_models():
    """Check if ML models exist"""
    models_dir = 'models'
    if not os.path.exists(models_dir):
        print("❌ Models directory not found!")
        return False
    
    model_files = os.listdir(models_dir)
    if not model_files:
        print("❌ No model files found in models/ directory!")
        return False
    
    print(f"✅ Found {len(model_files)} model files")
    return True

def main():
    print("🚀 AgroGPT Web Deployment Helper")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please fix missing files before deploying.")
        return
    
    # Check models
    if not check_models():
        print("\n❌ Please ensure ML models are in place.")
        return
    
    # Generate secret key
    secret_key = generate_secret_key()
    print(f"\n🔑 Generated Secret Key:")
    print(f"   {secret_key}")
    print("\n📝 Add this to your environment variables:")
    print(f"   SECRET_KEY={secret_key}")
    
    # Deployment options
    print("\n🌐 Deployment Options:")
    print("1. Railway (Recommended) - 500 hours/month free")
    print("2. Render - 750 hours/month free")
    print("3. Vercel - Great for static sites")
    print("4. PythonAnywhere - Educational")
    
    print("\n📋 Next Steps:")
    print("1. Push your code to GitHub")
    print("2. Choose a platform from above")
    print("3. Connect your GitHub repository")
    print("4. Set environment variables")
    print("5. Deploy!")
    
    print("\n✅ Your project is ready for deployment!")

if __name__ == "__main__":
    main() 