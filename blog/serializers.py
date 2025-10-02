from rest_framework import serializers
from .models import Post, Category, Tag, Comment, Like, SavedPost
from accounts.serializers import UserListSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
        read_only_fields = ('slug',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
        read_only_fields = ('slug',)

class CommentSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'parent', 'text', 'created_at', 'replies')
        read_only_fields = ('id', 'user', 'created_at')
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class PostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing posts"""
    author = UserListSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'image', 'author', 'created_at', 'updated_at', 
                 'status', 'categories', 'tags', 'comments_count', 'likes_count', 'is_saved')
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.like_set.filter(post=obj).count()
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.savedpost_set.filter(user=request.user).exists()
        return False

class PostDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single post view"""
    author = UserListSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'image', 'author', 'created_at', 
                 'updated_at', 'status', 'categories', 'tags', 'comments', 
                 'comments_count', 'likes_count', 'is_liked', 'is_saved')
        read_only_fields = ('slug', 'author', 'created_at', 'updated_at')
    
    def get_comments(self, obj):
        # Only get top-level comments (no parent)
        top_level_comments = obj.comments.filter(parent=None).order_by('-created_at')
        return CommentSerializer(top_level_comments, many=True).data
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.like_set.filter(post=obj).count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_set.filter(user=request.user, post=obj).exists()
        return False
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.savedpost_set.filter(user=request.user).exists()
        return False

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating posts"""
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'status', 'categories', 'tags')

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'parent', 'text')
    
    def validate(self, attrs):
        # If parent is specified, ensure it belongs to the same post
        if attrs.get('parent') and attrs.get('post'):
            if attrs['parent'].post != attrs['post']:
                raise serializers.ValidationError("Parent comment must belong to the same post")
        return attrs

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'comment')
        read_only_fields = ('user',)
    
    def validate(self, attrs):
        # Ensure either post or comment is specified, but not both
        if not attrs.get('post') and not attrs.get('comment'):
            raise serializers.ValidationError("Either post or comment must be specified")
        if attrs.get('post') and attrs.get('comment'):
            raise serializers.ValidationError("Cannot like both post and comment simultaneously")
        return attrs

class SavedPostSerializer(serializers.ModelSerializer):
    post = PostListSerializer(read_only=True)
    
    class Meta:
        model = SavedPost
        fields = ('id', 'post', 'saved_at')
        read_only_fields = ('saved_at',)