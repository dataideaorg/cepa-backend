from django.db import models
from django.utils import timezone
import uuid
import os


def generate_uuid():
    """Generate a unique UUID string for model primary keys"""
    return str(uuid.uuid4())


def upload_to_career_images(instance, filename):
    """Generate upload path for career opportunity images"""
    return os.path.join('career', 'images', filename)


def upload_to_announcement_images(instance, filename):
    """Generate upload path for announcement images"""
    return os.path.join('announcements', 'images', filename)


class CareerOpportunity(models.Model):
    """Model for career opportunities, internships, fellowships, and consultancies"""
    OPPORTUNITY_TYPES = [
        ('Full-time', 'Full-time Position'),
        ('Internship', 'Internship'),
        ('Fellowship', 'Fellowship'),
        ('Consultancy', 'Consultancy'),
        ('Part-time', 'Part-time Position'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.CharField(max_length=500)
    type = models.CharField(max_length=100, choices=OPPORTUNITY_TYPES)
    location = models.CharField(max_length=200, default='Kampala, Uganda')
    department = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    responsibilities = models.TextField(help_text='Main responsibilities for this position')
    requirements = models.TextField(help_text='Required qualifications and skills')
    how_to_apply = models.TextField(help_text='Application instructions and process')
    deadline = models.DateField(help_text='Application deadline')
    posted_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to=upload_to_career_images, blank=True, null=True)
    slug = models.CharField(max_length=500, unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Career Opportunity'
        verbose_name_plural = 'Career Opportunities'

    def __str__(self):
        return f"{self.title} - {self.type}"


class Announcement(models.Model):
    """Model for announcements, updates, and general notices"""
    ANNOUNCEMENT_TYPES = [
        ('General', 'General Announcement'),
        ('Event', 'Event Announcement'),
        ('Program', 'Program Update'),
        ('Partnership', 'Partnership Announcement'),
        ('Achievement', 'Achievement/Award'),
        ('Policy', 'Policy Update'),
        ('Urgent', 'Urgent Notice'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.CharField(max_length=500)
    type = models.CharField(max_length=100, choices=ANNOUNCEMENT_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    summary = models.TextField(help_text='Brief summary or excerpt')
    content = models.TextField(help_text='Full announcement content')
    published_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(blank=True, null=True, help_text='Optional expiry date for time-sensitive announcements')
    is_active = models.BooleanField(default=True, help_text='Whether the announcement is currently active')
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to=upload_to_announcement_images, blank=True, null=True)
    slug = models.CharField(max_length=500, unique=True, blank=True)
    external_link = models.URLField(blank=True, null=True, help_text='Optional external link for more information')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return f"{self.title} - {self.type}"