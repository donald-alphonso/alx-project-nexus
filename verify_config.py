#!/usr/bin/env python
"""
Configuration verification script to ensure all files are consistent.
"""

import os
import re
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False

def extract_env_vars(filepath):
    """Extract environment variables from .env file."""
    env_vars = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        return env_vars
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return {}

def check_docker_compose_consistency():
    """Check docker-compose.yml consistency."""
    print("\n🔍 CHECKING DOCKER-COMPOSE.YML...")
    
    try:
        with open('docker-compose.yml', 'r') as f:
            content = f.read()
            
        # Extract PostgreSQL settings
        postgres_db = re.search(r'POSTGRES_DB=(\w+)', content)
        postgres_user = re.search(r'POSTGRES_USER=(\w+)', content)
        postgres_password = re.search(r'POSTGRES_PASSWORD=([^\s]+)', content)
        
        if postgres_db and postgres_user and postgres_password:
            print(f"✅ PostgreSQL DB: {postgres_db.group(1)}")
            print(f"✅ PostgreSQL User: {postgres_user.group(1)}")
            print(f"✅ PostgreSQL Password: {postgres_password.group(1)}")
            return {
                'db': postgres_db.group(1),
                'user': postgres_user.group(1),
                'password': postgres_password.group(1)
            }
        else:
            print("❌ Could not extract PostgreSQL settings from docker-compose.yml")
            return None
            
    except Exception as e:
        print(f"❌ Error reading docker-compose.yml: {e}")
        return None

def check_pyproject_dependencies():
    """Check pyproject.toml dependencies."""
    print("\n🔍 CHECKING PYPROJECT.TOML DEPENDENCIES...")
    
    try:
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            
        required_deps = [
            'Django',
            'djangorestframework',
            'psycopg2-binary',
            'graphene-django',
            'celery',
            'redis',
            'gunicorn'
        ]
        
        missing_deps = []
        for dep in required_deps:
            if dep.lower() in content.lower():
                print(f"✅ {dep} found in pyproject.toml")
            else:
                print(f"❌ {dep} MISSING from pyproject.toml")
                missing_deps.append(dep)
                
        return len(missing_deps) == 0
        
    except Exception as e:
        print(f"❌ Error reading pyproject.toml: {e}")
        return False

def check_settings_consistency():
    """Check Django settings consistency."""
    print("\n🔍 CHECKING DJANGO SETTINGS...")
    
    try:
        with open('social_media_backend/settings.py', 'r') as f:
            content = f.read()
            
        # Check INSTALLED_APPS
        if "'rest_framework'" in content:
            print("✅ rest_framework in INSTALLED_APPS")
        else:
            print("❌ rest_framework MISSING from INSTALLED_APPS")
            
        if "'graphene_django'" in content:
            print("✅ graphene_django in INSTALLED_APPS")
        else:
            print("❌ graphene_django MISSING from INSTALLED_APPS")
            
        if "'corsheaders'" in content:
            print("✅ corsheaders in INSTALLED_APPS")
        else:
            print("❌ corsheaders MISSING from INSTALLED_APPS")
            
        # Check database configuration
        if "postgresql" in content.lower():
            print("✅ PostgreSQL configuration found")
        else:
            print("❌ PostgreSQL configuration not found")
            
        return True
        
    except Exception as e:
        print(f"❌ Error reading settings.py: {e}")
        return False

def main():
    """Main verification function."""
    print("🔍 CONFIGURATION VERIFICATION")
    print("=" * 50)
    
    # Check essential files
    files_ok = True
    essential_files = [
        ('docker-compose.yml', 'Docker Compose file'),
        ('.env.docker', 'Docker environment file'),
        ('pyproject.toml', 'Poetry configuration'),
        ('Dockerfile', 'Docker build file'),
        ('entrypoint.sh', 'Docker entrypoint script'),
        ('social_media_backend/settings.py', 'Django settings'),
        ('manage.py', 'Django management script')
    ]
    
    for filepath, description in essential_files:
        if not check_file_exists(filepath, description):
            files_ok = False
    
    if not files_ok:
        print("\n❌ Some essential files are missing!")
        return False
    
    # Check .env.docker variables
    print("\n🔍 CHECKING .ENV.DOCKER VARIABLES...")
    env_vars = extract_env_vars('.env.docker')
    
    required_env_vars = [
        'SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS',
        'DB_ENGINE', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT',
        'REDIS_URL', 'CELERY_BROKER_URL', 'CELERY_RESULT_BACKEND'
    ]
    
    env_ok = True
    for var in required_env_vars:
        if var in env_vars:
            print(f"✅ {var}: {env_vars[var]}")
        else:
            print(f"❌ {var} MISSING from .env.docker")
            env_ok = False
    
    # Check docker-compose consistency
    docker_config = check_docker_compose_consistency()
    
    # Compare .env.docker with docker-compose.yml
    if docker_config and env_vars:
        print("\n🔍 CHECKING CONSISTENCY BETWEEN FILES...")
        
        if env_vars.get('DB_NAME') == docker_config['db']:
            print("✅ Database name matches")
        else:
            print(f"❌ Database name mismatch: .env.docker={env_vars.get('DB_NAME')} vs docker-compose={docker_config['db']}")
            
        if env_vars.get('DB_USER') == docker_config['user']:
            print("✅ Database user matches")
        else:
            print(f"❌ Database user mismatch: .env.docker={env_vars.get('DB_USER')} vs docker-compose={docker_config['user']}")
            
        if env_vars.get('DB_PASSWORD') == docker_config['password']:
            print("✅ Database password matches")
        else:
            print(f"❌ Database password mismatch: .env.docker={env_vars.get('DB_PASSWORD')} vs docker-compose={docker_config['password']}")
    
    # Check dependencies
    deps_ok = check_pyproject_dependencies()
    
    # Check Django settings
    settings_ok = check_settings_consistency()
    
    # Final summary
    print("\n📊 VERIFICATION SUMMARY")
    print("=" * 30)
    
    all_checks = [
        ("Essential files", files_ok),
        ("Environment variables", env_ok),
        ("Dependencies", deps_ok),
        ("Django settings", settings_ok)
    ]
    
    passed = sum(1 for _, status in all_checks if status)
    total = len(all_checks)
    
    for check_name, status in all_checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name}")
    
    print(f"\n🎯 RESULT: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All configurations are correct! Ready to restart Docker.")
        return True
    else:
        print("❌ Some configurations need to be fixed before restarting.")
        return False

if __name__ == "__main__":
    main()
