from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Cohort, Fellow, CohortProject, CohortEvent, CohortGalleryImage
from .serializers import (
    CohortListSerializer, CohortDetailSerializer, FellowSerializer,
    CohortProjectSerializer, CohortEventSerializer, CohortGalleryImageSerializer
)


class CohortViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing cohorts.
    List endpoint returns simplified data, detail endpoint returns full data with related objects.
    """
    queryset = Cohort.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['year', 'is_active']
    search_fields = ['name', 'overview']
    ordering_fields = ['year', 'created_at']
    ordering = ['-year']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CohortDetailSerializer
        return CohortListSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active cohorts"""
        cohorts = self.queryset.filter(is_active=True)
        serializer = CohortListSerializer(cohorts, many=True)
        return Response(serializer.data)


class FellowViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing fellows"""
    queryset = Fellow.objects.all()
    serializer_class = FellowSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cohort']
    search_fields = ['name', 'bio', 'position']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CohortProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing cohort projects"""
    queryset = CohortProject.objects.all()
    serializer_class = CohortProjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cohort']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


class CohortEventViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing cohort events"""
    queryset = CohortEvent.objects.all()
    serializer_class = CohortEventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cohort']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['event_date', 'created_at']
    ordering = ['-event_date']


class CohortGalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing cohort gallery images"""
    queryset = CohortGalleryImage.objects.all()
    serializer_class = CohortGalleryImageSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['cohort']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
