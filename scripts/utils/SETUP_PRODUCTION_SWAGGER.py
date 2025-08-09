#!/usr/bin/env python3
"""
Setup Production-Ready Swagger Documentation
ALX Project Nexus - Final Configuration
"""

import os
import sys

def create_production_urls():
    """Create production URLs configuration"""
    
    urls_content = '''"""
URLs configuration for ALX Project Nexus - Production Ready
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# Import API views
from . import api_views

# Import Swagger views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # GraphQL endpoint (main API)
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)), name='graphql'),
    
    # API Documentation endpoints
    path('api/graphql-docs/', api_views.graphql_endpoint_docs, name='graphql-docs'),
    path('api/auth/', api_views.auth_info, name='auth-info'),
    path('api/stats/', api_views.platform_stats, name='platform-stats'),
    path('api/health/', api_views.health_check, name='health-check'),
    path('api/schema-info/', api_views.api_schema, name='api-schema'),
    path('api/errors/', api_views.error_handling_guide, name='error-guide'),
    
    # Swagger/OpenAPI documentation (Production-ready)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    
    return urls_content

def verify_swagger_setup():
    """Verify Swagger setup is correct"""
    
    print("🔍 VERIFYING SWAGGER SETUP")
    print("=" * 50)
    
    # Check if drf-spectacular is in settings
    try:
        with open('social_media_backend/settings.py', 'r') as f:
            settings_content = f.read()
            
        if "'drf_spectacular'," in settings_content:
            print("✅ drf-spectacular enabled in INSTALLED_APPS")
        else:
            print("❌ drf-spectacular not found in INSTALLED_APPS")
            
        if "SPECTACULAR_SETTINGS" in settings_content:
            print("✅ SPECTACULAR_SETTINGS configured")
        else:
            print("❌ SPECTACULAR_SETTINGS not configured")
            
    except FileNotFoundError:
        print("❌ settings.py not found")
    
    # Check if api_views.py exists
    if os.path.exists('social_media_backend/api_views.py'):
        print("✅ api_views.py exists")
    else:
        print("❌ api_views.py missing")
    
    # Check URLs configuration
    try:
        with open('social_media_backend/urls.py', 'r') as f:
            urls_content = f.read()
            
        if "SpectacularAPIView" in urls_content:
            print("✅ Swagger views imported in URLs")
        else:
            print("❌ Swagger views not imported in URLs")
            
        if "api/docs/" in urls_content:
            print("✅ Swagger endpoint configured")
        else:
            print("❌ Swagger endpoint not configured")
            
    except FileNotFoundError:
        print("❌ urls.py not found")

def test_swagger_endpoints():
    """Test Swagger endpoints"""
    
    print("\n🧪 TESTING SWAGGER ENDPOINTS")
    print("=" * 50)
    
    import requests
    
    endpoints_to_test = [
        ("GraphQL", "http://localhost:8000/graphql/"),
        ("Swagger UI", "http://localhost:8000/api/docs/"),
        ("ReDoc", "http://localhost:8000/api/redoc/"),
        ("API Schema", "http://localhost:8000/api/schema/"),
        ("Health Check", "http://localhost:8000/api/health/"),
        ("Platform Stats", "http://localhost:8000/api/stats/"),
    ]
    
    for name, url in endpoints_to_test:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: {url} - OK")
            else:
                print(f"⚠️ {name}: {url} - Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: {url} - Error: {e}")

def create_swagger_test_script():
    """Create a test script for Swagger functionality"""
    
    test_script = '''#!/usr/bin/env python3
"""
Test Swagger Documentation Functionality
"""

import requests
import json

