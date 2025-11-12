from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    HeroSection, WhoWeAreSection, StatCard,
    OurStorySection, WhatSetsUsApartSection, CallToActionSection, TeamMember
)
from .serializers import (
    HeroSectionSerializer, WhoWeAreSectionSerializer, StatCardSerializer,
    OurStorySectionSerializer, WhatSetsUsApartSectionSerializer,
    CallToActionSectionSerializer, TeamMemberSerializer, AboutPageSerializer
)


@api_view(['GET'])
def about_page_view(request):
    """
    Get all about page content in a single request
    """
    try:
        # Get all sections (or None if they don't exist)
        hero = HeroSection.objects.first()
        who_we_are = WhoWeAreSection.objects.prefetch_related('features').first()
        stats = StatCard.objects.all().order_by('order')
        our_story = OurStorySection.objects.prefetch_related('cards').first()
        what_sets_us_apart = WhatSetsUsApartSection.objects.prefetch_related('cards').first()
        call_to_action = CallToActionSection.objects.first()
        team = TeamMember.objects.filter(is_active=True).order_by('order')

        # Serialize all sections
        data = {
            'hero': HeroSectionSerializer(hero).data if hero else None,
            'who_we_are': WhoWeAreSectionSerializer(who_we_are).data if who_we_are else None,
            'stats': StatCardSerializer(stats, many=True).data,
            'our_story': OurStorySectionSerializer(our_story).data if our_story else None,
            'what_sets_us_apart': WhatSetsUsApartSectionSerializer(what_sets_us_apart).data if what_sets_us_apart else None,
            'call_to_action': CallToActionSectionSerializer(call_to_action).data if call_to_action else None,
            'team': TeamMemberSerializer(team, many=True).data,
        }

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class HeroSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Hero Section"""
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer


class WhoWeAreSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Who We Are Section"""
    queryset = WhoWeAreSection.objects.prefetch_related('features').all()
    serializer_class = WhoWeAreSectionSerializer


class StatCardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Stat Cards"""
    queryset = StatCard.objects.all().order_by('order')
    serializer_class = StatCardSerializer


class OurStorySectionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Our Story Section"""
    queryset = OurStorySection.objects.prefetch_related('cards').all()
    serializer_class = OurStorySectionSerializer


class WhatSetsUsApartSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for What Sets Us Apart Section"""
    queryset = WhatSetsUsApartSection.objects.prefetch_related('cards').all()
    serializer_class = WhatSetsUsApartSectionSerializer


class CallToActionSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Call to Action Section"""
    queryset = CallToActionSection.objects.all()
    serializer_class = CallToActionSectionSerializer


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Team Members"""
    queryset = TeamMember.objects.filter(is_active=True).order_by('order')
    serializer_class = TeamMemberSerializer