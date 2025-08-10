#!/usr/bin/env python3
"""
Quick Project Validation
Discrete validation for ALX presentation readiness
"""

import os
import requests
import json
from datetime import datetime

def check_project_structure():
    """Validate project organization"""
    required_files = [
        'README.md',
        'docker-compose.yml',
        'manage.py',
        'docs/PRESENTATION_5MIN.md',
        'docs/PROJECT_OVERVIEW.md'
    ]
    
    required_dirs = [
        'docs',
        'scripts',
        'users',
        'posts',
        'interactions'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(f"File: {file}")
    
    for directory in required_dirs:
        if not os.path.isdir(directory):
            missing.append(f"Directory: {directory}")
    
    return len(missing) == 0, missing

def check_services():
    """Check if services are accessible"""
    endpoints = {
        'GraphQL': 'http://localhost:8000/graphql/',
        'Admin': 'http://localhost:8000/admin/',
        'Health': 'http://localhost:8000/api/health/'
    }
    
    results = {}
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            results[name] = response.status_code < 500
        except:
            results[name] = False
    
    return results

def check_documentation():
    """Validate documentation completeness"""
    docs_structure = {
        'docs/INDEX.md': 'Documentation index',
        'docs/guides/POWERPOINT_CREATION_GUIDE.md': 'PowerPoint guide',
        'docs/PRESENTATION_5MIN.md': '5-minute presentation',
        'docs/PROJECT_OVERVIEW.md': 'Complete overview'
    }
    
    missing_docs = []
    for doc, description in docs_structure.items():
        if not os.path.exists(doc):
            missing_docs.append(f"{description}: {doc}")
    
    return len(missing_docs) == 0, missing_docs

def main():
    """Quick validation for presentation readiness"""
    print("🔍 Quick Project Validation")
    print("=" * 40)
    
    # Structure check
    structure_ok, missing_structure = check_project_structure()
    print(f"📁 Project Structure: {'✅ OK' if structure_ok else '❌ Issues'}")
    if missing_structure:
        for item in missing_structure[:3]:  # Show max 3
            print(f"   - Missing: {item}")
    
    # Services check
    services = check_services()
    print(f"🌐 Services Status:")
    for service, status in services.items():
        print(f"   - {service}: {'✅ OK' if status else '❌ Down'}")
    
    # Documentation check
    docs_ok, missing_docs = check_documentation()
    print(f"📚 Documentation: {'✅ Complete' if docs_ok else '❌ Missing'}")
    if missing_docs:
        for doc in missing_docs[:2]:  # Show max 2
            print(f"   - {doc}")
    
    # Overall status
    all_services_ok = all(services.values())
    overall_ready = structure_ok and all_services_ok and docs_ok
    
    print("\n" + "=" * 40)
    print(f"🎯 Presentation Ready: {'✅ YES' if overall_ready else '❌ NO'}")
    
    if overall_ready:
        print("🎊 Project is ready for ALX presentation!")
        print("📋 Next steps:")
        print("   1. Review PRESENTATION_5MIN.md")
        print("   2. Create PowerPoint using the guide")
        print("   3. Practice your 5-minute demo")
    else:
        print("⚠️ Please address the issues above")
    
    return overall_ready

if __name__ == "__main__":
    try:
        ready = main()
        exit(0 if ready else 1)
    except Exception as e:
        print(f"❌ Validation error: {e}")
        exit(1)
