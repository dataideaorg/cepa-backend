from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import BlogPost, NewsArticle, Publication, Event
from .serializers import (
    BlogPostSerializer, NewsArticleSerializer, 
    PublicationSerializer, EventSerializer, HomepageLatestSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BlogPostViewSet(viewsets.ModelViewSet):
    """ViewSet for BlogPost model with full CRUD operations"""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'featured']
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['created_at', 'date', 'title']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured blog posts"""
        featured_posts = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='slug/(?P<slug>[^/.]+)')
    def by_slug(self, request, slug=None):
        """Get blog post by slug"""
        try:
            post = self.queryset.get(slug=slug)
            serializer = self.get_serializer(post)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response(
                {'error': 'Blog post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class NewsArticleViewSet(viewsets.ModelViewSet):
    """ViewSet for NewsArticle model with full CRUD operations"""
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'featured']
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['created_at', 'date', 'title']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured news articles"""
        featured_articles = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_slug(self, request, slug=None):
        """Get news article by slug"""
        try:
            article = self.queryset.get(slug=slug)
            serializer = self.get_serializer(article)
            return Response(serializer.data)
        except NewsArticle.DoesNotExist:
            return Response(
                {'error': 'News article not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class PublicationViewSet(viewsets.ModelViewSet):
    """ViewSet for Publication model with full CRUD operations"""
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'category', 'featured']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'date', 'title']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured publications"""
        featured_publications = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_publications, many=True)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for Event model with full CRUD operations"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'featured']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'date', 'title']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured events"""
        featured_events = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events"""
        upcoming_events = self.queryset.filter(status='upcoming')
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def past(self, request):
        """Get past events"""
        past_events = self.queryset.filter(status='completed')
        serializer = self.get_serializer(past_events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_slug(self, request, slug=None):
        """Get event by slug"""
        try:
            event = self.queryset.get(slug=slug)
            serializer = self.get_serializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response(
                {'error': 'Event not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class HomepageViewSet(viewsets.ViewSet):
    """ViewSet for homepage latest updates"""
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest updates for homepage (featured items from all resource types)"""
        featured_blog_posts = BlogPost.objects.filter(featured=True)[:3]
        featured_news_articles = NewsArticle.objects.filter(featured=True)[:3]
        featured_publications = Publication.objects.filter(featured=True)[:3]
        featured_events = Event.objects.filter(featured=True)[:3]
        
        data = {
            'featured_blog_posts': BlogPostSerializer(featured_blog_posts, many=True).data,
            'featured_news_articles': NewsArticleSerializer(featured_news_articles, many=True).data,
            'featured_publications': PublicationSerializer(featured_publications, many=True).data,
            'featured_events': EventSerializer(featured_events, many=True).data,
        }
        
        return Response(data)
