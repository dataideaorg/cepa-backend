from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, ChatSessionViewSet, ChatViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'sessions', ChatSessionViewSet, basename='session')
router.register(r'', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]
