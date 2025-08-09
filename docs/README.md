# ALX Project Nexus - Social Media Feed Backend

A scalable social media backend built with Django, PostgreSQL, and GraphQL.

## Technologies Used

- **Django 5.1**: Web framework
- **PostgreSQL 16**: Database
- **GraphQL (Graphene)**: API layer
- **Celery 5.4**: Background tasks
- **Redis 7.2**: Message broker and cache
- **Docker**: Containerization
- **JWT**: Authentication

## Project Structure

```
social_media_backend/
├── users/              # User management and authentication
├── posts/              # Posts, comments, and hashtags
├── interactions/       # Likes, shares, bookmarks, notifications
├── social_media_backend/  # Main project settings
├── docker-compose.yml  # Docker services configuration
├── Dockerfile         # Application container
├── entrypoint.sh      # Docker startup script
└── requirements.txt   # Python dependencies
```

## Key Features

### Core Functionality
- **User Management**: Registration, authentication, profiles, follow system
- **Posts**: Create, edit, delete posts with hashtag support
- **Comments**: Nested comments system
- **Interactions**: Like, share, bookmark posts and comments
- **Notifications**: Real-time notification system
- **Reports**: User reporting system for content moderation

### Technical Features
- **JWT Authentication**: Secure GraphQL authentication
- **GraphQL API**: Complete CRUD operations with queries and mutations
- **Background Tasks**: Celery for async processing
- **Database Optimization**: Indexed fields and optimized queries
- **Docker Support**: Full containerization
- **Admin Interface**: Django admin for content management

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd alx-project-nexus
```

### 2. Environment Setup
The project uses `.env.docker` for Docker environment variables. All necessary variables are pre-configured.

### 3. Build and Run
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 4. Access the Application
- **GraphQL Playground**: http://localhost:8000/graphql/
- **Django Admin**: http://localhost:8000/admin/
  - Username: `admin`
  - Password: `admin123`

### 5. Services Included
- **Web Application**: Django server on port 8000
- **PostgreSQL**: Database on port 5432
- **Redis**: Cache and message broker on port 6379
- **Celery Worker**: Background task processing
- **Celery Beat**: Scheduled tasks

## Development Setup (Local)

### 1. Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create sample data
python manage.py create_sample_data --users 15 --posts 75
```

### 3. Run Development Server
```bash
python manage.py runserver
```

## Database Schema

### Core Models
- **User**: Extended user model with profile information
- **Follow**: User following relationships
- **Post**: User posts with content and metadata
- **Comment**: Nested comments on posts
- **Hashtag**: Hashtag system with trending support
- **Like**: Generic likes for posts and comments
- **Share**: Post sharing system
- **Bookmark**: User bookmarks
- **Notification**: Real-time notifications
- **Report**: Content reporting system

## GraphQL API

### Authentication
```graphql
# Login
mutation {
  tokenAuth(username: "admin", password: "admin123") {
    token
    refreshToken
  }
}
```

### Sample Queries
```graphql
# Get all posts
query {
  allPosts {
    id
    content
    author {
      username
    }
    likesCount
    createdAt
  }
}

# Get user profile
query {
  userProfile(username: "admin") {
    id
    username
    bio
    postsCount
    followersCount
  }
}
```

### Sample Mutations
```graphql
# Create a post
mutation {
  createPost(content: "Hello World! #django #graphql") {
    post {
      id
      content
      author {
        username
      }
    }
  }
}

# Like a post
mutation {
  likePost(postId: 1) {
    success
    message
  }
}
```

## Background Tasks

The application uses Celery for background processing:

- **Notifications**: Async notification delivery
- **Cleanup**: Periodic cleanup of old data
- **Trending**: Update trending hashtags

## Security Features

- JWT token authentication
- CORS configuration
- Environment variable protection
- SQL injection prevention
- XSS protection
- CSRF protection

## Performance Optimizations

- Database indexing on frequently queried fields
- Query optimization with select_related and prefetch_related
- Redis caching for sessions and Celery
- Efficient GraphQL resolvers
- Static file serving with Whitenoise

## Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

### Docker Production
1. Update environment variables in `.env.docker`
2. Set `DEBUG=False`
3. Configure proper `SECRET_KEY`
4. Set up SSL/HTTPS
5. Configure domain in `ALLOWED_HOSTS`

### Cloud Deployment
The application is ready for deployment on:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

## Development Challenges & Solutions

### 1. Database Design
**Challenge**: Creating efficient relationships between users, posts, and interactions
**Solution**: Used Generic Foreign Keys for flexible relationships and proper indexing

### 2. GraphQL Integration
**Challenge**: Implementing complex queries and mutations with authentication
**Solution**: Used Graphene-Django with JWT integration and custom decorators

### 3. Real-time Features
**Challenge**: Managing notifications and background tasks
**Solution**: Implemented Celery with Redis for async processing

### 4. Scalability
**Challenge**: Designing for high-traffic scenarios
**Solution**: Database optimization, caching, and containerization

## Best Practices Implemented

- **Clean Architecture**: Separation of concerns with Django apps
- **Code Quality**: Consistent formatting and documentation
- **Security**: JWT authentication and environment variables
- **Performance**: Database optimization and caching
- **DevOps**: Docker containerization and easy deployment
- **Testing**: Comprehensive test coverage
- **Documentation**: Clear API documentation and code comments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Author

Developed as part of the ALX Backend Professional Development program.

---

**Happy Coding! **

Welcome to **alx-project-nexus**, a GitHub repository that compiles all of my key learnings from the **ProDev Backend Engineering** program.

## About the Program

The **ProDev Backend Engineering** program enabled me to develop a strong foundation in building and managing web applications on the server side. I learned how to design APIs that are efficient, secure, maintainable, and scalable using industry-standard tools and best practices.

---

## Key Technologies Covered

- **Python** – Primary programming language
- **Django** – Python web framework for building robust applications
- **REST APIs** – Interface for data exchange between systems
- **GraphQL** – A flexible alternative to REST for API communication
- **Docker** – Containerization tool for managing development environments
- **CI/CD** – Continuous Integration and Deployment automation (e.g., GitHub Actions)

---

## Major Concepts

- **Relational Database Design** (modeling, normalization)
- **Asynchronous Programming** – Optimizing performance
- **Caching Strategies** – Improving API response times

---

## Challenges Faced

- API security issues → Solved using authentication tokens and permission handling
- Docker configuration difficulties → Addressed by improving understanding of Dockerfiles and docker-compose
- CI/CD not triggering correctly → Fixed by correcting the GitHub Actions YAML configuration

---

## Best Practices Adopted

- Clear and up-to-date documentation (README, code comments)
- Consistent naming conventions (snake_case, camelCase)
- Clean error handling (try/except blocks, logging)
- Unit testing for code reliability

---

## Collaboration

This project also serves as an opportunity to collaborate with other learners in the program:

- **Backend learners**: Exchange ideas and provide technical support
- **Frontend learners**: Integrate their frontend with our backend API

**Collaboration space**: Discord channel `#ProDevProjectNexus`

---

## Cloning the Repository

```bash
git clone https://github.com/your-username/alx-project-nexus.git
cd alx-project-nexus
```
