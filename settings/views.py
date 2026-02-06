from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PageHeroImage, CitizensVoiceFeedbackLinks
from .serializers import PageHeroImageSerializer, CitizensVoiceFeedbackLinksSerializer


class CitizensVoiceFeedbackLinksView(APIView):
    """
    GET /api/settings/citizens-voice-feedback/
    Returns the three Google form URLs for the Citizens Voice feedback cards.
    """
    def get(self, request):
        instance = CitizensVoiceFeedbackLinks.objects.first()
        if not instance:
            return Response({
                'ask_mp_form_url': '',
                'comment_bill_form_url': '',
                'feedback_law_form_url': '',
            })
        serializer = CitizensVoiceFeedbackLinksSerializer(instance)
        return Response(serializer.data)


class PageHeroImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Page Hero Images.
    Use /api/settings/page-hero-images/{page_slug}/ to get hero image for a page.
    """
    queryset = PageHeroImage.objects.filter(is_active=True)
    serializer_class = PageHeroImageSerializer
    lookup_field = 'page_slug'

    def retrieve(self, request, *args, **kwargs):
        page_slug = kwargs.get('page_slug')
        try:
            hero_image = PageHeroImage.objects.get(page_slug=page_slug, is_active=True)
            serializer = self.get_serializer(hero_image)
            return Response(serializer.data)
        except PageHeroImage.DoesNotExist:
            return Response(
                {"detail": "No hero image found for this page."},
                status=status.HTTP_404_NOT_FOUND,
            )
