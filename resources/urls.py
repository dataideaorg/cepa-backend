from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogPostViewSet, NewsArticleViewSet, PublicationViewSet, 
    EventViewSet, HomepageViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'blog', BlogPostViewSet, basename='blog')
router.register(r'news', NewsArticleViewSet, basename='news')
router.register(r'publications', PublicationViewSet, basename='publications')
router.register(r'events', EventViewSet, basename='events')
router.register(r'homepage', HomepageViewSet, basename='homepage')

urlpatterns = [
    path('', include(router.urls)),
]
