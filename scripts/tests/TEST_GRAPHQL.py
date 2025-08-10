#!/usr/bin/env python3
"""
Test GraphQL avec requête valide
"""

import requests
import json

def test_graphql():
    """Test GraphQL avec une requête d'introspection"""
    url = "http://localhost:8000/graphql/"
    
    # Requête d'introspection GraphQL
    query = {
        "query": """
        {
            __schema {
                queryType {
                    name
                    fields {
                        name
                        type {
                            name
                        }
                    }
                }
            }
        }
        """
    }
    
    try:
        response = requests.post(url, json=query, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and '__schema' in data['data']:
                schema = data['data']['__schema']
                query_type = schema['queryType']
                print(f"✅ GraphQL Schema OK: {query_type['name']}")
                print(f"✅ Available queries: {len(query_type['fields'])}")
                
                # Afficher quelques queries
                for field in query_type['fields'][:5]:
                    print(f"   - {field['name']}")
                
                return True
            else:
                print("❌ Invalid GraphQL response")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_query():
    """Test une requête GraphQL simple"""
    url = "http://localhost:8000/graphql/"
    
    query = {
        "query": """
        {
            allUsers(first: 1) {
                edges {
                    node {
                        id
                        username
                        email
                    }
                }
            }
        }
        """
    }
    
    try:
        response = requests.post(url, json=query, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                users = data['data']['allUsers']['edges']
                print(f"✅ Users query OK: {len(users)} users found")
                return True
            else:
                print("❌ No data in response")
                return False
        else:
            print(f"❌ Query failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 TEST GRAPHQL DÉTAILLÉ")
    print("=" * 40)
    
    print("\n1. Test Schema Introspection:")
    schema_ok = test_graphql()
    
    print("\n2. Test Simple Query:")
    query_ok = test_simple_query()
    
    print("\n" + "=" * 40)
    if schema_ok and query_ok:
        print("🎊 GraphQL ENTIÈREMENT FONCTIONNEL!")
    elif schema_ok:
        print("✅ GraphQL Schema OK, queries partielles")
    else:
        print("⚠️ GraphQL nécessite vérification")
