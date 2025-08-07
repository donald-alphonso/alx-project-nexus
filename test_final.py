#!/usr/bin/env python
"""
Final test to verify everything is working.
"""

import requests
import json
import time

def test_django_home():
    """Test Django home page."""
    try:
        response = requests.get('http://localhost:8000/', timeout=10)
        if response.status_code == 200:
            print("✅ Django home page accessible")
            return True
        else:
            print(f"❌ Django home page returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Django home page error: {e}")
        return False

def test_graphql_endpoint():
    """Test GraphQL endpoint."""
    try:
        # Simple introspection query
        query = {
            "query": "{ __schema { types { name } } }"
        }
        
        response = requests.post(
            'http://localhost:8000/graphql/',
            json=query,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and '__schema' in data['data']:
                print("✅ GraphQL endpoint working")
                return True
            else:
                print(f"❌ GraphQL returned unexpected data: {data}")
                return False
        else:
            print(f"❌ GraphQL endpoint returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GraphQL endpoint error: {e}")
        return False

def test_admin_panel():
    """Test admin panel accessibility."""
    try:
        response = requests.get('http://localhost:8000/admin/', timeout=10)
        if response.status_code == 200:
            print("✅ Admin panel accessible")
            return True
        else:
            print(f"❌ Admin panel returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Admin panel error: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 FINAL APPLICATION TEST")
    print("=" * 40)
    
    print("⏳ Waiting for application to be ready...")
    time.sleep(5)
    
    tests = [
        ("Django Home Page", test_django_home),
        ("GraphQL Endpoint", test_graphql_endpoint),
        ("Admin Panel", test_admin_panel)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        time.sleep(1)
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Application is fully functional.")
        print("\n🌐 Your Social Media Backend is ready!")
        print("📍 Main URL: http://localhost:8000")
        print("🔧 GraphQL: http://localhost:8000/graphql/")
        print("👤 Admin: http://localhost:8000/admin/ (admin/admin123)")
        return True
    else:
        print("❌ Some tests failed. Check the logs above.")
        return False

if __name__ == "__main__":
    main()
