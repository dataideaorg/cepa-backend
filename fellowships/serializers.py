from rest_framework import serializers
from django.conf import settings
from .models import Cohort, Fellow, CohortProject, CohortEvent, CohortGalleryImage


class FellowSerializer(serializers.ModelSerializer):
    """Serializer for Fellow model"""
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Fellow
        fields = ['id', 'name', 'bio', 'profile_image', 'profile_image_url', 'position', 'linkedin_url',
                  'twitter_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.profile_image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None


class CohortProjectSerializer(serializers.ModelSerializer):
    """Serializer for CohortProject model"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CohortProject
        fields = ['id', 'title', 'description', 'image', 'image_url', 'project_url',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None


class CohortEventSerializer(serializers.ModelSerializer):
    """Serializer for CohortEvent model"""
    class Meta:
        model = CohortEvent
        fields = ['id', 'title', 'description', 'event_date', 'location',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CohortGalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for CohortGalleryImage model"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CohortGalleryImage
        fields = ['id', 'image', 'image_url', 'caption', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None


class CohortListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing cohorts"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Cohort
        fields = ['id', 'name', 'year', 'image', 'image_url', 'slug', 'is_active']

    def get_image_url(self, obj):
        if obj.image:
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None


class CohortDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Cohort with all related data"""
    image_url = serializers.SerializerMethodField()
    fellows = FellowSerializer(many=True, read_only=True)
    projects = CohortProjectSerializer(many=True, read_only=True)
    events = CohortEventSerializer(many=True, read_only=True)
    gallery_images = CohortGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Cohort
        fields = ['id', 'name', 'year', 'image', 'image_url', 'overview', 'is_active',
                  'slug', 'fellows', 'projects', 'events', 'gallery_images',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            base_url = settings.FULL_MEDIA_URL.rstrip('/')
            image_path = obj.image.name.lstrip('/')
            return f"{base_url}/{image_path}"
        return None
