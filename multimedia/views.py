from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import (
    Podcast, Video, GalleryGroup, GalleryImage,
    Poll, PollOption, PollVote, XPollEmbed, Trivia, TriviaQuestion,
)
from .serializers import (
    PodcastSerializer, VideoSerializer,
    GalleryGroupSerializer, GalleryGroupListSerializer, GalleryImageSerializer,
    PollSerializer, XPollEmbedSerializer,
    TriviaListSerializer, TriviaDetailSerializer,
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


class PollPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-featured', '-created_at')
    serializer_class = PollSerializer
    pagination_class = PollPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'featured']
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'title']
    ordering = ['-featured', '-created_at']

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and 'vote' in request.path:
            return csrf_exempt(super().dispatch)(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='vote')
    def vote(self, request, pk=None):
        poll = self.get_object()
        if not poll.is_active:
            return Response(
                {'error': 'This poll is not currently active.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        option_id = request.data.get('option_id')
        if option_id is None:
            return Response(
                {'error': 'option_id is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            option_id = int(option_id)
        except (TypeError, ValueError):
            return Response(
                {'error': 'option_id must be a number.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            option = PollOption.objects.get(id=option_id, poll=poll)
        except PollOption.DoesNotExist:
            return Response(
                {'error': 'Invalid option selected.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ip_address = self._get_client_ip(request)
        session_id = (getattr(request.session, 'session_key', None) or '') or request.data.get('session_id', '')
        if not poll.allow_multiple_votes:
            existing = PollVote.objects.filter(
                poll=poll, ip_address=ip_address, session_id=session_id,
            ).first()
            if existing:
                return Response(
                    {'error': 'You have already voted on this poll.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        PollVote.objects.create(
            poll=poll, option=option,
            ip_address=ip_address or None,
            session_id=session_id or '',
        )
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='results')
    def results(self, request, pk=None):
        poll = self.get_object()
        options = PollOption.objects.filter(poll=poll).order_by('order', 'created_at')
        total_votes = poll.total_votes
        results_list = [
            {
                'option_id': opt.id,
                'text': opt.text,
                'vote_count': opt.vote_count,
                'percentage': opt.vote_percentage,
            }
            for opt in options
        ]
        return Response({
            'poll_id': poll.id,
            'poll_title': poll.title,
            'total_votes': total_votes,
            'results': results_list,
        })

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class XPollEmbedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = XPollEmbed.objects.all()
    serializer_class = XPollEmbedSerializer
    pagination_class = None


class TriviaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trivia.objects.filter(is_active=True).order_by('order', '-created_at')
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TriviaDetailSerializer
        return TriviaListSerializer