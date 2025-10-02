from rest_framework import status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Post, Category, Tag, Comment, Like, SavedPost
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer,
    CategorySerializer, TagSerializer, CommentSerializer, CommentCreateSerializer,
    LikeSerializer, SavedPostSerializer
)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class PostViewSet(ModelViewSet):
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'categories', 'tags', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Post.objects.select_related('author').prefetch_related(
            'categories', 'tags', 'comments'
        )
        
        # Non-authenticated users and non-authors can only see published posts
        if not self.request.user.is_authenticated:
            return queryset.filter(status='published')
        
        # Authors can see their own draft posts
        if self.action in ['list']:
            return queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        # Only authors and admins can create posts
        if not self.request.user.is_author_role():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only authors and admins can create posts")
        serializer.save(author=self.request.user)
    
    def get_object(self):
        obj = super().get_object()
        # Only authors can access their draft posts
        if (obj.status == 'draft' and 
            self.request.user != obj.author and 
            not self.request.user.is_admin_role()):
            from django.http import Http404
            raise Http404
        return obj
    
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.can_edit_post(obj):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit your own posts")
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.can_edit_post(obj):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own posts")
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post', 'delete'])
    def like(self, request, slug=None):
        """Like or unlike a post"""
        post = self.get_object()
        like, created = Like.objects.get_or_create(
            user=request.user, 
            post=post,
            defaults={'comment': None}
        )
        
        if not created:
            # Unlike
            like.delete()
            return Response({'liked': False, 'likes_count': post.like_set.filter(post=post).count()})
        
        return Response({'liked': True, 'likes_count': post.like_set.filter(post=post).count()})
    
    @action(detail=True, methods=['post', 'delete'])
    def save(self, request, slug=None):
        """Save or unsave a post"""
        post = self.get_object()
        saved_post, created = SavedPost.objects.get_or_create(
            user=request.user, 
            post=post
        )
        
        if not created:
            # Unsave
            saved_post.delete()
            return Response({'saved': False})
        
        return Response({'saved': True})
    
    @action(detail=False, methods=['get'])
    def saved(self, request):
        """Get current user's saved posts"""
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        saved_posts = SavedPost.objects.filter(user=request.user).select_related('post')
        page = self.paginate_queryset([sp.post for sp in saved_posts])
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        posts = [sp.post for sp in saved_posts]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular posts sorted by likes count"""
        posts = self.get_queryset().annotate(
            likes_count=Count('like', filter=Q(like__post__isnull=False))
        ).order_by('-likes_count', '-created_at')
        
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """Get current user's posts"""
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        posts = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('user', 'post').prefetch_related('replies')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_object(self):
        obj = super().get_object()
        # Only comment authors or admins can update/delete comments
        if (self.action in ['update', 'partial_update', 'destroy'] and 
            obj.user != self.request.user and 
            not self.request.user.is_admin_role()):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You can only modify your own comments")
        return obj
    
    @action(detail=True, methods=['post', 'delete'])
    def like(self, request, pk=None):
        """Like or unlike a comment"""
        comment = self.get_object()
        like, created = Like.objects.get_or_create(
            user=request.user, 
            comment=comment,
            defaults={'post': None}
        )
        
        if not created:
            # Unlike
            like.delete()
            return Response({'liked': False, 'likes_count': comment.like_set.filter(comment=comment).count()})
        
        return Response({'liked': True, 'likes_count': comment.like_set.filter(comment=comment).count()})

class LikeViewSet(ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SavedPostViewSet(ModelViewSet):
    serializer_class = SavedPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SavedPost.objects.filter(user=self.request.user).select_related('post')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
