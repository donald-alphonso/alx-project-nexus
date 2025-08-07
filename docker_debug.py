#!/usr/bin/env python
"""
Docker diagnostic script to check what's installed in the container.
"""

import subprocess
import sys
import os

def run_docker_command(service, command):
    """Run a command in a specific Docker service."""
    try:
        result = subprocess.run([
            'docker-compose', 'exec', '-T', service, 'sh', '-c', command
        ], capture_output=True, text=True, cwd='.')
        
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def check_requirements_in_container():
    """Check if requirements are properly installed in container."""
    print("🔍 Checking requirements installation in Docker container...")
    
    # Check if requirements.txt exists in container
    code, stdout, stderr = run_docker_command('web', 'cat requirements.txt')
    if code == 0:
        print("✅ requirements.txt found in container:")
        print(stdout[:500] + "..." if len(stdout) > 500 else stdout)
    else:
        print(f"❌ requirements.txt not found: {stderr}")
    
    # Check installed packages
    code, stdout, stderr = run_docker_command('web', 'pip list')
    if code == 0:
        print("\n📦 Installed packages in container:")
        lines = stdout.split('\n')
        for line in lines:
            if 'django' in line.lower() or 'rest' in line.lower() or 'graphene' in line.lower():
                print(f"  {line}")
    else:
        print(f"❌ Could not list packages: {stderr}")
    
    # Check if rest_framework is specifically installed
    code, stdout, stderr = run_docker_command('web', 'python -c "import rest_framework; print(rest_framework.__version__)"')
    if code == 0:
        print(f"✅ rest_framework version: {stdout.strip()}")
    else:
        print(f"❌ rest_framework not importable: {stderr}")

def check_django_settings():
    """Check Django settings in container."""
    print("\n🔍 Checking Django settings in container...")
    
    code, stdout, stderr = run_docker_command('web', 'python manage.py check --deploy')
    if code == 0:
        print("✅ Django check passed")
    else:
        print(f"❌ Django check failed: {stderr}")

if __name__ == "__main__":
    print("🐳 Docker Container Diagnostic")
    print("=" * 50)
    
    # First check if containers are running
    result = subprocess.run(['docker-compose', 'ps'], capture_output=True, text=True, cwd='.')
    if result.returncode != 0:
        print("❌ Docker containers not running. Start them first with: docker-compose up")
        sys.exit(1)
    
    check_requirements_in_container()
    check_django_settings()
    
    print("\n🏁 Diagnostic complete!")
