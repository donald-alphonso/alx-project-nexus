# 🧪 Testing Guide - ALX Project Nexus

## 🎯 Overview

This guide covers all testing procedures, validation scripts, and quality assurance processes for the ALX Project Nexus social media backend.

---

## 🚀 Quick Testing

### Automated Validation Script
```bash
# Run comprehensive validation
python scripts/tests/VALIDATION_AMELIOREE.py

# Expected Results:
# ✅ Health Check: PASS
# ✅ GraphQL Endpoint: PASS
# ✅ User Creation: PASS
# ✅ Authentication: PASS
# ✅ Documentation: PASS
# 🎯 Success Rate: 80%+ (Excellent)
```

### Health Check Test
```bash
# Quick health verification
curl http://localhost:8000/api/health/

# Expected Response:
{
  "status": "healthy",
  "timestamp": "2025-01-10T12:00:00Z",
  "services": {
    "database": "healthy",
    "cache": "healthy",
    "api": "healthy"
  },
  "version": "1.0.0"
}
```

---

## 🔧 System Testing

### Docker Services Test
```bash
# Check all services status
docker-compose ps

# Expected services:
# - web (Django application)
# - db (PostgreSQL database)
# - redis (Redis cache)
# - celery_worker (Background tasks)
# - celery_beat (Scheduled tasks)
```

### Database Connection Test
```bash
# Test database connectivity
docker-compose exec web python manage.py check

# Expected: "System check identified no issues"
```

### Django Configuration Test
```bash
# Validate Django settings
docker-compose exec web python manage.py check --deploy

# Expected: No critical issues
```

---

## 🌐 API Testing

### GraphQL Endpoint Testing

#### Basic Query Test
```bash
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ allUsers { id username email } }"}'
```

#### Authentication Test
```bash
# Test protected mutation without token (should fail)
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createPost(content: \"Test\") { success } }"}'

# Expected: Authentication error
```

#### Token Authentication Test
```bash
# Get JWT token
TOKEN=$(curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { tokenAuth(username: \"admin@example.com\", password: \"admin123\") { token } }"}' \
  | jq -r '.data.tokenAuth.token')

# Use token for protected operation
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "mutation { createPost(content: \"Test post\") { success post { id } } }"}'
```

### REST Endpoints Testing
```bash
# Test all REST endpoints
curl http://localhost:8000/                    # Project info
curl http://localhost:8000/api/health/         # Health check
curl http://localhost:8000/api/docs/           # API documentation
curl http://localhost:8000/api/swagger/        # Swagger UI
curl http://localhost:8000/api/error-handling/ # Error handling guide
```

---

## 👥 User Management Testing

### User Registration Test
```graphql
mutation {
  createUser(
    username: "testuser_$(date +%s)"
    email: "test_$(date +%s)@example.com"
    password: "testpassword123"
    firstName: "Test"
    lastName: "User"
  ) {
    success
    errors
    user {
      id
      username
      email
      firstName
      lastName
    }
  }
}
```

### User Login Test
```graphql
mutation {
  tokenAuth(
    username: "test@example.com"
    password: "testpassword123"
  ) {
    token
    user {
      id
      username
      email
    }
  }
}
```

### Profile Update Test
```graphql
mutation {
  updateProfile(
    bio: "Updated bio for testing"
    location: "Test City"
    website: "https://test.example.com"
  ) {
    success
    errors
    user {
      bio
      location
      website
    }
  }
}
```

---

## 📝 Content Testing

### Post Creation Tests

#### Text Post Test
```graphql
mutation {
  createPost(
    content: "This is a test post with #testing hashtag"
    visibility: "public"
  ) {
    success
    errors
    post {
      id
      content
      visibility
      createdAt
    }
  }
}
```

#### Media Post Test
```graphql
mutation {
  createPost(
    content: "Test post with image"
    visibility: "public"
    image: "base64_encoded_test_image"
  ) {
    success
    errors
    post {
      id
      content
      image
      hasMedia
      mediaUrl
    }
  }
}
```

### Post Interaction Tests

#### Like Test
```graphql
mutation {
  likePost(postId: "1") {
    success
    errors
    like {
      id
      user {
        username
      }
    }
  }
}
```

#### Comment Test
```graphql
mutation {
  createComment(
    postId: "1"
    content: "This is a test comment"
  ) {
    success
    errors
    comment {
      id
      content
      author {
        username
      }
    }
  }
}
```

---

## 🔒 Security Testing

### Authentication Security Tests

#### Invalid Token Test
```bash
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid_token" \
  -d '{"query": "mutation { createPost(content: \"Test\") { success } }"}'

# Expected: Authentication error
```

#### Expired Token Test
```bash
# Use an expired token
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer expired_token" \
  -d '{"query": "mutation { createPost(content: \"Test\") { success } }"}'

# Expected: Token expired error
```

### Input Validation Tests

#### Invalid Email Test
```graphql
mutation {
  createUser(
    username: "testuser"
    email: "invalid_email"
    password: "password123"
  ) {
    success
    errors
  }
}
# Expected: Email validation error
```

#### Short Password Test
```graphql
mutation {
  createUser(
    username: "testuser"
    email: "test@example.com"
    password: "123"
  ) {
    success
    errors
  }
}
# Expected: Password length error
```

### Permission Tests

#### Unauthorized Access Test
```graphql
# Try to update another user's post
mutation {
  updatePost(
    postId: "1"  # Post owned by different user
    content: "Trying to hack"
  ) {
    success
    errors
  }
}
# Expected: Permission denied
```

