# 📚 Complete User Guide - ALX Project Nexus

## 🎯 Overview

ALX Project Nexus is a comprehensive social media backend with GraphQL API, featuring user management, posts with media support, social interactions, and enterprise-grade error handling.

---

## 🔑 Authentication & Admin Access

### Admin Panel Access
- **URL:** http://localhost:8000/admin/
- **Login Method:** Email-based authentication
- **Credentials:**
  - **Email:** `admin@example.com` ⚠️ **Use EMAIL, not username**
  - **Password:** `admin123`

### Why Email Login?
The custom User model uses email as the primary authentication field:
```python
USERNAME_FIELD = 'email'  # Login with email
REQUIRED_FIELDS = ['username']
```

### Alternative Admin Users
If needed, you can promote any of the 27 existing users to admin status:
```bash
docker-compose exec web python manage.py shell -c "
from users.models import User
user = User.objects.get(username='testuser1')
user.is_staff = True
user.is_superuser = True
user.save()
"
```

---

## 👥 User Management Features

### User Registration
```graphql
mutation {
  createUser(
    username: "newuser"
    email: "user@example.com"
    password: "securepassword123"
    firstName: "John"
    lastName: "Doe"
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

### User Profile Features
- **Bio:** Up to 500 characters
- **Avatar:** Image upload support
- **Location:** Text field
- **Website:** URL field
- **Birth Date:** Date field
- **Verification Status:** Boolean flag
- **Counters:** Followers, following, posts

### Follow System
```graphql
# Follow a user
mutation {
  followUser(userId: "1") {
    success
    errors
    follow {
      id
      follower {
        username
      }
      following {
        username
      }
    }
  }
}

