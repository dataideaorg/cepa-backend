from rest_framework import serializers
from django.conf import settings
from .models import (
    FocusArea, FocusAreaBasicInformation, FocusAreaObjective, FocusAreaActivity,
    FocusAreaOutcome, FocusAreaPartner, FocusAreaMilestone
)


class FocusAreaObjectiveSerializer(serializers.ModelSerializer):
    """Serializer for FocusAreaObjective model"""

    class Meta:
        model = FocusAreaObjective
        fields = ['id', 'text', 'order']


class FocusAreaActivitySerializer(serializers.ModelSerializer):
    """Serializer for FocusAreaActivity model"""

    class Meta:
        model = FocusAreaActivity
        fields = ['id', 'text', 'order']


class FocusAreaOutcomeSerializer(serializers.ModelSerializer):
    """Serializer for FocusAreaOutcome model"""

    class Meta:
        model = FocusAreaOutcome
        fields = ['id', 'title', 'description', 'metric', 'order']


class FocusAreaPartnerSerializer(serializers.ModelSerializer):
    """Serializer for FocusAreaPartner model"""

    class Meta:
        model = FocusAreaPartner
        fields = ['id', 'name', 'type', 'role', 'order']


class FocusAreaMilestoneSerializer(serializers.ModelSerializer):
    """Serializer for FocusAreaMilestone model"""

    class Meta:
        model = FocusAreaMilestone
        fields = ['id', 'year', 'event', 'order']


class FocusAreaSerializer(serializers.ModelSerializer):
    """Serializer for FocusArea model with all related data"""
    objectives = FocusAreaObjectiveSerializer(many=True, read_only=True)
    activities = FocusAreaActivitySerializer(many=True, read_only=True)
    outcomes = FocusAreaOutcomeSerializer(many=True, read_only=True)
    partners = FocusAreaPartnerSerializer(many=True, read_only=True)
    milestones = FocusAreaMilestoneSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = FocusArea
        fields = [
            'id', 'slug', 'title', 'description', 'image', 'image_url',
            'overview_summary', 'status', 'start_date', 'order',
            'objectives', 'activities', 'outcomes', 'partners', 'milestones',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        """Return absolute URL for the image"""
        if obj.image:
            # Ensure no double slashes in URL
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None


class FocusAreaListSerializer(serializers.ModelSerializer):
    """Simplified serializer for focus area list view"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = FocusArea
        fields = [
            'id', 'slug', 'title', 'description', 'image', 'image_url',
            'status', 'order'
        ]

    def get_image_url(self, obj):
        """Return absolute URL for the image"""
        if obj.image:
            # Ensure no double slashes in URL
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None
