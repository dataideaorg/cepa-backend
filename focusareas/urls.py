from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FocusAreaViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'focus-areas', FocusAreaViewSet, basename='focus-areas')

urlpatterns = [
    path('', include(router.urls)),
]
