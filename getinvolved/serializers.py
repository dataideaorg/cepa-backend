from rest_framework import serializers
from .models import CareerOpportunity, Announcement


class CareerOpportunitySerializer(serializers.ModelSerializer):
    """Serializer for CareerOpportunity model"""
    
    class Meta:
        model = CareerOpportunity
        fields = [
            'id', 'title', 'type', 'location', 'department', 'description',
            'responsibilities', 'requirements', 'how_to_apply', 'deadline',
            'posted_date', 'status', 'featured', 'image', 'slug',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    """Serializer for Announcement model"""
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'type', 'priority', 'summary', 'content',
            'published_date', 'expiry_date', 'is_active', 'featured',
            'image', 'slug', 'external_link', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
