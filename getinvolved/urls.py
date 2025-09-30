from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareerOpportunityViewSet

router = DefaultRouter()
router.register(r'career', CareerOpportunityViewSet, basename='career')

urlpatterns = [
    path('', include(router.urls)),
]
