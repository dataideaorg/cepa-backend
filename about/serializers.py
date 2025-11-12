from rest_framework import serializers
from django.conf import settings
from .models import (
    HeroSection, WhoWeAreSection, WhoWeAreFeature, StatCard,
    OurStorySection, OurStoryCard, WhatSetsUsApartSection,
    WhatSetsUsApartCard, CallToActionSection, TeamMember
)


class HeroSectionSerializer(serializers.ModelSerializer):
    """Serializer for Hero Section"""
    hero_image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSection
        fields = ['id', 'title', 'description', 'hero_image', 'hero_image_url', 'updated_at']

    def get_hero_image_url(self, obj):
        """Return absolute URL for the hero image"""
        if obj.hero_image:
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.hero_image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None


class WhoWeAreFeatureSerializer(serializers.ModelSerializer):
    """Serializer for Who We Are Feature"""

    class Meta:
        model = WhoWeAreFeature
        fields = ['id', 'icon', 'title', 'description', 'order']


class WhoWeAreSectionSerializer(serializers.ModelSerializer):
    """Serializer for Who We Are Section"""
    features = WhoWeAreFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = WhoWeAreSection
        fields = ['id', 'title', 'description', 'features', 'updated_at']


class StatCardSerializer(serializers.ModelSerializer):
    """Serializer for Stat Card"""

    class Meta:
        model = StatCard
        fields = ['id', 'value', 'label', 'order', 'updated_at']


class OurStoryCardSerializer(serializers.ModelSerializer):
    """Serializer for Our Story Card"""

    class Meta:
        model = OurStoryCard
        fields = ['id', 'icon', 'title', 'description', 'order']


class OurStorySectionSerializer(serializers.ModelSerializer):
    """Serializer for Our Story Section"""
    cards = OurStoryCardSerializer(many=True, read_only=True)

    class Meta:
        model = OurStorySection
        fields = ['id', 'title', 'description', 'cards', 'updated_at']


class WhatSetsUsApartCardSerializer(serializers.ModelSerializer):
    """Serializer for What Sets Us Apart Card"""

    class Meta:
        model = WhatSetsUsApartCard
        fields = ['id', 'title', 'description', 'order']


class WhatSetsUsApartSectionSerializer(serializers.ModelSerializer):
    """Serializer for What Sets Us Apart Section"""
    cards = WhatSetsUsApartCardSerializer(many=True, read_only=True)

    class Meta:
        model = WhatSetsUsApartSection
        fields = ['id', 'title', 'description', 'cards', 'updated_at']


class CallToActionSectionSerializer(serializers.ModelSerializer):
    """Serializer for Call to Action Section"""

    class Meta:
        model = CallToActionSection
        fields = ['id', 'title', 'description', 'updated_at']


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for Team Member"""
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'role', 'profile_image', 'profile_image_url', 'linkedin_url', 'order', 'is_active', 'updated_at']

    def get_profile_image_url(self, obj):
        """Return absolute URL for the profile image"""
        if obj.profile_image:
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.profile_image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None


class AboutPageSerializer(serializers.Serializer):
    """Combined serializer for all About page sections"""
    hero = HeroSectionSerializer(read_only=True)
    who_we_are = WhoWeAreSectionSerializer(read_only=True)
    stats = StatCardSerializer(many=True, read_only=True)
    our_story = OurStorySectionSerializer(read_only=True)
    what_sets_us_apart = WhatSetsUsApartSectionSerializer(read_only=True)
    call_to_action = CallToActionSectionSerializer(read_only=True)
    team = TeamMemberSerializer(many=True, read_only=True)