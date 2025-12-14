from rest_framework import serializers
from django.conf import settings
from .models import Document, ChatSession, ChatMessage


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model"""
    file_url = serializers.SerializerMethodField()
    file_type = serializers.CharField(read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'name', 'file', 'file_url', 'file_type',
            'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        """Return full URL for file access"""
        if obj.file:
            if hasattr(settings, 'FULL_MEDIA_URL'):
                return settings.FULL_MEDIA_URL + str(obj.file)
            return settings.MEDIA_URL + str(obj.file)
        return None


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for ChatMessage model"""

    class Meta:
        model = ChatMessage
        fields = [
            'id', 'message_type', 'content',
            'source_document_name', 'source_document_url',
            'source_document_type', 'confidence', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    """Serializer for ChatSession model (list view)"""
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = [
            'id', 'session_title', 'started_at', 'last_activity',
            'is_active', 'message_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'started_at', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        """Return the number of messages in the session"""
        return obj.messages.count()


class ChatSessionDetailSerializer(serializers.ModelSerializer):
    """Serializer for ChatSession model (detail view with messages)"""
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = [
            'id', 'session_title', 'started_at', 'last_activity',
            'is_active', 'messages', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'started_at', 'created_at', 'updated_at']


class ChatQuerySerializer(serializers.Serializer):
    """Serializer for chat query requests"""
    query = serializers.CharField(required=True, help_text="User's question")
    session_id = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Existing session ID (optional - creates new session if not provided)"
    )


class ChatResponseSerializer(serializers.Serializer):
    """Serializer for chat response"""
    session_id = serializers.CharField()
    user_message_id = serializers.CharField()
    assistant_message_id = serializers.CharField()
    answer = serializers.CharField()
    source_document_name = serializers.CharField()
    source_document_url = serializers.CharField()
    source_document_type = serializers.CharField()
    confidence = serializers.FloatField()
    timestamp = serializers.DateTimeField()
