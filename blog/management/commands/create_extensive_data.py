from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Category, Tag, Post, Comment, Like, SavedPost
from django.utils.text import slugify
import random
from faker import Faker
import uuid

User = get_user_model()
fake = Faker(['en_US', 'ru_RU'])

class Command(BaseCommand):
    help = 'Create extensive sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users', type=int, default=50,
            help='Number of users to create (default: 50)'
        )
        parser.add_argument(
            '--posts', type=int, default=200,
            help='Number of posts to create (default: 200)'
        )
        parser.add_argument(
            '--comments', type=int, default=500,
            help='Number of comments to create (default: 500)'
        )

    def handle(self, *args, **options):
        self.stdout.write('🚀 Creating extensive sample data...')
        
        users_count = options['users']
        posts_count = options['posts']
        comments_count = options['comments']
        
        # Clear existing data
        self.stdout.write('🧹 Clearing existing data...')
        Like.objects.all().delete()
        SavedPost.objects.all().delete()
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create admin users
        self.create_admin_users()
        
        # Create categories
        categories = self.create_categories()
        
        # Create tags  
        tags = self.create_tags()
        
        # Create users
        users = self.create_users(users_count)
        
        # Create posts
        posts = self.create_posts(posts_count, users, categories, tags)
        
        # Create comments
        self.create_comments(comments_count, users, posts)
        
        # Create likes
        self.create_likes(users, posts)
        
        # Create saved posts
        self.create_saved_posts(users, posts)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully created sample data!')
        )
        self.stdout.write(f'📊 Statistics:')
        self.stdout.write(f'   👥 Users: {User.objects.count()}')
        self.stdout.write(f'   📝 Posts: {Post.objects.count()}') 
        self.stdout.write(f'   💬 Comments: {Comment.objects.count()}')
        self.stdout.write(f'   ❤️ Likes: {Like.objects.count()}')
        self.stdout.write(f'   🔖 Saved Posts: {SavedPost.objects.count()}')
        self.stdout.write(f'   🏷️ Tags: {Tag.objects.count()}')
        self.stdout.write(f'   📂 Categories: {Category.objects.count()}')
        
        self.stdout.write('\n🔑 Test users:')
        self.stdout.write('   admin/admin123 (Admin)')
        self.stdout.write('   author/author123 (Author)')
        self.stdout.write('   reader/reader123 (Reader)')

    def create_admin_users(self):
        """Create default admin users"""
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'bio': 'System administrator and blog maintainer.'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'👑 Created admin user: admin/admin123')
        
        author_user, created = User.objects.get_or_create(
            username='author',
            defaults={
                'email': 'author@example.com',
                'role': 'author',
                'first_name': 'John',
                'last_name': 'Author',
                'bio': 'Professional tech writer and developer with 10+ years of experience.'
            }
        )
        if created:
            author_user.set_password('author123')
            author_user.save()
            self.stdout.write(f'✍️ Created author user: author/author123')
        
        reader_user, created = User.objects.get_or_create(
            username='reader',
            defaults={
                'email': 'reader@example.com',
                'role': 'reader',
                'first_name': 'Jane',
                'last_name': 'Reader',
                'bio': 'Tech enthusiast and avid reader of programming blogs.'
            }
        )
        if created:
            reader_user.set_password('reader123')
            reader_user.save()
            self.stdout.write(f'📖 Created reader user: reader/reader123')

    def create_categories(self):
        """Create blog categories"""
        categories_data = [
            'Programming', 'Web Development', 'Mobile Development', 'DevOps', 
            'Data Science', 'Machine Learning', 'Artificial Intelligence', 
            'Database', 'Security', 'Cloud Computing', 'UI/UX Design',
            'Software Architecture', 'Testing', 'Career', 'Tutorials',
            'News', 'Reviews', 'Open Source', 'Frameworks', 'Tools'
        ]
        
        categories = []
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'📂 Created category: {cat_name}')
        
        return categories

    def create_tags(self):
        """Create blog tags"""
        tags_data = [
            'python', 'javascript', 'react', 'django', 'flask', 'nodejs', 
            'vue', 'angular', 'typescript', 'css', 'html', 'sass', 'bootstrap',
            'jquery', 'php', 'laravel', 'java', 'spring', 'kotlin', 'swift',
            'ios', 'android', 'flutter', 'react-native', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'terraform', 'ansible', 'jenkins', 'git',
            'github', 'gitlab', 'mongodb', 'postgresql', 'mysql', 'redis',
            'elasticsearch', 'nginx', 'apache', 'linux', 'ubuntu', 'centos',
            'vim', 'vscode', 'pycharm', 'api', 'rest', 'graphql', 'microservices',
            'testing', 'tdd', 'bdd', 'agile', 'scrum', 'design-patterns',
            'algorithms', 'data-structures', 'performance', 'optimization',
            'security', 'authentication', 'oauth', 'jwt', 'blockchain',
            'cryptocurrency', 'ai', 'ml', 'tensorflow', 'pytorch', 'pandas',
            'numpy', 'jupyter', 'data-analysis', 'data-visualization'
        ]
        
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            tags.append(tag)
            if created:
                self.stdout.write(f'🏷️ Created tag: {tag_name}')
        
        return tags

    def create_users(self, count):
        """Create fake users"""
        self.stdout.write(f'👥 Creating {count} users...')
        users = []
        roles = ['reader', 'author', 'reader', 'reader', 'author']  # More readers than authors
        
        for i in range(count):
            username = fake.user_name()
            # Ensure unique username
            while User.objects.filter(username=username).exists():
                username = f"{fake.user_name()}{random.randint(1, 999)}"
            
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='testpass123',
                role=random.choice(roles),
                bio=fake.text(max_nb_chars=200) if random.choice([True, False]) else ''
            )
            users.append(user)
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'   ✅ Created {i + 1}/{count} users')
        
        return users

    def create_posts(self, count, users, categories, tags):
        """Create fake posts"""
        self.stdout.write(f'📝 Creating {count} posts...')
        posts = []
        
        # Authors are users with author or admin role
        authors = [u for u in users if u.role in ['author', 'admin']] + [
            User.objects.get(username='admin'),
            User.objects.get(username='author')
        ]
        
        status_choices = ['published', 'published', 'published', 'draft']  # More published
        
        # Sample tech content templates
        content_templates = [
            self.get_programming_content(),
            self.get_tutorial_content(),
            self.get_review_content(),
            self.get_news_content(),
            self.get_guide_content()
        ]
        
        for i in range(count):
            title = self.generate_tech_title()
            content = random.choice(content_templates).format(
                title=title,
                author=random.choice(authors).get_full_name(),
                tech=random.choice(['Python', 'JavaScript', 'React', 'Django', 'Node.js']),
                concept=fake.word(),
                example=fake.sentence()
            )
            
            post = Post.objects.create(
                title=title,
                slug=slugify(title) + f"-{uuid.uuid4().hex[:8]}",
                content=content,
                author=random.choice(authors),
                status=random.choice(status_choices)
            )
            
            # Add random categories (1-3)
            post_categories = random.sample(categories, random.randint(1, 3))
            post.categories.set(post_categories)
            
            # Add random tags (2-8)
            post_tags = random.sample(tags, random.randint(2, 8))
            post.tags.set(post_tags)
            
            posts.append(post)
            
            if (i + 1) % 20 == 0:
                self.stdout.write(f'   ✅ Created {i + 1}/{count} posts')
        
        return posts

    def create_comments(self, count, users, posts):
        """Create fake comments"""
        self.stdout.write(f'💬 Creating {count} comments...')
        
        published_posts = [p for p in posts if p.status == 'published']
        
        for i in range(count):
            post = random.choice(published_posts)
            user = random.choice(users)
            
            # 80% chance for top-level comment, 20% for reply
            parent = None
            if random.random() < 0.2:
                existing_comments = Comment.objects.filter(post=post, parent=None)
                if existing_comments.exists():
                    parent = random.choice(existing_comments)
            
            comment_text = self.generate_comment_text()
            
            Comment.objects.create(
                user=user,
                post=post,
                parent=parent,
                text=comment_text
            )
            
            if (i + 1) % 50 == 0:
                self.stdout.write(f'   ✅ Created {i + 1}/{count} comments')

    def create_likes(self, users, posts):
        """Create fake likes"""
        self.stdout.write('❤️ Creating likes...')
        
        published_posts = [p for p in posts if p.status == 'published']
        likes_count = 0
        
        # Each user likes 5-20 random posts
        for user in users:
            posts_to_like = random.sample(published_posts, random.randint(5, min(20, len(published_posts))))
            for post in posts_to_like:
                Like.objects.get_or_create(user=user, post=post)
                likes_count += 1
        
        # Also like some comments randomly
        all_comments = list(Comment.objects.all())
        for user in users:
            comments_to_like = random.sample(all_comments, random.randint(2, min(10, len(all_comments))))
            for comment in comments_to_like:
                Like.objects.get_or_create(user=user, comment=comment)
                likes_count += 1
        
        self.stdout.write(f'   ✅ Created {likes_count} likes')

    def create_saved_posts(self, users, posts):
        """Create saved posts"""
        self.stdout.write('🔖 Creating saved posts...')
        
        published_posts = [p for p in posts if p.status == 'published']
        saved_count = 0
        
        # Each user saves 2-10 random posts
        for user in users:
            posts_to_save = random.sample(published_posts, random.randint(2, min(10, len(published_posts))))
            for post in posts_to_save:
                SavedPost.objects.get_or_create(user=user, post=post)
                saved_count += 1
        
        self.stdout.write(f'   ✅ Created {saved_count} saved posts')

    def generate_tech_title(self):
        """Generate realistic tech blog titles"""
        templates = [
            "Getting Started with {tech}",
            "10 Best Practices for {tech} Development", 
            "Building {concept} with {tech}",
            "Complete Guide to {tech} in 2025",
            "{tech} vs Other Frameworks: A Comparison",
            "Advanced {tech} Techniques You Should Know",
            "How to Build a {concept} Using {tech}",
            "Understanding {concept} in {tech}",
            "Top {tech} Libraries You Should Try",
            "Mastering {concept} with {tech}",
            "Common {tech} Mistakes and How to Avoid Them",
            "Why {tech} is Perfect for {concept}",
            "{tech} Tutorial: From Beginner to Expert",
            "Performance Optimization in {tech}",
            "Testing Strategies for {tech} Applications"
        ]
        
        tech_options = [
            'React', 'Django', 'Python', 'JavaScript', 'Node.js', 'Vue.js',
            'Angular', 'TypeScript', 'Docker', 'Kubernetes', 'AWS', 'MongoDB',
            'PostgreSQL', 'GraphQL', 'REST API', 'Machine Learning', 'AI'
        ]
        
        concept_options = [
            'Web Apps', 'APIs', 'Microservices', 'Authentication', 'Databases',
            'User Interfaces', 'Backend Systems', 'Mobile Apps', 'Cloud Solutions',
            'Data Analysis', 'Real-time Features', 'E-commerce Sites', 'Dashboards'
        ]
        
        template = random.choice(templates)
        return template.format(
            tech=random.choice(tech_options),
            concept=random.choice(concept_options)
        )

    def get_programming_content(self):
        return """# {title}

Welcome to this comprehensive guide on programming concepts and best practices.

## Introduction

In this article, we'll explore the fundamentals and advanced techniques that every developer should know. Whether you're a beginner or an experienced programmer, you'll find valuable insights here.

## Key Concepts

### 1. Code Organization
```python
class ExampleClass:
    def __init__(self):
        self.data = []
    
    def process_data(self, input_data):
        # Process the data
        return processed_data
```

### 2. Best Practices
- Write clean, readable code
- Use meaningful variable names
- Add proper documentation
- Implement error handling

## Performance Considerations

When building applications, performance is crucial:

1. **Optimize database queries**
2. **Use caching strategies**  
3. **Minimize resource usage**
4. **Profile your code regularly**

## Conclusion

{example}

Happy coding!
"""

    def get_tutorial_content(self):
        return """# {title}

## Step-by-Step Tutorial

This tutorial will walk you through creating a complete application from scratch.

### Prerequisites
- Basic knowledge of programming
- Development environment setup
- Understanding of web technologies

### Step 1: Project Setup
```bash
mkdir my-project
cd my-project
npm init -y
```

### Step 2: Installation
Install the required dependencies:

```bash
npm install express mongoose cors
npm install -D nodemon
```

### Step 3: Basic Configuration
Create the main application file:

```javascript
const express = require('express');
const app = express();

app.use(express.json());
app.use(cors());

app.get('/', (req, res) => {{
    res.json({{ message: 'Hello World!' }});
}});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {{
    console.log(`Server running on port ${{PORT}}`);
}});
```

### Step 4: Testing
Run your application and test the endpoints.

## Next Steps
- Add authentication
- Implement error handling
- Add data validation
- Deploy to production

{example}
"""

    def get_review_content(self):
        return """# {title}

## Product Review

In this comprehensive review, we'll examine the features, pros, and cons of this technology.

### Overview
This tool has gained significant popularity in the developer community due to its ease of use and powerful features.

### Key Features
- **Feature 1**: Excellent performance
- **Feature 2**: Great documentation
- **Feature 3**: Active community support
- **Feature 4**: Regular updates

### Pros
✅ Easy to learn and use
✅ Great performance
✅ Excellent documentation
✅ Strong community
✅ Regular updates

### Cons
❌ Limited customization options
❌ Learning curve for advanced features
❌ Some compatibility issues

### Rating: 4.5/5 Stars

### Conclusion
Overall, this is an excellent choice for developers looking for a reliable and efficient solution.

{example}
"""

    def get_news_content(self):
        return """# {title}

## Latest Tech News

Breaking news in the world of technology and software development.

### What's New
The latest update brings several exciting features and improvements:

- Enhanced performance
- New API endpoints
- Improved security
- Better error handling
- Updated documentation

### Industry Impact
This development is expected to have a significant impact on:
1. Developer productivity
2. Application performance
3. Security standards
4. Industry best practices

### Community Response
The developer community has responded positively to these changes:

> "This is exactly what we needed. The new features will make our development process much more efficient." - {author}

### Looking Forward
Upcoming features in the roadmap include:
- Advanced analytics
- Machine learning integration
- Enhanced mobile support
- Cloud-native features

{example}
"""

    def get_guide_content(self):
        return """# {title}

## Complete Developer Guide

This comprehensive guide covers everything you need to know about modern development practices.

### Table of Contents
1. Getting Started
2. Core Concepts
3. Advanced Techniques
4. Best Practices
5. Troubleshooting

### Getting Started

Before diving into the technical details, let's set up our development environment:

```bash
# Install required tools
curl -o- https://example.com/install.sh | bash
```

### Core Concepts

Understanding the fundamental concepts is crucial for success:

#### Concept 1: Architecture
Modern applications follow specific architectural patterns for scalability and maintainability.

#### Concept 2: Data Flow
Understanding how data flows through your application is essential.

#### Concept 3: Security
Implementing proper security measures from the beginning.

### Advanced Techniques

Once you master the basics, you can explore advanced techniques:

- Performance optimization
- Caching strategies
- Database optimization
- Code splitting
- Lazy loading

### Best Practices Checklist

- [ ] Code is properly documented
- [ ] Tests are comprehensive
- [ ] Security measures are in place
- [ ] Performance is optimized
- [ ] Error handling is robust

### Troubleshooting Common Issues

**Issue 1**: Application not starting
- Check dependencies
- Verify configuration
- Review logs

**Issue 2**: Performance problems
- Profile the application
- Check database queries
- Optimize critical paths

{example}
"""

    def generate_comment_text(self):
        """Generate realistic comment text"""
        comments = [
            "Great article! Very informative and well-written.",
            "Thanks for sharing this. I learned something new today.",
            "This is exactly what I was looking for. Bookmarked!",
            "Excellent explanation. The examples really helped me understand.",
            "Could you add more details about the implementation?",
            "I followed this tutorial and it worked perfectly. Thanks!",
            "This approach solved my problem. Much appreciated!",
            "Very helpful post. Looking forward to more content like this.",
            "The code examples are clear and easy to follow.",
            "I had the same issue and this fixed it. Thank you!",
            "Interesting perspective. I hadn't thought of it this way.",
            "Well explained! This will definitely help other developers.",
            "Great tutorial! Step-by-step instructions were perfect.",
            "This is a common problem and your solution is elegant.",
            "Thanks for taking the time to write this detailed explanation.",
            "The performance improvements are impressive!",
            "I implemented this in my project and it works great.",
            "Could you also cover the security aspects?",
            "This saved me hours of debugging. Much appreciated!",
            "Clear and concise explanation. Perfect for beginners."
        ]
        return random.choice(comments)