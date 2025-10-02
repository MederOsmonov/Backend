from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('author', 'Author'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    social_links = models.JSONField(default=dict, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')

    def __str__(self):
        return self.username
    
    def is_admin_role(self):
        return self.role == 'admin' or self.is_staff or self.is_superuser
    
    def is_author_role(self):
        return self.role in ['author', 'admin'] or self.is_staff or self.is_superuser
    
    def can_edit_post(self, post):
        return self.is_admin_role() or post.author == self