# Unfollow a user
mutation {
  unfollowUser(userId: "1") {
    success
    errors
  }
}
```

---

## 📝 Post Management with Media Support

### Creating Posts with Media

#### Text Post
```graphql
mutation {
  createPost(
    content: "Hello world! This is my first post."
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

#### Post with Image
```graphql
mutation {
  createPost(
    content: "Check out this amazing sunset!"
    visibility: "public"
    image: "base64_encoded_image_data"
  ) {
    success
    errors
    post {
      id
      content
      image
      mediaUrl
      hasMedia
    }
  }
}
```

#### Post with Video
```graphql
mutation {
  createPost(
    content: "My latest video creation"
    visibility: "followers"
    video: "base64_encoded_video_data"
  ) {
    success
    errors
    post {
      id
      content
      video
      mediaUrl
      hasMedia
    }
  }
}
```

### Media Support Details
- **Image Formats:** JPG, JPEG, PNG, GIF
- **Video Formats:** MP4, AVI, MOV, WMV
- **Upload Path:** 
  - Images: `posts/images/`
  - Videos: `posts/videos/`
- **Validation:** File extension validation included

### Post Visibility Options
- **`public`** - Visible to everyone
- **`followers`** - Visible to followers only
- **`private`** - Visible to author only

### Post Features
- **Content:** Up to 2200 characters
- **Media:** Image OR video (not both)
- **Hashtags:** Automatic detection and linking
- **Pinning:** Pin important posts
- **Counters:** Likes, comments, shares, views

---

## ❤️ Social Interactions

### Liking Posts
```graphql
# Like a post
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

# Unlike a post
mutation {
  unlikePost(postId: "1") {
    success
    errors
  }
}
```

### Commenting System
```graphql
# Add comment
mutation {
  createComment(
    postId: "1"
    content: "Great post!"
  ) {
    success
    errors
    comment {
      id
      content
      author {
        username
      }
      createdAt
    }
  }
}

# Reply to comment
mutation {
  createComment(
    postId: "1"
    content: "I agree!"
    parentId: "5"  # Reply to comment ID 5
  ) {
    success
    errors
    comment {
      id
      content
      parent {
        id
        content
      }
    }
  }
}
```

### Notification System
- **Like notifications:** When someone likes your post
- **Comment notifications:** When someone comments on your post
- **Follow notifications:** When someone follows you
- **Real-time updates:** Notifications appear instantly

---

## 🔍 Content Discovery

### Search Posts
```graphql
query {
  searchPosts(query: "GraphQL") {
    id
    content
    author {
      username
    }
    likesCount
    commentsCount
  }
}
```

### Hashtag System
```graphql
# Get posts by hashtag
query {
  postsByHashtag(hashtag: "technology") {
    id
    content
    author {
      username
    }
    createdAt
  }
}

# Popular hashtags
query {
  popularHashtags {
    name
    postsCount
  }
}
```

### Feed Types
- **Public Feed:** All public posts
- **Personal Feed:** Posts from followed users
- **User Feed:** Specific user's posts

---

## 🛡️ Security & Error Handling

### Authentication Required Operations
All these operations require JWT token:
- Creating posts
- Liking/unliking
- Following/unfollowing
- Commenting
- Updating profile

### JWT Token Usage
```bash
# Get token
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { tokenAuth(username: \"admin@example.com\", password: \"admin123\") { token } }"}'

# Use token in requests
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"query": "mutation { createPost(content: \"Hello!\") { success } }"}'
```

### Error Handling System
The system includes 9 standardized error types:
- `VALIDATION_001` - Invalid input data
- `AUTH_001` - Authentication required
- `AUTH_002` - Permission denied
- `RESOURCE_001` - Resource not found
- `DB_001` - Database error
- `SERVER_001` - Internal server error
- `RATE_001` - Rate limit exceeded

---

## 📊 Admin Dashboard Features

### User Management
- View all users
- Edit user profiles
- Manage user permissions
- View user statistics

### Content Moderation
- Review all posts
- Moderate comments
- Handle reports
- Content analytics

### System Monitoring
- User activity logs
- Error tracking
- Performance metrics
- Health status

---

## 🔧 API Endpoints Reference

### GraphQL Endpoints (38 total)

#### Queries (20)
- `allUsers` - List all users
- `user(id)` - Get specific user
- `me` - Current user profile
- `allPosts` - List all posts
- `post(id)` - Get specific post
- `myPosts` - Current user's posts
- `feed` - Personalized feed
- `searchPosts(query)` - Search posts
- `allComments` - List comments
- `myNotifications` - User notifications
- And 10 more...

#### Mutations (18)
- `createUser` - Register new user
- `updateProfile` - Update user profile
- `createPost` - Create new post
- `updatePost` - Update existing post
- `deletePost` - Delete post
- `likePost` - Like a post
- `createComment` - Add comment
- `followUser` - Follow user
- And 10 more...

### REST Endpoints
- `GET /` - Project information
- `GET /api/health/` - System health check
- `GET /api/docs/` - API documentation
- `GET /api/swagger/` - Interactive Swagger UI
- `GET /api/error-handling/` - Error handling guide
- `GET /admin/` - Django admin panel

---

## 🧪 Testing & Validation

### Health Check
```bash
curl http://localhost:8000/api/health/
```

Expected response:
```json
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

### Automated Testing
```bash
# Run comprehensive validation
python scripts/tests/VALIDATION_AMELIOREE.py

# Expected: 80%+ success rate
```

---

## 🚀 Quick Start Examples

### Complete User Journey
```graphql
# 1. Register user
mutation {
  createUser(username: "demo", email: "demo@example.com", password: "demo123456") {
    success
    user { id username }
  }
}

# 2. Login and get token
mutation {
  tokenAuth(username: "demo@example.com", password: "demo123456") {
    token
  }
}

# 3. Create post with image
mutation {
  createPost(
    content: "My first post with image! #hello #world"
    visibility: "public"
    image: "base64_image_data"
  ) {
    success
    post {
      id
      content
      image
      hasMedia
    }
  }
}

# 4. Follow another user
mutation {
  followUser(userId: "1") {
    success
  }
}

# 5. Like a post
mutation {
  likePost(postId: "1") {
    success
  }
}
```

---

## 📱 Frontend Integration Tips

### File Upload Handling
For image/video uploads in frontend:
1. Convert file to base64
2. Send in GraphQL mutation
3. Handle validation errors
4. Display media URLs from response

### Real-time Features
- Use GraphQL subscriptions for notifications
- Implement WebSocket connections
- Handle connection states

### Error Handling
- Always check `success` field in responses
- Display `errors` array to users
- Implement retry logic for network errors

---

## 🎯 Best Practices

### Security
- Always validate JWT tokens
- Implement rate limiting
- Sanitize user inputs
- Use HTTPS in production

### Performance
- Use pagination for large datasets
- Implement caching strategies
- Optimize database queries
- Monitor API performance

### User Experience
- Provide clear error messages
- Implement loading states
- Handle offline scenarios
- Optimize media loading

---

## 🆘 Troubleshooting

### Common Issues

#### Admin Login Problems
- **Issue:** "Please enter correct email and password"
- **Solution:** Use email (`admin@example.com`) not username

#### GraphQL Authentication Errors
- **Issue:** "Authentication required"
- **Solution:** Include JWT token in Authorization header

#### Media Upload Failures
- **Issue:** File upload errors
- **Solution:** Check file format and size limits

#### Database Connection Issues
- **Issue:** Database errors
- **Solution:** Ensure PostgreSQL container is running

### Getting Help
1. Check health endpoint: `/api/health/`
2. Review error logs in Docker containers
3. Use interactive GraphiQL for testing
4. Consult API documentation at `/api/docs/`

---

*Last updated: January 10, 2025*  
*Version: 1.0.0*