---

## 🛡️ Error Handling Testing

### Error Code Testing

#### Validation Error Test
```graphql
mutation {
  createUser(
    username: ""  # Invalid empty username
    email: "test@example.com"
    password: "password123"
  ) {
    success
    errors
  }
}
# Expected: VALIDATION_001 error
```

#### Authentication Error Test
```graphql
mutation {
  createPost(content: "Test")  # No auth token
}
# Expected: AUTH_001 error
```

#### Resource Not Found Test
```graphql
query {
  post(id: "999999")  # Non-existent post
}
# Expected: RESOURCE_001 error
```

### Rate Limiting Test
```bash
# Send multiple rapid requests
for i in {1..100}; do
  curl -X POST http://localhost:8000/graphql/ \
    -H "Content-Type: application/json" \
    -d '{"query": "{ allUsers { id } }"}' &
done

# Expected: Some requests should hit rate limit
```

---

## 📊 Performance Testing

### Load Testing
```bash
# Install Apache Bench (if not available)
# apt-get install apache2-utils

# Test concurrent requests
ab -n 1000 -c 10 http://localhost:8000/api/health/

# Expected: Reasonable response times
```

### Database Performance Test
```bash
# Test database query performance
docker-compose exec web python manage.py shell -c "
import time
from users.models import User
start = time.time()
users = list(User.objects.all())
end = time.time()
print(f'Query time: {end - start:.3f} seconds')
print(f'Users count: {len(users)}')
"
```

### Memory Usage Test
```bash
# Check container memory usage
docker stats --no-stream

# Monitor for memory leaks
```

---

## 🧪 Integration Testing

### Full User Journey Test
```bash
#!/bin/bash
# Complete user journey test script

echo "1. Creating new user..."
USER_RESPONSE=$(curl -s -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"mutation { createUser(username: \\\"testuser_$(date +%s)\\\", email: \\\"test_$(date +%s)@example.com\\\", password: \\\"testpass123\\\") { success user { id username } } }\"}")

echo "2. Getting JWT token..."
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { tokenAuth(username: \"admin@example.com\", password: \"admin123\") { token } }"}')

TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.data.tokenAuth.token')

echo "3. Creating post..."
POST_RESPONSE=$(curl -s -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "mutation { createPost(content: \"Integration test post\") { success post { id } } }"}')

echo "4. Liking post..."
LIKE_RESPONSE=$(curl -s -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "mutation { likePost(postId: \"1\") { success } }"}')

echo "Integration test completed!"
```

---

## 📋 Test Checklists

### Pre-Deployment Checklist
- [ ] All automated tests pass (80%+ success rate)
- [ ] Health check endpoint returns "healthy"
- [ ] All Docker services running
- [ ] Database migrations applied
- [ ] Admin access working
- [ ] GraphQL API functional
- [ ] Authentication system working
- [ ] Error handling active
- [ ] Documentation accessible

### Feature Testing Checklist
- [ ] User registration/login
- [ ] Profile management
- [ ] Post creation (text/media)
- [ ] Social interactions (like/comment/follow)
- [ ] Hashtag system
- [ ] Notification system
- [ ] Search functionality
- [ ] Admin panel access

### Security Testing Checklist
- [ ] JWT authentication enforced
- [ ] Input validation active
- [ ] Rate limiting functional
- [ ] Permission system working
- [ ] Error messages sanitized
- [ ] File upload restrictions
- [ ] SQL injection protection
- [ ] XSS protection

---

## 🔍 Debugging & Troubleshooting

### Common Test Failures

#### Health Check Fails
```bash
# Check service status
docker-compose ps

# Check logs
docker-compose logs web
docker-compose logs db
docker-compose logs redis
```

#### GraphQL Errors
```bash
# Check Django logs
docker-compose logs web | grep ERROR

# Test GraphQL directly
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name } } }"}'
```

#### Authentication Issues
```bash
# Verify user exists and has correct permissions
docker-compose exec web python manage.py shell -c "
from users.models import User
user = User.objects.get(username='admin')
print(f'is_staff: {user.is_staff}')
print(f'is_superuser: {user.is_superuser}')
print(f'is_active: {user.is_active}')
"
```

### Test Environment Reset
```bash
# Reset test environment
docker-compose down
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput

# Verify reset
python scripts/tests/VALIDATION_AMELIOREE.py
```

---

## 📈 Test Reporting

### Automated Test Reports
The validation script generates detailed reports:
- Success/failure rates
- Response times
- Error details
- Recommendations

### Manual Test Documentation
Document manual tests with:
- Test case description
- Expected results
- Actual results
- Pass/fail status
- Screenshots if applicable

### Performance Metrics
Track key metrics:
- Response times
- Throughput
- Error rates
- Resource usage

---

## 🎯 Best Practices

### Testing Guidelines
1. **Test Early:** Run tests during development
2. **Test Often:** Automate testing in CI/CD
3. **Test Thoroughly:** Cover all critical paths
4. **Test Realistically:** Use production-like data

### Test Data Management
1. **Clean Data:** Use fresh test data
2. **Realistic Data:** Mirror production scenarios
3. **Data Privacy:** Don't use real user data
4. **Data Cleanup:** Clean up after tests

### Continuous Testing
1. **Automated Validation:** Run on every deployment
2. **Health Monitoring:** Continuous health checks
3. **Performance Monitoring:** Track metrics over time
4. **Error Monitoring:** Alert on failures

---

*Last updated: January 10, 2025*  
*Testing Guide Version: 1.0.0*
