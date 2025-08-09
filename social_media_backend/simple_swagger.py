"""
Simple Swagger Documentation View - ALX Project Nexus
Quick solution for presentation
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def simple_swagger_docs(request):
    """Simple Swagger documentation page"""
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>ALX Project Nexus - GraphQL API Documentation</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }
        .method { background: #27ae60; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
        .url { font-family: monospace; background: #34495e; color: white; padding: 5px 10px; border-radius: 3px; margin-left: 10px; }
        .description { margin-top: 10px; color: #555; }
        .example { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; font-family: monospace; margin: 10px 0; overflow-x: auto; }
        .feature { background: #e8f5e8; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #27ae60; }
        .auth { background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin: 20px 0; }
        .link { color: #3498db; text-decoration: none; font-weight: bold; }
        .link:hover { text-decoration: underline; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat { background: #3498db; color: white; padding: 15px; border-radius: 5px; text-align: center; flex: 1; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 ALX Project Nexus - GraphQL API Documentation</h1>
        
        <div class="stats">
            <div class="stat">
                <h3>38</h3>
                <p>Total Endpoints</p>
            </div>
            <div class="stat">
                <h3>20</h3>
                <p>Queries</p>
            </div>
            <div class="stat">
                <h3>18</h3>
                <p>Mutations</p>
            </div>
            <div class="stat">
                <h3>JWT</h3>
                <p>Authentication</p>
            </div>
        </div>

        <h2>📚 Main API Endpoints</h2>
        
        <div class="endpoint">
            <span class="method">GET/POST</span>
            <span class="url">/graphql/</span>
            <div class="description">
                <strong>Main GraphQL Endpoint</strong><br>
                Interactive GraphiQL interface for testing all queries and mutations.
                <br><a href="/graphql/" class="link" target="_blank">🔗 Open GraphiQL Interface</a>
            </div>
        </div>

        <div class="endpoint">
            <span class="method">GET</span>
            <span class="url">/admin/</span>
            <div class="description">
                <strong>Django Admin Panel</strong><br>
                Complete administration interface for managing users, posts, and platform data.
                <br><a href="/admin/" class="link" target="_blank">🔗 Open Admin Panel</a>
            </div>
        </div>

        <div class="endpoint">
            <span class="method">GET</span>
            <span class="url">/api/health/</span>
            <div class="description">
                <strong>Health Check</strong><br>
                Monitor API status and system health.
                <br><a href="/api/health/" class="link" target="_blank">🔗 Check Health</a>
            </div>
        </div>

        <div class="endpoint">
            <span class="method">GET</span>
            <span class="url">/api/stats/</span>
            <div class="description">
                <strong>Platform Statistics</strong><br>
                Real-time platform metrics and analytics.
                <br><a href="/api/stats/" class="link" target="_blank">🔗 View Statistics</a>
            </div>
        </div>

        <h2>🔐 Authentication</h2>
        <div class="auth">
            <strong>JWT Token Authentication</strong><br>
            Include in headers: <code>Authorization: JWT &lt;your-token&gt;</code><br>
            Token expiry: 60 minutes | Refresh token expiry: 7 days
        </div>

        <h2>✨ Key Features</h2>
        <div class="feature">👥 <strong>User Management:</strong> Registration, authentication, profiles</div>
        <div class="feature">📝 <strong>Content:</strong> Posts, comments, media uploads</div>
        <div class="feature">❤️ <strong>Social:</strong> Likes, follows, notifications</div>
        <div class="feature">🔍 <strong>Search:</strong> Advanced search and discovery</div>
        <div class="feature">📊 <strong>Analytics:</strong> Real-time statistics and insights</div>
        <div class="feature">🔧 <strong>Admin:</strong> Complete management interface</div>

        <h2>📋 Example GraphQL Operations</h2>

        <h3>User Registration</h3>
        <div class="example">
mutation CreateUser {
  createUser(
    username: "johndoe"
    email: "john@example.com"
    password: "securepassword123"
  ) {
    user {
      id
      username
      email
    }
    success
    errors
  }
}
        </div>

        <h3>User Authentication</h3>
        <div class="example">
mutation Login {
  tokenAuth(
    email: "john@example.com"
    password: "securepassword123"
  ) {
    token
    payload
  }
}
        </div>

        <h3>Create Post</h3>
        <div class="example">
mutation CreatePost {
  createPost(content: "Hello ALX! #GraphQL #Django") {
    post {
      id
      content
      author {
        username
      }
      createdAt
    }
    success
    errors
  }
}
        </div>

        <h3>Get All Posts</h3>
        <div class="example">
query GetPosts {
  allPosts {
    id
    content
    author {
      username
    }
    likesCount
    commentsCount
    createdAt
  }
}
        </div>

        <h3>Like a Post</h3>
        <div class="example">
mutation LikePost {
  likePost(postId: 1) {
    like {
      id
    }
    success
    errors
  }
}
        </div>

        <h2>🌐 Frontend Integration</h2>
        <p>This API is designed for remote frontend consumption. Example JavaScript integration:</p>
        
        <div class="example">
// Authenticate user
const loginResponse = await fetch('http://localhost:8000/graphql/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: `
      mutation {
        tokenAuth(email: "user@example.com", password: "password") {
          token
        }
      }
    `
  })
});

const { data } = await loginResponse.json();
const token = data.tokenAuth.token;

// Use token for authenticated requests
const postsResponse = await fetch('http://localhost:8000/graphql/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `JWT ${token}`
  },
  body: JSON.stringify({
    query: `
      query {
        allPosts {
          id
          content
          author { username }
        }
      }
    `
  })
});
        </div>

        <h2>🎯 Quick Links</h2>
        <p>
            <a href="/graphql/" class="link">🔗 GraphiQL Interface</a> | 
            <a href="/admin/" class="link">🔗 Admin Panel</a> | 
            <a href="/api/health/" class="link">🔗 Health Check</a> | 
            <a href="/api/stats/" class="link">🔗 Statistics</a>
        </p>

        <hr style="margin: 40px 0;">
        <p style="text-align: center; color: #7f8c8d;">
            <strong>ALX Project Nexus</strong> - Modern Social Media Platform API<br>
            Developed by Donald Ahossi - ALX Software Engineering Program 2025<br>
            Production-ready GraphQL API with comprehensive documentation
        </p>
    </div>
</body>
</html>
    """
    
    return HttpResponse(html_content, content_type='text/html')
