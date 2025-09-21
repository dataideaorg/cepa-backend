from django.db import models
from django.utils import timezone
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class ContactSubmission(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('partnership', 'Partnership'),
        ('media', 'Media Inquiry'),
        ('donation', 'Donation'),
        ('volunteer', 'Volunteer'),
        ('fellowship', 'Fellowship Program'),
        ('event', 'Event Information'),
        ('research', 'Research Collaboration'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    ]

    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    is_spam = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    def mark_as_responded(self):
        """Mark the submission as responded to"""
        self.status = 'responded'
        self.responded_at = timezone.now()
        self.save()

    def mark_as_closed(self):
        """Mark the submission as closed"""
        self.status = 'closed'
        self.save()

    @property
    def is_old(self):
        """Check if submission is older than 7 days"""
        return (timezone.now() - self.created_at).days > 7

    @property
    def response_time(self):
        """Calculate response time in hours"""
        if self.responded_at:
            return (self.responded_at - self.created_at).total_seconds() / 3600
        return None