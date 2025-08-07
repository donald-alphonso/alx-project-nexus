#!/usr/bin/env python
"""
Local test script to verify Django setup without Docker.
"""

import os
import sys
import subprocess

def setup_local_env():
    """Setup local environment variables for testing."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_backend.settings')
    
    # Use SQLite for local testing
    os.environ['DB_ENGINE'] = 'django.db.backends.sqlite3'
    os.environ['DB_NAME'] = 'db.sqlite3'
    os.environ['DEBUG'] = 'True'
    os.environ['SECRET_KEY'] = 'test-secret-key-for-local-development'
    os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1'
    
    # Disable Celery for local testing
    os.environ['CELERY_TASK_ALWAYS_EAGER'] = 'True'
    
    print("🔧 Local environment configured for testing")

def test_django_check():
    """Run Django system checks."""
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'check'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Django system check passed!")
            return True
        else:
            print(f"❌ Django system check failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running Django check: {e}")
        return False

def test_migrations():
    """Test database migrations."""
    try:
        # Make migrations
        result = subprocess.run([
            sys.executable, 'manage.py', 'makemigrations'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode != 0:
            print(f"❌ Make migrations failed: {result.stderr}")
            return False
        
        # Apply migrations
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Database migrations successful!")
            return True
        else:
            print(f"❌ Database migrations failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

def test_graphql_schema():
    """Test GraphQL schema compilation."""
    try:
        import django
        django.setup()
        
        from social_media_backend.schema import schema
        print("✅ GraphQL schema compiled successfully!")
        return True
    except Exception as e:
        print(f"❌ GraphQL schema error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running Local Django Test...")
    print("=" * 50)
    
    setup_local_env()
    
    tests = [
        ("Django System Check", test_django_check),
        ("Database Migrations", test_migrations),
        ("GraphQL Schema", test_graphql_schema),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Django setup is working correctly.")
        print("\n💡 You can now run: python manage.py runserver")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
