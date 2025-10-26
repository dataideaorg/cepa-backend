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


class FocusAreaBasicInformationSerializer(serializers.ModelSerializer):
    """Serializer for FocusAreaBasicInformation model"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = FocusAreaBasicInformation
        fields = ['image', 'image_url', 'overview_summary', 'status', 'start_date', 'order', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        """Return absolute URL for the image"""
        if obj.image:
            # Ensure no double slashes in URL
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None


class FocusAreaSerializer(serializers.ModelSerializer):
    """Serializer for FocusArea model with all related data"""
    objectives = FocusAreaObjectiveSerializer(many=True, read_only=True)
    activities = FocusAreaActivitySerializer(many=True, read_only=True)
    outcomes = FocusAreaOutcomeSerializer(many=True, read_only=True)
    partners = FocusAreaPartnerSerializer(many=True, read_only=True)
    milestones = FocusAreaMilestoneSerializer(many=True, read_only=True)

    # Flatten basic_information fields
    image = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    overview_summary = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = FocusArea
        fields = [
            'id', 'slug', 'title', 'image', 'image_url',
            'overview_summary', 'status', 'start_date', 'order',
            'objectives', 'activities', 'outcomes', 'partners', 'milestones',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_image(self, obj):
        """Get image from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.image.name if obj.basic_information.image else None
        return None

    def get_image_url(self, obj):
        """Return absolute URL for the image from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information and obj.basic_information.image:
            # Ensure no double slashes in URL
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.basic_information.image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None

    def get_overview_summary(self, obj):
        """Get overview_summary from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.overview_summary
        return ""

    def get_status(self, obj):
        """Get status from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.status
        return "Active"

    def get_start_date(self, obj):
        """Get start_date from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.start_date
        return ""

    def get_order(self, obj):
        """Get order from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.order
        return 0

    def get_updated_at(self, obj):
        """Get updated_at from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.updated_at
        return obj.created_at


class FocusAreaListSerializer(serializers.ModelSerializer):
    """Simplified serializer for focus area list view"""
    image = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    overview_summary = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()

    class Meta:
        model = FocusArea
        fields = [
            'id', 'slug', 'title', 'overview_summary', 'image', 'image_url',
            'status', 'order'
        ]

    def get_image(self, obj):
        """Get image from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.image.name if obj.basic_information.image else None
        return None

    def get_image_url(self, obj):
        """Return absolute URL for the image from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information and obj.basic_information.image:
            # Ensure no double slashes in URL
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.basic_information.image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None

    def get_overview_summary(self, obj):
        """Get overview_summary from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.overview_summary
        return ""

    def get_status(self, obj):
        """Get status from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.status
        return "Active"

    def get_order(self, obj):
        """Get order from basic_information"""
        if hasattr(obj, 'basic_information') and obj.basic_information:
            return obj.basic_information.order
        return 0
