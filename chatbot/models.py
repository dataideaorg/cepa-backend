from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid
import os


def generate_uuid():
    """Generate a unique UUID string for model primary keys"""
    return str(uuid.uuid4())


def upload_to_chatbot_documents(instance, filename):
    """Generate upload path for chatbot documents"""
    return os.path.join('chatbot', 'documents', filename)


class Document(models.Model):
    """Dedicated documents for chatbot knowledge base"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    name = models.CharField(max_length=255, db_index=True, help_text="Display name for the document")
    file = models.FileField(upload_to=upload_to_chatbot_documents, help_text="Upload PDF document")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the document")
    is_active = models.BooleanField(default=True, help_text="Include in chatbot knowledge base")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.name

    @property
    def file_url(self):
        """Return the full URL to access the file"""
        if self.file:
            # Use FULL_MEDIA_URL if available, otherwise construct from MEDIA_URL
            if hasattr(settings, 'FULL_MEDIA_URL'):
                return settings.FULL_MEDIA_URL + str(self.file)
            return settings.MEDIA_URL + str(self.file)
        return None

    @property
    def file_type(self):
        """Extract file extension from the uploaded file"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower().replace('.', '')
        return 'pdf'


class ChatSession(models.Model):
    """Represents a user's conversation session"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    session_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional title for the session (auto-generated from first query)"
    )
    started_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Session is active")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_activity']
        verbose_name = 'Chat Session'
        verbose_name_plural = 'Chat Sessions'

    def __str__(self):
        return self.session_title or f"Session {self.id[:8]}"


class ChatMessage(models.Model):
    """Individual message in a chat session"""
    MESSAGE_TYPES = [
        ('user', 'User Question'),
        ('assistant', 'AI Response'),
    ]

    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The chat session this message belongs to"
    )
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField(help_text="Message content (query or answer)")

    # AI response metadata (null for user messages)
    source_document_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Which document was used to answer the query"
    )
    source_document_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL to the source document"
    )
    source_document_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Type of source: 'document' or 'publication'"
    )
    confidence = models.FloatField(
        blank=True,
        null=True,
        help_text="AI confidence score (0-1)"
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        indexes = [
            models.Index(fields=['session', 'created_at']),
        ]

    def __str__(self):
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"{self.message_type}: {preview}"
