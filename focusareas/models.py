from django.db import models
from django.utils import timezone
import uuid
import os


def generate_uuid():
    """Generate a unique UUID string for model primary keys"""
    return str(uuid.uuid4())


def upload_to_focus_area_images(instance, filename):
    """Generate upload path for focus area images"""
    return os.path.join('focus_areas', 'images', filename)


class FocusArea(models.Model):
    """Model for CEPA's focus areas"""
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Planned', 'Planned'),
    ]

    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Short description for cards and previews")
    image = models.ImageField(upload_to=upload_to_focus_area_images, blank=True, null=True)

    # Overview section
    overview_summary = models.TextField(help_text="Detailed summary for the overview section")

    # Timeline
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    start_date = models.CharField(max_length=100, help_text="E.g., 'January 2020'")

    # Display order
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Focus Area'
        verbose_name_plural = 'Focus Areas'

    def __str__(self):
        return self.title


class FocusAreaObjective(models.Model):
    """Objectives for a focus area"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    focus_area = models.ForeignKey(FocusArea, on_delete=models.CASCADE, related_name='objectives')
    text = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Objective'
        verbose_name_plural = 'Objectives'

    def __str__(self):
        return f"{self.focus_area.title} - {self.text[:50]}"


class FocusAreaActivity(models.Model):
    """Key activities for a focus area"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    focus_area = models.ForeignKey(FocusArea, on_delete=models.CASCADE, related_name='activities')
    text = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.focus_area.title} - {self.text[:50]}"


class FocusAreaOutcome(models.Model):
    """Outcomes and impact for a focus area"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    focus_area = models.ForeignKey(FocusArea, on_delete=models.CASCADE, related_name='outcomes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    metric = models.CharField(max_length=100, help_text="E.g., '50+ Reports', '500+ Trained'")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Outcome'
        verbose_name_plural = 'Outcomes'

    def __str__(self):
        return f"{self.focus_area.title} - {self.title}"


class FocusAreaPartner(models.Model):
    """Partners for a focus area"""
    PARTNER_TYPES = [
        ('Government', 'Government'),
        ('Donor', 'Donor'),
        ('NGO Partners', 'NGO Partners'),
        ('International Partner', 'International Partner'),
        ('Private Sector', 'Private Sector'),
        ('Research Partners', 'Research Partners'),
        ('Media Partners', 'Media Partners'),
    ]

    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    focus_area = models.ForeignKey(FocusArea, on_delete=models.CASCADE, related_name='partners')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, choices=PARTNER_TYPES)
    role = models.TextField(help_text="Description of their role in this focus area")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return f"{self.focus_area.title} - {self.name}"


class FocusAreaMilestone(models.Model):
    """Timeline milestones for a focus area"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    focus_area = models.ForeignKey(FocusArea, on_delete=models.CASCADE, related_name='milestones')
    year = models.CharField(max_length=10)
    event = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Milestone'
        verbose_name_plural = 'Milestones'

    def __str__(self):
        return f"{self.focus_area.title} - {self.year}"
