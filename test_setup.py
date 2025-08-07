#!/usr/bin/env python
"""
Test script to verify that all dependencies are properly installed.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required packages can be imported."""
    try:
        import django
        print(f"✅ Django {django.get_version()} - OK")
    except ImportError as e:
        print(f"❌ Django - ERROR: {e}")
        return False

    try:
        import rest_framework
        print(f"✅ Django REST Framework - OK")
    except ImportError as e:
        print(f"❌ Django REST Framework - ERROR: {e}")
        return False

    try:
        import graphene_django
        print(f"✅ Graphene Django - OK")
    except ImportError as e:
        print(f"❌ Graphene Django - ERROR: {e}")
        return False

    try:
        import celery
        print(f"✅ Celery - OK")
    except ImportError as e:
        print(f"❌ Celery - ERROR: {e}")
        return False

    try:
        import redis
        print(f"✅ Redis - OK")
    except ImportError as e:
        print(f"❌ Redis - ERROR: {e}")
        return False

    try:
        import corsheaders
        print(f"✅ CORS Headers - OK")
    except ImportError as e:
        print(f"❌ CORS Headers - ERROR: {e}")
        return False

    return True

def test_django_setup():
    """Test Django configuration."""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_backend.settings')
        import django
        django.setup()
        print("✅ Django setup - OK")
        return True
    except Exception as e:
        print(f"❌ Django setup - ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Social Media Backend Setup...")
    print("=" * 50)
    
    if test_imports():
        print("\n📦 All packages imported successfully!")
        
        if test_django_setup():
            print("✅ Django configuration is valid!")
            print("\n🎉 Setup test PASSED! Ready to run the application.")
            sys.exit(0)
        else:
            print("❌ Django configuration failed!")
            sys.exit(1)
    else:
        print("❌ Some packages are missing!")
        sys.exit(1)
