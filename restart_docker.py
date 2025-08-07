#!/usr/bin/env python
"""
Clean Docker restart script.
"""

import subprocess
import sys
import time

def run_command(cmd, description):
    """Run a command and report status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def main():
    """Main restart function."""
    print("🐳 CLEAN DOCKER RESTART")
    print("=" * 40)
    
    steps = [
        ("docker-compose down -v", "Stopping containers and removing volumes"),
        ("docker system prune -f", "Cleaning Docker cache"),
        ("docker-compose up --build -d", "Building and starting containers")
    ]
    
    for cmd, description in steps:
        if not run_command(cmd, description):
            print(f"\n❌ Failed at step: {description}")
            sys.exit(1)
        time.sleep(2)
    
    print("\n⏳ Waiting for containers to start...")
    time.sleep(10)
    
    # Check container status
    print("\n🔍 Checking container status...")
    run_command("docker-compose ps", "Container status")
    
    print("\n🎉 Docker restart completed!")
    print("🌐 Application should be available at: http://localhost:8000")
    print("🔧 GraphQL endpoint: http://localhost:8000/graphql/")
    print("👤 Admin panel: http://localhost:8000/admin/")

if __name__ == "__main__":
    main()
