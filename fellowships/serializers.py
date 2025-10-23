from rest_framework import serializers
from .models import Cohort, Fellow, CohortProject, CohortEvent, CohortGalleryImage


class FellowSerializer(serializers.ModelSerializer):
    """Serializer for Fellow model"""
    class Meta:
        model = Fellow
        fields = ['id', 'name', 'bio', 'profile_image', 'position', 'linkedin_url',
                  'twitter_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CohortProjectSerializer(serializers.ModelSerializer):
    """Serializer for CohortProject model"""
    class Meta:
        model = CohortProject
        fields = ['id', 'title', 'description', 'image', 'project_url',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CohortEventSerializer(serializers.ModelSerializer):
    """Serializer for CohortEvent model"""
    class Meta:
        model = CohortEvent
        fields = ['id', 'title', 'description', 'event_date', 'location',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CohortGalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for CohortGalleryImage model"""
    class Meta:
        model = CohortGalleryImage
        fields = ['id', 'image', 'caption', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CohortListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing cohorts"""
    class Meta:
        model = Cohort
        fields = ['id', 'name', 'year', 'slug', 'is_active']


class CohortDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Cohort with all related data"""
    fellows = FellowSerializer(many=True, read_only=True)
    projects = CohortProjectSerializer(many=True, read_only=True)
    events = CohortEventSerializer(many=True, read_only=True)
    gallery_images = CohortGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Cohort
        fields = ['id', 'name', 'year', 'overview', 'hero_image', 'is_active',
                  'slug', 'fellows', 'projects', 'events', 'gallery_images',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
