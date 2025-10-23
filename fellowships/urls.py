from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CohortViewSet, FellowViewSet, CohortProjectViewSet,
    CohortEventViewSet, CohortGalleryImageViewSet
)

router = DefaultRouter()
router.register(r'cohorts', CohortViewSet, basename='cohort')
router.register(r'fellows', FellowViewSet, basename='fellow')
router.register(r'projects', CohortProjectViewSet, basename='cohort-project')
router.register(r'events', CohortEventViewSet, basename='cohort-event')
router.register(r'gallery', CohortGalleryImageViewSet, basename='cohort-gallery')

urlpatterns = [
    path('', include(router.urls)),
]
