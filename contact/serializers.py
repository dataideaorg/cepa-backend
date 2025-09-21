from rest_framework import serializers
from .models import ContactSubmission

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'responded_at', 'ip_address', 'user_agent', 'is_spam', 'admin_notes']

class ContactSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating contact submissions (excludes admin-only fields)"""
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'organization', 'subject', 'message']
        
    def validate_email(self, value):
        """Validate email format"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Please provide a valid email address.")
        return value.lower()
    
    def validate_name(self, value):
        """Validate name"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Please provide a valid name (at least 2 characters).")
        return value.strip()
    
    def validate_message(self, value):
        """Validate message"""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Please provide a message with at least 10 characters.")
        return value.strip()

class ContactSubmissionListSerializer(serializers.ModelSerializer):
    """Serializer for listing contact submissions (excludes sensitive fields)"""
    response_time_hours = serializers.SerializerMethodField()
    is_old = serializers.SerializerMethodField()
    
    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'organization', 'subject', 'priority', 'status', 
                 'created_at', 'updated_at', 'responded_at', 'response_time_hours', 'is_old']
    
    def get_response_time_hours(self, obj):
        return obj.response_time
    
    def get_is_old(self, obj):
        return obj.is_old

class ContactSubmissionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating contact submissions (admin only)"""
    class Meta:
        model = ContactSubmission
        fields = ['priority', 'status', 'admin_notes', 'is_spam']
    
    def validate_status(self, value):
        """Validate status transitions"""
        if self.instance and self.instance.status == 'closed' and value != 'closed':
            raise serializers.ValidationError("Cannot change status of a closed submission.")
        return value
