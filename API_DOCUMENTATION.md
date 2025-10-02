# Blog API Documentation

## Base URL
`http://localhost:8000/api/v1/`

## Authentication Endpoints

### Register
- **POST** `/accounts/auth/register/`
- **Body**: 
```json
{
    "username": "string",
    "email": "string", 
    "password": "string",
    "password_confirm": "string",
    "first_name": "string",
    "last_name": "string"
}
```

### Login
- **POST** `/accounts/auth/login/`
- **Body**:
```json
{
    "username": "string",
    "password": "string"
}
```
- **Response**: Returns access & refresh tokens + user data

### Token Refresh
- **POST** `/accounts/auth/token/refresh/`
- **Body**:
```json
{
    "refresh": "refresh_token"
}
```

### User Profile
- **GET** `/accounts/users/me/` - Get current user profile
- **PUT/PATCH** `/accounts/users/me/` - Update current user profile

## Blog Endpoints

### Posts
- **GET** `/blog/posts/` - List all published posts
- **POST** `/blog/posts/` - Create new post (authors only)
- **GET** `/blog/posts/{slug}/` - Get post details
- **PUT/PATCH** `/blog/posts/{slug}/` - Update post (author or admin)
- **DELETE** `/blog/posts/{slug}/` - Delete post (author or admin)

#### Post Actions
- **POST** `/blog/posts/{slug}/like/` - Like post
- **DELETE** `/blog/posts/{slug}/like/` - Unlike post
- **POST** `/blog/posts/{slug}/save/` - Save post
- **DELETE** `/blog/posts/{slug}/save/` - Unsave post

#### Post Collections
- **GET** `/blog/posts/my_posts/` - Get current user's posts
- **GET** `/blog/posts/saved/` - Get current user's saved posts
- **GET** `/blog/posts/popular/` - Get popular posts (sorted by likes)

### Categories
- **GET** `/blog/categories/` - List categories
- **POST** `/blog/categories/` - Create category (authenticated users)
- **GET** `/blog/categories/{slug}/` - Get category details

### Tags
- **GET** `/blog/tags/` - List tags
- **POST** `/blog/tags/` - Create tag (authenticated users)
- **GET** `/blog/tags/{slug}/` - Get tag details

### Comments
- **GET** `/blog/comments/` - List comments
- **POST** `/blog/comments/` - Create comment (authenticated users)
- **GET** `/blog/comments/{id}/` - Get comment details
- **PUT/PATCH** `/blog/comments/{id}/` - Update comment (author or admin)
- **DELETE** `/blog/comments/{id}/` - Delete comment (author or admin)

#### Comment Actions
- **POST** `/blog/comments/{id}/like/` - Like comment
- **DELETE** `/blog/comments/{id}/like/` - Unlike comment

### Saved Posts
- **GET** `/blog/saved-posts/` - List current user's saved posts
- **POST** `/blog/saved-posts/` - Save a post
- **DELETE** `/blog/saved-posts/{id}/` - Remove saved post

## Query Parameters

### Posts Filtering & Search
- `?search=query` - Search in title and content
- `?status=published` - Filter by status
- `?categories=1,2` - Filter by category IDs
- `?tags=1,2` - Filter by tag IDs
- `?author=1` - Filter by author ID
- `?ordering=-created_at` - Sort by field (created_at, updated_at, title)

### Pagination
- `?page=1` - Page number
- `?page_size=10` - Items per page (default: 10)

## User Roles

### Reader (default)
- Read published posts
- Leave comments
- Like posts/comments
- Save posts

### Author
- All Reader permissions
- Create/edit/delete own posts
- Manage own drafts

### Admin
- All Author permissions  
- Manage all posts
- Manage all comments
- Access Django admin

## Response Format

### Success Response
```json
{
    "data": {...},
    "message": "Success"
}
```

### Error Response
```json
{
    "error": "Error message",
    "details": {...}
}
```

### Paginated Response
```json
{
    "count": 100,
    "next": "url_to_next_page",
    "previous": "url_to_previous_page", 
    "results": [...]
}
```

## Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **500**: Internal Server Error