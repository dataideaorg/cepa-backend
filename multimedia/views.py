from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Podcast, Video, GalleryGroup, GalleryImage
from .serializers import (
    PodcastSerializer, VideoSerializer, 
    GalleryGroupSerializer, GalleryGroupListSerializer, GalleryImageSerializer
)


class PodcastViewSet(viewsets.ModelViewSet):
    """ViewSet for Podcast model with full CRUD operations"""
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured podcasts"""
        featured_podcasts = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_podcasts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get podcasts by category"""
        category = request.query_params.get('category')
        if category:
            podcasts = self.queryset.filter(category__icontains=category)
        else:
            podcasts = self.queryset.all()
        
        serializer = self.get_serializer(podcasts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all unique podcast categories"""
        categories = self.queryset.values_list('category', flat=True).distinct()
        return Response(list(categories))


class VideoViewSet(viewsets.ModelViewSet):
    """ViewSet for Video model with full CRUD operations"""
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured videos"""
        featured_videos = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_videos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get videos by category"""
        category = request.query_params.get('category')
        if category:
            videos = self.queryset.filter(category__icontains=category)
        else:
            videos = self.queryset.all()
        
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all unique video categories"""
        categories = self.queryset.values_list('category', flat=True).distinct()
        return Response(list(categories))


class GalleryGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for GalleryGroup model with full CRUD operations"""
    queryset = GalleryGroup.objects.all()
    serializer_class = GalleryGroupSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured gallery groups"""
        featured_groups = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_groups, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        """Get all images for a specific gallery group"""
        gallery_group = self.get_object()
        images = gallery_group.images.all().order_by('order', 'created_at')
        serializer = GalleryImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_image(self, request, pk=None):
        """Add an image to a gallery group"""
        gallery_group = self.get_object()
        serializer = GalleryImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(group=gallery_group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryImageViewSet(viewsets.ModelViewSet):
    """ViewSet for GalleryImage model with full CRUD operations"""
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer

    def get_queryset(self):
        """Filter images by gallery group if specified"""
        queryset = super().get_queryset()
        group_id = self.request.query_params.get('group')
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get images from featured gallery groups"""
        featured_groups = GalleryGroup.objects.filter(featured=True)
        images = self.queryset.filter(group__in=featured_groups)
        serializer = self.get_serializer(images, many=True, context={'request': request})
        return Response(serializer.data)