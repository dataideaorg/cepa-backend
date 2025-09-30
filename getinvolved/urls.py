from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareerOpportunityViewSet, AnnouncementViewSet

router = DefaultRouter()
router.register(r'career', CareerOpportunityViewSet, basename='career')
router.register(r'announcements', AnnouncementViewSet, basename='announcements')

urlpatterns = [
    path('', include(router.urls)),
]
