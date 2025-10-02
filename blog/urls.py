from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CategoryViewSet, TagViewSet, CommentViewSet, LikeViewSet, SavedPostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'saved-posts', SavedPostViewSet, basename='savedpost')

urlpatterns = [
    path('', include(router.urls)),
]