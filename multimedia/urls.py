from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PodcastViewSet, VideoViewSet, GalleryGroupViewSet, GalleryImageViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'podcasts', PodcastViewSet, basename='podcast')
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'gallery-groups', GalleryGroupViewSet, basename='gallery-group')
router.register(r'gallery-images', GalleryImageViewSet, basename='gallery-image')

urlpatterns = [
    path('', include(router.urls)),
]
