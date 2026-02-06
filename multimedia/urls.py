from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PodcastViewSet, VideoViewSet, GalleryGroupViewSet, GalleryImageViewSet,
    PollViewSet, XPollEmbedViewSet, TriviaViewSet,
)

router = DefaultRouter()
router.register(r'podcasts', PodcastViewSet, basename='podcast')
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'gallery-groups', GalleryGroupViewSet, basename='gallery-group')
router.register(r'gallery-images', GalleryImageViewSet, basename='gallery-image')
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'x-poll-embeds', XPollEmbedViewSet, basename='xpollembed')
router.register(r'trivia', TriviaViewSet, basename='trivia')

urlpatterns = [
    path('', include(router.urls)),
]
