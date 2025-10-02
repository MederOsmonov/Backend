# Blog Backend API

Django REST Framework backend for a modern blog application with user roles, posts, comments, likes, and saved posts functionality.

## Features

### User Management
- 🔐 JWT Authentication (Login/Register/Token Refresh)
- 👥 Role-based permissions (Admin, Author, Reader)
- 👤 User profiles with bio, avatar, social links
- 📧 Email-based authentication

### Blog Functionality
- 📝 Posts with rich content, categories, and tags
- 💬 Nested comments (up to 2 levels)
- ❤️ Likes on posts and comments
- 🔖 Save/bookmark posts
- 🔍 Search and filtering
- 📊 Popular posts by likes count

### Content Management
- 📋 Draft/Published status
- 🏷️ Categories and tags
- 🖼️ Image uploads for posts and avatars
- 📱 Auto-generated slugs
- 🔒 Role-based content access

### API Features
- 🚀 RESTful API design
- 📄 Pagination
- 🔍 Search and filtering
- 📋 Comprehensive permissions
- 🛡️ CORS support

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Create sample data (optional)**
```bash
python manage.py create_sample_data
```

5. **Start the development server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication
- `POST /api/v1/accounts/auth/register/` - User registration
- `POST /api/v1/accounts/auth/login/` - User login
- `POST /api/v1/accounts/auth/token/refresh/` - Refresh JWT token
- `GET /api/v1/accounts/users/me/` - Get current user profile
- `PUT /api/v1/accounts/users/me/` - Update current user profile

### Blog
- `GET /api/v1/blog/posts/` - List posts
- `POST /api/v1/blog/posts/` - Create post (authors only)
- `GET /api/v1/blog/posts/{slug}/` - Get post details
- `PUT /api/v1/blog/posts/{slug}/` - Update post (author/admin)
- `DELETE /api/v1/blog/posts/{slug}/` - Delete post (author/admin)

### Post Actions
- `POST /api/v1/blog/posts/{slug}/like/` - Like/unlike post
- `POST /api/v1/blog/posts/{slug}/save/` - Save/unsave post
- `GET /api/v1/blog/posts/my_posts/` - Get user's posts
- `GET /api/v1/blog/posts/saved/` - Get saved posts
- `GET /api/v1/blog/posts/popular/` - Get popular posts

### Categories & Tags
- `GET /api/v1/blog/categories/` - List categories
- `GET /api/v1/blog/tags/` - List tags
- `POST /api/v1/blog/categories/` - Create category
- `POST /api/v1/blog/tags/` - Create tag

### Comments
- `GET /api/v1/blog/comments/` - List comments
- `POST /api/v1/blog/comments/` - Create comment
- `PUT /api/v1/blog/comments/{id}/` - Update comment (author/admin)
- `DELETE /api/v1/blog/comments/{id}/` - Delete comment (author/admin)
- `POST /api/v1/blog/comments/{id}/like/` - Like/unlike comment

## User Roles

### Reader (Default)
- Read published posts
- Leave comments
- Like posts and comments
- Save posts to favorites

### Author
- All Reader permissions
- Create, edit, and delete own posts
- Manage post drafts
- View own post analytics

### Admin
- All Author permissions
- Manage all posts and comments
- Access Django admin panel
- Full CRUD permissions

## Test Users

After running `create_sample_data` command:

- **Admin**: `admin` / `admin123`
- **Author**: `author` / `author123`
- **Reader**: `reader` / `reader123`

## Query Parameters

### Search & Filter
- `?search=query` - Search in post titles and content
- `?categories=1,2` - Filter by category IDs
- `?tags=1,2` - Filter by tag IDs
- `?author=1` - Filter by author ID
- `?status=published` - Filter by status

### Sorting
- `?ordering=-created_at` - Sort by creation date (desc)
- `?ordering=title` - Sort by title (asc)
- `?ordering=-updated_at` - Sort by update date (desc)

### Pagination
- `?page=1` - Page number
- `?page_size=10` - Items per page

## Admin Panel

Access the Django admin at `http://127.0.0.1:8000/admin/`

Use the admin user credentials to manage:
- Users and roles
- Posts and drafts
- Categories and tags
- Comments and moderation
- Site configuration

## Development

### Project Structure
```
Backend/
├── accounts/           # User management app
├── blog/              # Blog functionality app
├── Backend/           # Django project settings
├── media/             # User uploaded files
├── staticfiles/       # Static files
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

### Key Models
- **User**: Extended user model with roles and profile
- **Post**: Blog posts with categories, tags, and status
- **Comment**: Nested comments on posts
- **Like**: Likes on posts and comments
- **SavedPost**: User's saved/bookmarked posts
- **Category/Tag**: Content organization

### Permissions
- Role-based access control
- Object-level permissions
- Custom permission classes
- JWT token authentication

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving (nginx/whitenoise)
4. Configure media file storage (AWS S3/local)
5. Set secure environment variables
6. Use gunicorn/uwsgi for WSGI server

## API Documentation

See `API_DOCUMENTATION.md` for detailed API reference including:
- Complete endpoint list
- Request/response examples
- Authentication requirements
- Error handling
- Status codes

## Support

For questions or issues, please check the documentation or create an issue in the repository.