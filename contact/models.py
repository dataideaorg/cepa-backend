from django.db import models
from django.utils import timezone
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Contact(models.Model):
    INQUIRY_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('partnership', 'Partnership Opportunity'),
        ('media', 'Media Inquiry'),
        ('research', 'Research Collaboration'),
        ('fellowship', 'Fellowship Program'),
        ('speaking', 'Speaking Engagement'),
        ('other', 'Other'),
    ]
    
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='general')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_responded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Newsletter(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
    
    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return f"{name} ({self.email})" if name else self.email