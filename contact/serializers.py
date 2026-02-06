from rest_framework import serializers
from .models import Contact, Newsletter, Feedback


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message', 'organization', 'inquiry_type']


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'name', 'email', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Please provide a valid email address")
        return value.lower()

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long")
        return value.strip()