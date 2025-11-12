from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    about_page_view,
    HeroSectionViewSet,
    WhoWeAreSectionViewSet,
    StatCardViewSet,
    OurStorySectionViewSet,
    WhatSetsUsApartSectionViewSet,
    CallToActionSectionViewSet
)

router = DefaultRouter()
router.register(r'hero', HeroSectionViewSet, basename='hero')
router.register(r'who-we-are', WhoWeAreSectionViewSet, basename='who-we-are')
router.register(r'stats', StatCardViewSet, basename='stats')
router.register(r'our-story', OurStorySectionViewSet, basename='our-story')
router.register(r'what-sets-us-apart', WhatSetsUsApartSectionViewSet, basename='what-sets-us-apart')
router.register(r'call-to-action', CallToActionSectionViewSet, basename='call-to-action')

urlpatterns = [
    path('page/', about_page_view, name='about-page'),
    path('', include(router.urls)),
]