from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Category, Tag, Post, Comment
from django.utils.text import slugify

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: admin/admin123')
        
        author_user, created = User.objects.get_or_create(
            username='author',
            defaults={
                'email': 'author@example.com',
                'role': 'author',
                'first_name': 'John',
                'last_name': 'Author',
            }
        )
        if created:
            author_user.set_password('author123')
            author_user.save()
            self.stdout.write(f'Created author user: author/author123')
        
        reader_user, created = User.objects.get_or_create(
            username='reader',
            defaults={
                'email': 'reader@example.com',
                'role': 'reader',
                'first_name': 'Jane',
                'last_name': 'Reader',
            }
        )
        if created:
            reader_user.set_password('reader123')
            reader_user.save()
            self.stdout.write(f'Created reader user: reader/reader123')
        
        # Create categories
        categories_data = ['Technology', 'Programming', 'Django', 'React', 'Tutorial']
        categories = []
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {cat_name}')
        
        # Create tags
        tags_data = ['python', 'javascript', 'web-development', 'backend', 'frontend', 'api', 'rest']
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag_name}')
        
        # Create posts
        posts_data = [
            {
                'title': 'Getting Started with Django REST Framework',
                'content': '''
# Introduction to Django REST Framework

Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django. In this tutorial, we'll explore the basics of creating RESTful APIs.

## Key Features

- Serialization that supports both ORM and non-ORM data sources
- Authentication policies including OAuth1a and OAuth2
- Customizable everything - just use regular function-based views if you don't need the more powerful features
- Extensive documentation, and great community support

## Getting Started

First, install Django REST Framework:

```bash
pip install djangorestframework
```

Then add it to your INSTALLED_APPS...
                ''',
                'status': 'published',
                'author': author_user,
                'categories': [categories[0], categories[1], categories[2]],
                'tags': [tags[0], tags[5], tags[6]]
            },
            {
                'title': 'Building Modern UIs with React',
                'content': '''
# React: A Modern JavaScript Library

React is a JavaScript library for building user interfaces, particularly web applications. It was developed by Facebook and is now maintained by Meta.

## Why React?

1. **Component-Based**: Build encapsulated components that manage their own state
2. **Declarative**: React makes it painless to create interactive UIs
3. **Learn Once, Write Anywhere**: Develop new features without rewriting existing code

## Getting Started

Create a new React app:

```bash
npx create-react-app my-app
cd my-app
npm start
```
                ''',
                'status': 'published',
                'author': author_user,
                'categories': [categories[0], categories[3], categories[4]],
                'tags': [tags[1], tags[2], tags[4]]
            },
            {
                'title': 'API Design Best Practices',
                'content': '''
# REST API Design Best Practices

When designing RESTful APIs, following established conventions and best practices ensures your API is intuitive, maintainable, and scalable.

## Key Principles

1. **Use HTTP Methods Correctly**
   - GET for retrieval
   - POST for creation
   - PUT for updates
   - DELETE for removal

2. **Resource Naming**
   - Use nouns, not verbs
   - Use plural forms for collections
   - Be consistent

3. **Status Codes**
   - 200 OK for successful GET, PUT, PATCH
   - 201 Created for successful POST
   - 404 Not Found for missing resources
   - 400 Bad Request for invalid input

## Example

```
GET /api/posts/        # Get all posts
GET /api/posts/123/    # Get specific post
POST /api/posts/       # Create new post
PUT /api/posts/123/    # Update post
DELETE /api/posts/123/ # Delete post
```
                ''',
                'status': 'published',
                'author': admin_user,
                'categories': [categories[0], categories[1]],
                'tags': [tags[5], tags[6], tags[2]]
            },
            {
                'title': 'Advanced Django Concepts - Draft',
                'content': '''
# Advanced Django Concepts

This is a draft post about advanced Django concepts including:

- Custom model managers
- Django signals
- Middleware development
- Cache framework
- Database optimization

More content coming soon...
                ''',
                'status': 'draft',
                'author': author_user,
                'categories': [categories[1], categories[2]],
                'tags': [tags[0], tags[2]]
            }
        ]
        
        for post_data in posts_data:
            categories_for_post = post_data.pop('categories', [])
            tags_for_post = post_data.pop('tags', [])
            
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    **post_data,
                    'slug': slugify(post_data['title'])
                }
            )
            
            if created:
                post.categories.set(categories_for_post)
                post.tags.set(tags_for_post)
                self.stdout.write(f'Created post: {post.title}')
                
                # Add some comments
                if post.status == 'published':
                    comment1 = Comment.objects.create(
                        user=reader_user,
                        post=post,
                        text=f"Great article about {post.title.lower()}! Very informative."
                    )
                    
                    # Reply to comment
                    Comment.objects.create(
                        user=post.author,
                        post=post,
                        parent=comment1,
                        text="Thank you! Glad you found it helpful."
                    )
                    
                    self.stdout.write(f'Added comments to: {post.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('Test users created:')
        self.stdout.write('- admin/admin123 (Admin)')
        self.stdout.write('- author/author123 (Author)')
        self.stdout.write('- reader/reader123 (Reader)')