from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import models
from .models import CareerOpportunity, Announcement
from .serializers import CareerOpportunitySerializer, AnnouncementSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CareerOpportunityViewSet(viewsets.ModelViewSet):
    """ViewSet for CareerOpportunity model with full CRUD operations"""
    queryset = CareerOpportunity.objects.all()
    serializer_class = CareerOpportunitySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'featured', 'location']
    search_fields = ['title', 'description', 'requirements', 'responsibilities']
    ordering_fields = ['created_at', 'posted_date', 'deadline', 'title']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured career opportunities"""
        featured_opportunities = self.queryset.filter(featured=True, status='open')
        serializer = self.get_serializer(featured_opportunities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def open(self, request):
        """Get open career opportunities"""
        open_opportunities = self.queryset.filter(status='open')
        serializer = self.get_serializer(open_opportunities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get career opportunities by type"""
        opportunity_type = request.query_params.get('type', None)
        if opportunity_type:
            opportunities = self.queryset.filter(type=opportunity_type, status='open')
            serializer = self.get_serializer(opportunities, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Type parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'], url_path='slug/(?P<slug>[^/.]+)')
    def by_slug(self, request, slug=None):
        """Get career opportunity by slug"""
        try:
            opportunity = self.queryset.get(slug=slug)
            serializer = self.get_serializer(opportunity)
            return Response(serializer.data)
        except CareerOpportunity.DoesNotExist:
            return Response(
                {'error': 'Career opportunity not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class AnnouncementViewSet(viewsets.ModelViewSet):
    """ViewSet for Announcement model with full CRUD operations"""
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'priority', 'is_active', 'featured']
    search_fields = ['title', 'summary', 'content']
    ordering_fields = ['created_at', 'published_date', 'priority', 'title']
    ordering = ['-published_date', '-created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured announcements"""
        featured_announcements = self.queryset.filter(featured=True, is_active=True)
        serializer = self.get_serializer(featured_announcements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active announcements (not expired)"""
        today = timezone.now().date()
        active_announcements = self.queryset.filter(is_active=True).filter(
            models.Q(expiry_date__isnull=True) | models.Q(expiry_date__gte=today)
        )
        serializer = self.get_serializer(active_announcements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def urgent(self, request):
        """Get urgent announcements"""
        today = timezone.now().date()
        urgent_announcements = self.queryset.filter(
            priority='urgent', 
            is_active=True
        ).filter(
            models.Q(expiry_date__isnull=True) | models.Q(expiry_date__gte=today)
        )
        serializer = self.get_serializer(urgent_announcements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get announcements by type"""
        announcement_type = request.query_params.get('type', None)
        if announcement_type:
            announcements = self.queryset.filter(type=announcement_type, is_active=True)
            serializer = self.get_serializer(announcements, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Type parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'], url_path='slug/(?P<slug>[^/.]+)')
    def by_slug(self, request, slug=None):
        """Get announcement by slug"""
        try:
            announcement = self.queryset.get(slug=slug)
            serializer = self.get_serializer(announcement)
            return Response(serializer.data)
        except Announcement.DoesNotExist:
            return Response(
                {'error': 'Announcement not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
