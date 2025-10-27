from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import FocusArea
from .serializers import FocusAreaSerializer, FocusAreaListSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class FocusAreaViewSet(viewsets.ModelViewSet):
    """ViewSet for FocusArea model with full CRUD operations"""
    queryset = FocusArea.objects.all().select_related('basic_information').prefetch_related(
        'objectives', 'activities', 'outcomes', 'partners', 'milestones', 'resources'
    )
    serializer_class = FocusAreaSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['basic_information__status']
    search_fields = ['title', 'basic_information__overview_summary']
    ordering_fields = ['basic_information__order', 'title', 'created_at']
    ordering = ['basic_information__order', 'title']

    def get_serializer_class(self):
        """Use list serializer for list view, detail serializer for others"""
        if self.action == 'list':
            return FocusAreaListSerializer
        return FocusAreaSerializer

    @action(detail=False, methods=['get'], url_path='slug/(?P<slug>[^/.]+)')
    def by_slug(self, request, slug=None):
        """Get focus area by slug with all related data"""
        try:
            focus_area = self.queryset.get(slug=slug)
            serializer = FocusAreaSerializer(focus_area)
            return Response(serializer.data)
        except FocusArea.DoesNotExist:
            return Response(
                {'error': 'Focus area not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active focus areas"""
        active_focus_areas = self.queryset.filter(basic_information__status='Active')
        serializer = self.get_serializer(active_focus_areas, many=True)
        return Response(serializer.data)
