from rest_framework import serializers
from .models import Contact, Newsletter

class ContactSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Contact
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 
            'organization', 'subject', 'message', 'inquiry_type', 
            'created_at', 'updated_at', 'is_responded'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_responded']
    
    def validate_email(self, value):
        """Validate email format"""
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value.lower()
    
    def validate(self, data):
        """Additional validation"""
        if not data.get('first_name') or not data.get('first_name').strip():
            raise serializers.ValidationError({'first_name': 'First name is required.'})
        
        if not data.get('last_name') or not data.get('last_name').strip():
            raise serializers.ValidationError({'last_name': 'Last name is required.'})
            
        if not data.get('subject') or not data.get('subject').strip():
            raise serializers.ValidationError({'subject': 'Subject is required.'})
            
        if not data.get('message') or not data.get('message').strip():
            raise serializers.ValidationError({'message': 'Message is required.'})
        
        return data

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = [
            'id', 'email', 'first_name', 'last_name', 
            'is_active', 'subscribed_at', 'unsubscribed_at'
        ]
        read_only_fields = ['id', 'subscribed_at', 'unsubscribed_at']
    
    def validate_email(self, value):
        """Validate email format and uniqueness"""
        if not value:
            raise serializers.ValidationError("Email is required.")
        
        email = value.lower()
        
        # Check if email already exists and is active
        if Newsletter.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError("This email is already subscribed to our newsletter.")
        
        return email
    
    def create(self, validated_data):
        """Create or reactivate newsletter subscription"""
        email = validated_data['email']
        
        # Check if email exists but is inactive
        try:
            newsletter = Newsletter.objects.get(email=email)
            if not newsletter.is_active:
                # Reactivate subscription
                newsletter.is_active = True
                newsletter.first_name = validated_data.get('first_name', newsletter.first_name)
                newsletter.last_name = validated_data.get('last_name', newsletter.last_name)
                newsletter.unsubscribed_at = None
                newsletter.save()
                return newsletter
        except Newsletter.DoesNotExist:
            pass
        
        # Create new subscription
        return super().create(validated_data)
