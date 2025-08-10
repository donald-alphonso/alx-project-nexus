#!/usr/bin/env python3
"""
Celery Management Script
Manage Celery workers, beat scheduler, and monitor tasks
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print(f"{'='*60}")

def print_status(message, status="INFO"):
    """Print a status message"""
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    print(f"{icons.get(status, 'ℹ️')} {message}")

def check_redis_connection():
    """Check if Redis is running and accessible"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=1)
        r.ping()
        print_status("Redis connection successful", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Redis connection failed: {e}", "ERROR")
        return False

def check_django_app():
    """Check if Django app is running"""
    try:
        response = requests.get('http://localhost:8000/api/health/', timeout=5)
        if response.status_code == 200:
            print_status("Django app is running", "SUCCESS")
            return True
        else:
            print_status(f"Django app returned status {response.status_code}", "WARNING")
            return False
    except Exception as e:
        print_status(f"Django app not accessible: {e}", "ERROR")
        return False

def start_celery_worker():
    """Start Celery worker"""
    print_header("Starting Celery Worker")
    
    if not check_redis_connection():
        print_status("Cannot start worker without Redis", "ERROR")
        return False
    
    try:
        # Change to project directory
        os.chdir(project_root)
        
        # Start Celery worker
        cmd = [
            'celery', '-A', 'social_media_backend', 'worker',
            '--loglevel=info',
            '--concurrency=4',
            '--queues=default,users,media,analytics,maintenance,emails'
        ]
        
        print_status(f"Starting worker with command: {' '.join(cmd)}", "INFO")
        
        # Start worker in background
        process = subprocess.Popen(cmd)
        print_status(f"Celery worker started with PID: {process.pid}", "SUCCESS")
        
        return True
        
    except Exception as e:
        print_status(f"Failed to start Celery worker: {e}", "ERROR")
        return False

def start_celery_beat():
    """Start Celery beat scheduler"""
    print_header("Starting Celery Beat Scheduler")
    
    if not check_redis_connection():
        print_status("Cannot start beat without Redis", "ERROR")
        return False
    
    try:
        # Change to project directory
        os.chdir(project_root)
        
        # Start Celery beat
        cmd = [
            'celery', '-A', 'social_media_backend', 'beat',
            '--loglevel=info',
            '--scheduler=django_celery_beat.schedulers:DatabaseScheduler'
        ]
        
        print_status(f"Starting beat with command: {' '.join(cmd)}", "INFO")
        
        # Start beat in background
        process = subprocess.Popen(cmd)
        print_status(f"Celery beat started with PID: {process.pid}", "SUCCESS")
        
        return True
        
    except Exception as e:
        print_status(f"Failed to start Celery beat: {e}", "ERROR")
        return False

def monitor_celery():
    """Monitor Celery workers and tasks"""
    print_header("Celery Monitoring")
    
    try:
        # Change to project directory
        os.chdir(project_root)
        
        # Check worker status
        print_status("Checking worker status...", "INFO")
        result = subprocess.run(['celery', '-A', 'social_media_backend', 'inspect', 'active'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print_status("Worker status check successful", "SUCCESS")
            print(result.stdout)
        else:
            print_status("No active workers found", "WARNING")
        
        # Check scheduled tasks
        print_status("Checking scheduled tasks...", "INFO")
        result = subprocess.run(['celery', '-A', 'social_media_backend', 'inspect', 'scheduled'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print_status("Scheduled tasks check successful", "SUCCESS")
            print(result.stdout)
        
    except Exception as e:
        print_status(f"Monitoring failed: {e}", "ERROR")

def test_celery_tasks():
    """Test Celery tasks execution"""
    print_header("Testing Celery Tasks")
    
    try:
        # Change to project directory and set Django settings
        os.chdir(project_root)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_backend.settings')
        
        import django
        django.setup()
        
        # Import tasks
        from users.tasks import cleanup_expired_tokens, update_user_statistics
        from posts.tasks import update_trending_hashtags, generate_content_analytics
        
        # Test user tasks
        print_status("Testing user tasks...", "INFO")
        result1 = cleanup_expired_tokens.delay()
        print_status(f"cleanup_expired_tokens task ID: {result1.id}", "SUCCESS")
        
        result2 = update_user_statistics.delay()
        print_status(f"update_user_statistics task ID: {result2.id}", "SUCCESS")
        
        # Test post tasks
        print_status("Testing post tasks...", "INFO")
        result3 = update_trending_hashtags.delay()
        print_status(f"update_trending_hashtags task ID: {result3.id}", "SUCCESS")
        
        result4 = generate_content_analytics.delay()
        print_status(f"generate_content_analytics task ID: {result4.id}", "SUCCESS")
        
        print_status("All test tasks submitted successfully", "SUCCESS")
        
        # Wait a bit and check results
        time.sleep(5)
        
        print_status("Checking task results...", "INFO")
        for i, result in enumerate([result1, result2, result3, result4], 1):
            if result.ready():
                print_status(f"Task {i} completed: {result.result}", "SUCCESS")
            else:
                print_status(f"Task {i} still running...", "WARNING")
        
    except Exception as e:
        print_status(f"Task testing failed: {e}", "ERROR")

def show_celery_status():
    """Show comprehensive Celery status"""
    print_header("Celery System Status")
    
    # Check dependencies
    print_status("Checking system dependencies...", "INFO")
    redis_ok = check_redis_connection()
    django_ok = check_django_app()
    
    # Check Celery processes
    print_status("Checking Celery processes...", "INFO")
    try:
        # Check for running Celery processes
        result = subprocess.run(['pgrep', '-f', 'celery'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print_status(f"Found {len(pids)} Celery processes: {', '.join(pids)}", "SUCCESS")
        else:
            print_status("No Celery processes running", "WARNING")
    except Exception as e:
        print_status(f"Process check failed: {e}", "ERROR")
    
    # Summary
    print_header("System Summary")
    print_status(f"Redis: {'✅ OK' if redis_ok else '❌ NOT OK'}")
    print_status(f"Django: {'✅ OK' if django_ok else '❌ NOT OK'}")
    
    if redis_ok and django_ok:
        print_status("System ready for Celery operations", "SUCCESS")
    else:
        print_status("System not ready - fix dependencies first", "ERROR")

def main():
    """Main function"""
    print_header("ALX Project Nexus - Celery Manager")
    
    if len(sys.argv) < 2:
        print("""
Usage: python CELERY_MANAGER.py <command>

Commands:
  status     - Show Celery system status
  worker     - Start Celery worker
  beat       - Start Celery beat scheduler
  monitor    - Monitor Celery workers and tasks
  test       - Test Celery tasks execution
  help       - Show this help message

Examples:
  python CELERY_MANAGER.py status
  python CELERY_MANAGER.py worker
  python CELERY_MANAGER.py test
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'status':
        show_celery_status()
    elif command == 'worker':
        start_celery_worker()
    elif command == 'beat':
        start_celery_beat()
    elif command == 'monitor':
        monitor_celery()
    elif command == 'test':
        test_celery_tasks()
    elif command == 'help':
        main()
    else:
        print_status(f"Unknown command: {command}", "ERROR")
        main()

if __name__ == "__main__":
    main()
