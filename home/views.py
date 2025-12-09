from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import HeroSlide
from .serializers import HeroSlideSerializer


class HeroSlideViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving hero slides.
    Only active slides are returned by default.
    """
    serializer_class = HeroSlideSerializer

    def get_queryset(self):
        """Return only active hero slides, ordered by order field"""
        return HeroSlide.objects.filter(is_active=True).order_by('order')

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active hero slides"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
