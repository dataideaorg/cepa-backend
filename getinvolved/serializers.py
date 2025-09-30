from rest_framework import serializers
from .models import CareerOpportunity


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
