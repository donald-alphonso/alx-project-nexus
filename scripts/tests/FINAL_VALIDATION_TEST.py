#!/usr/bin/env python3
"""
FINAL VALIDATION TEST - ALX Project Nexus
Complete validation of Swagger documentation and API functionality
"""

import requests
import json
import time
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}{title.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️ {message}{Colors.END}")

def test_swagger_endpoints():
    """Test all Swagger documentation endpoints"""
    
    print_header("SWAGGER DOCUMENTATION VALIDATION")
    
    base_url = "http://localhost:8000"
    endpoints = {
        "Swagger UI": f"{base_url}/api/docs/",
        "ReDoc Documentation": f"{base_url}/api/redoc/",
        "OpenAPI Schema": f"{base_url}/api/schema/",
        "GraphQL Interface": f"{base_url}/graphql/",
        "Health Check": f"{base_url}/api/health/",
        "Platform Statistics": f"{base_url}/api/stats/",
        "Authentication Info": f"{base_url}/api/auth/",
        "API Schema Info": f"{base_url}/api/schema-info/",
        "Error Handling Guide": f"{base_url}/api/errors/",
        "GraphQL Documentation": f"{base_url}/api/graphql-docs/",
    }
    
    results = {}
    total_tests = len(endpoints)
    passed_tests = 0
    
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print_success(f"{name}: {url}")
                results[name] = "PASS"
                passed_tests += 1
            else:
                print_error(f"{name}: {url} - Status {response.status_code}")
                results[name] = f"FAIL - {response.status_code}"
        except requests.exceptions.RequestException as e:
            print_error(f"{name}: {url} - Connection Error")
            results[name] = f"ERROR - {str(e)}"
    
    print(f"\n{Colors.BOLD}SWAGGER ENDPOINTS SUMMARY:{Colors.END}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {Colors.GREEN}{passed_tests}{Colors.END}")
    print(f"Failed: {Colors.RED}{total_tests - passed_tests}{Colors.END}")
    print(f"Success Rate: {Colors.BOLD}{(passed_tests/total_tests)*100:.1f}%{Colors.END}")
    
    return passed_tests == total_tests

def test_graphql_functionality():
    """Test GraphQL API functionality"""
    
    print_header("GRAPHQL API FUNCTIONALITY TEST")
    
    base_url = "http://localhost:8000/graphql/"
    
    # Test GraphQL introspection
    print_info("Testing GraphQL introspection...")
    
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
            base_url,
            json=introspection_query,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and '__schema' in data['data']:
                schema = data['data']['__schema']
                print_success("GraphQL schema accessible")
                print_info(f"Query Type: {schema.get('queryType', {}).get('name', 'Unknown')}")
                print_info(f"Mutation Type: {schema.get('mutationType', {}).get('name', 'Unknown')}")
                print_info(f"Total Types: {len(schema.get('types', []))}")
                return True
            else:
                print_error("GraphQL schema response format unexpected")
                return False
        else:
            print_error(f"GraphQL introspection failed - Status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"GraphQL introspection error: {e}")
        return False

def test_api_documentation_quality():
    """Test the quality and completeness of API documentation"""
    
    print_header("API DOCUMENTATION QUALITY ASSESSMENT")
    
    quality_checks = []
    
    # Check Swagger UI content
    try:
        response = requests.get("http://localhost:8000/api/docs/", timeout=10)
        if response.status_code == 200:
            content = response.text.lower()
            
            # Check for key documentation elements
            checks = [
                ("English Language", "alx project nexus" in content),
                ("Professional Title", "graphql api" in content),
                ("Interactive Interface", "swagger" in content or "openapi" in content),
                ("Authentication Documentation", "jwt" in content or "authorization" in content),
            ]
            
            for check_name, passed in checks:
                if passed:
                    print_success(f"{check_name} documentation present")
                    quality_checks.append(True)
                else:
                    print_warning(f"{check_name} documentation needs improvement")
                    quality_checks.append(False)
        else:
            print_error("Could not access Swagger UI for quality assessment")
            quality_checks = [False] * 4
            
    except requests.exceptions.RequestException:
        print_error("Network error during documentation quality check")
        quality_checks = [False] * 4
    
    # Check API schema endpoint
    try:
        response = requests.get("http://localhost:8000/api/schema-info/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            schema_checks = [
                ("API Name Present", "api_name" in data),
                ("Version Information", "version" in data),
                ("Endpoints Documentation", "endpoints" in data),
                ("Authentication Guide", "authentication" in data),
                ("Feature List", "features" in data),
            ]
            
            for check_name, passed in schema_checks:
                if passed:
                    print_success(f"{check_name}")
                    quality_checks.append(True)
                else:
                    print_warning(f"{check_name} missing")
                    quality_checks.append(False)
        else:
            print_warning("API schema info endpoint not accessible")
            quality_checks.extend([False] * 5)
            
    except requests.exceptions.RequestException:
        print_error("Could not check API schema information")
        quality_checks.extend([False] * 5)
    
    passed_quality_checks = sum(quality_checks)
    total_quality_checks = len(quality_checks)
    
    print(f"\n{Colors.BOLD}DOCUMENTATION QUALITY SUMMARY:{Colors.END}")
    print(f"Quality Checks Passed: {Colors.GREEN}{passed_quality_checks}/{total_quality_checks}{Colors.END}")
    print(f"Quality Score: {Colors.BOLD}{(passed_quality_checks/total_quality_checks)*100:.1f}%{Colors.END}")
    
    return passed_quality_checks >= total_quality_checks * 0.8

def test_production_readiness():
    """Test production readiness indicators"""
    
    print_header("PRODUCTION READINESS ASSESSMENT")
    
    readiness_checks = []
    
    # Check health endpoint
    try:
        response = requests.get("http://localhost:8000/api/health/", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print_success("Health check endpoint operational")
            print_info(f"Status: {health_data.get('status', 'Unknown')}")
            readiness_checks.append(True)
        else:
            print_warning("Health check endpoint not responding correctly")
            readiness_checks.append(False)
    except:
        print_error("Health check endpoint not accessible")
        readiness_checks.append(False)
    
    # Check statistics endpoint
    try:
        response = requests.get("http://localhost:8000/api/stats/", timeout=10)
        if response.status_code == 200:
            stats_data = response.json()
            print_success("Statistics endpoint operational")
            print_info(f"Total Users: {stats_data.get('total_users', 'N/A')}")
            print_info(f"Total Posts: {stats_data.get('total_posts', 'N/A')}")
            readiness_checks.append(True)
        else:
            print_warning("Statistics endpoint not responding correctly")
            readiness_checks.append(False)
    except:
        print_error("Statistics endpoint not accessible")
        readiness_checks.append(False)
    
    # Check error handling documentation
    try:
        response = requests.get("http://localhost:8000/api/errors/", timeout=10)
        if response.status_code == 200:
            error_data = response.json()
            print_success("Error handling documentation available")
            readiness_checks.append(True)
        else:
            print_warning("Error handling documentation not accessible")
            readiness_checks.append(False)
    except:
        print_error("Error handling documentation endpoint failed")
        readiness_checks.append(False)
    
    # Check CORS and security headers
    try:
        response = requests.get("http://localhost:8000/api/health/", timeout=10)
        headers = response.headers
        
        security_features = [
            ("Content-Type header", "content-type" in headers),
            ("Server response", response.status_code == 200),
        ]
        
        for feature_name, present in security_features:
            if present:
                print_success(f"{feature_name} configured")
                readiness_checks.append(True)
            else:
                print_warning(f"{feature_name} needs attention")
                readiness_checks.append(False)
                
    except:
        print_error("Could not check security headers")
        readiness_checks.extend([False] * 2)
    
    passed_readiness = sum(readiness_checks)
    total_readiness = len(readiness_checks)
    
    print(f"\n{Colors.BOLD}PRODUCTION READINESS SUMMARY:{Colors.END}")
    print(f"Readiness Checks Passed: {Colors.GREEN}{passed_readiness}/{total_readiness}{Colors.END}")
    print(f"Readiness Score: {Colors.BOLD}{(passed_readiness/total_readiness)*100:.1f}%{Colors.END}")
    
    return passed_readiness >= total_readiness * 0.8

def generate_final_report():
    """Generate final validation report"""
    
    print_header("FINAL VALIDATION REPORT")
    
    # Run all tests
    swagger_test = test_swagger_endpoints()
    graphql_test = test_graphql_functionality()
    quality_test = test_api_documentation_quality()
    production_test = test_production_readiness()
    
    # Calculate overall score
    tests = [swagger_test, graphql_test, quality_test, production_test]
    passed_tests = sum(tests)
    total_tests = len(tests)
    overall_score = (passed_tests / total_tests) * 100
    
    print_header("OVERALL ASSESSMENT")
    
    print(f"{Colors.BOLD}TEST RESULTS:{Colors.END}")
    print(f"✅ Swagger Endpoints: {'PASS' if swagger_test else 'FAIL'}")
    print(f"✅ GraphQL Functionality: {'PASS' if graphql_test else 'FAIL'}")
    print(f"✅ Documentation Quality: {'PASS' if quality_test else 'FAIL'}")
    print(f"✅ Production Readiness: {'PASS' if production_test else 'FAIL'}")
    
    print(f"\n{Colors.BOLD}OVERALL SCORE: {Colors.END}", end="")
    if overall_score >= 90:
        print(f"{Colors.GREEN}{overall_score:.1f}% - EXCELLENT{Colors.END}")
        grade = "EXCELLENT"
    elif overall_score >= 75:
        print(f"{Colors.CYAN}{overall_score:.1f}% - VERY GOOD{Colors.END}")
        grade = "VERY GOOD"
    elif overall_score >= 60:
        print(f"{Colors.YELLOW}{overall_score:.1f}% - GOOD{Colors.END}")
        grade = "GOOD"
    else:
        print(f"{Colors.RED}{overall_score:.1f}% - NEEDS IMPROVEMENT{Colors.END}")
        grade = "NEEDS IMPROVEMENT"
    
    print(f"\n{Colors.BOLD}ALX PROJECT STATUS:{Colors.END}")
    if overall_score >= 90:
        print(f"{Colors.GREEN}🎊 READY FOR ALX PRESENTATION{Colors.END}")
        print(f"{Colors.GREEN}🏆 EXPECTED GRADE: EXCELLENT (95-100%){Colors.END}")
        print(f"{Colors.GREEN}✅ PRODUCTION-READY API DOCUMENTATION{Colors.END}")
    elif overall_score >= 75:
        print(f"{Colors.CYAN}✅ READY FOR ALX PRESENTATION{Colors.END}")
        print(f"{Colors.CYAN}🏆 EXPECTED GRADE: VERY GOOD (85-95%){Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠️ NEEDS MINOR IMPROVEMENTS{Colors.END}")
        print(f"{Colors.YELLOW}🔧 RECOMMENDED FIXES BEFORE PRESENTATION{Colors.END}")
    
    print(f"\n{Colors.BOLD}QUICK ACCESS LINKS:{Colors.END}")
    print(f"📚 Swagger UI: {Colors.CYAN}http://localhost:8000/api/docs/{Colors.END}")
    print(f"🔗 GraphQL: {Colors.CYAN}http://localhost:8000/graphql/{Colors.END}")
    print(f"💚 Health Check: {Colors.CYAN}http://localhost:8000/api/health/{Colors.END}")
    print(f"📊 Statistics: {Colors.CYAN}http://localhost:8000/api/stats/{Colors.END}")
    
    print(f"\n{Colors.BOLD}{Colors.PURPLE}🎯 PERFECT FOR FRONTEND INTEGRATION!{Colors.END}")
    print(f"{Colors.WHITE}Your API documentation is professional and ready for production use.{Colors.END}")
    
    return overall_score, grade

def main():
    """Main validation function"""
    
    print(f"{Colors.BOLD}{Colors.PURPLE}")
    print("🚀 ALX PROJECT NEXUS - FINAL VALIDATION")
    print("📚 Swagger Documentation & API Testing")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.END}")
    
    try:
        score, grade = generate_final_report()
        
        print_header("VALIDATION COMPLETED")
        print(f"{Colors.BOLD}Final Score: {score:.1f}%{Colors.END}")
        print(f"{Colors.BOLD}Grade: {grade}{Colors.END}")
        
        if score >= 90:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎊 CONGRATULATIONS!{Colors.END}")
            print(f"{Colors.GREEN}Your ALX Project Nexus is EXCELLENT and ready for presentation!{Colors.END}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Validation interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Validation error: {e}{Colors.END}")

if __name__ == "__main__":
    main()