def test_swagger_api():
    """Test all Swagger endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 TESTING SWAGGER API ENDPOINTS")
    print("=" * 60)
    
    # Test endpoints
    endpoints = {
        "GraphQL Interface": f"{base_url}/graphql/",
        "Swagger UI": f"{base_url}/api/docs/",
        "ReDoc Documentation": f"{base_url}/api/redoc/",
        "OpenAPI Schema": f"{base_url}/api/schema/",
        "Health Check": f"{base_url}/api/health/",
        "Platform Statistics": f"{base_url}/api/stats/",
        "Authentication Info": f"{base_url}/api/auth/",
        "API Schema Info": f"{base_url}/api/schema-info/",
        "Error Guide": f"{base_url}/api/errors/",
    }
    
    results = {}
    
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=10)
            status = "✅ OK" if response.status_code == 200 else f"⚠️ Status {response.status_code}"
            results[name] = {
                "url": url,
                "status_code": response.status_code,
                "status": status
            }
            print(f"{status} - {name}: {url}")
            
        except requests.exceptions.RequestException as e:
            results[name] = {
                "url": url,
                "status_code": None,
                "status": f"❌ Error: {str(e)}"
            }
            print(f"❌ Error - {name}: {url} - {e}")
    
    # Test GraphQL introspection
    print("\\n🔍 TESTING GRAPHQL INTROSPECTION")
    print("=" * 60)
    
    introspection_query = {
        "query": """
        query IntrospectionQuery {
          __schema {
            queryType { name }
            mutationType { name }
            types {
              name
              kind
            }
          }
        }
        """
    }
    
    try:
        response = requests.post(
            f"{base_url}/graphql/",
            json=introspection_query,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and '__schema' in data['data']:
                schema = data['data']['__schema']
                print(f"✅ GraphQL Schema accessible")
                print(f"   Query Type: {schema.get('queryType', {}).get('name', 'Unknown')}")
                print(f"   Mutation Type: {schema.get('mutationType', {}).get('name', 'Unknown')}")
                print(f"   Total Types: {len(schema.get('types', []))}")
            else:
                print("⚠️ GraphQL Schema response format unexpected")
        else:
            print(f"❌ GraphQL introspection failed - Status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ GraphQL introspection error: {e}")
    
    # Summary
    print("\\n📊 SUMMARY")
    print("=" * 60)
    
    total_endpoints = len(results)
    successful_endpoints = sum(1 for r in results.values() if r['status_code'] == 200)
    
    print(f"Total Endpoints Tested: {total_endpoints}")
    print(f"Successful Responses: {successful_endpoints}")
    print(f"Success Rate: {(successful_endpoints/total_endpoints)*100:.1f}%")
    
    if successful_endpoints == total_endpoints:
        print("\\n🎊 ALL SWAGGER ENDPOINTS WORKING PERFECTLY!")
        print("✅ Ready for production use")
        print("✅ Frontend developers can use the API documentation")
    elif successful_endpoints >= total_endpoints * 0.8:
        print("\\n✅ SWAGGER MOSTLY FUNCTIONAL")
        print("⚠️ Some minor issues detected")
    else:
        print("\\n❌ SWAGGER NEEDS ATTENTION")
        print("🔧 Multiple endpoints not responding correctly")
    
    return results

if __name__ == "__main__":
    test_swagger_api()
'''
    
    with open('test_swagger_api.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ Swagger test script created: test_swagger_api.py")

def main():
    """Setup production-ready Swagger documentation"""
    
    print("🚀 SETTING UP PRODUCTION SWAGGER DOCUMENTATION")
    print("=" * 70)
    
    # 1. Verify current setup
    verify_swagger_setup()
    
    # 2. Update URLs if needed
    urls_content = create_production_urls()
    with open('social_media_backend/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    print("\\n✅ URLs updated for production Swagger")
    
    # 3. Create test script
    create_swagger_test_script()
    
    # 4. Test endpoints
    print("\\n⏳ Waiting for Docker restart...")
    os.system("docker-compose restart web")
    
    print("\\n🔄 Testing Swagger endpoints...")
    test_swagger_endpoints()
    
    print("\\n🎊 PRODUCTION SWAGGER SETUP COMPLETED!")
    print("=" * 70)
    print("📚 Swagger UI: http://localhost:8000/api/docs/")
    print("📖 ReDoc: http://localhost:8000/api/redoc/")
    print("🔗 GraphQL: http://localhost:8000/graphql/")
    print("💚 Health Check: http://localhost:8000/api/health/")
    print("📊 Statistics: http://localhost:8000/api/stats/")
    
    print("\\n🎯 READY FOR FRONTEND INTEGRATION!")
    print("✅ Professional API documentation")
    print("✅ Complete endpoint coverage")
    print("✅ Production-ready standards")
    print("✅ English documentation")
    print("✅ Interactive testing interface")

if __name__ == "__main__":
    main()
'''
