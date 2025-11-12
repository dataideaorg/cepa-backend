from django.db import models
from django.utils import timezone


class HeroSection(models.Model):
    """Hero section for the About page"""
    title = models.CharField(max_length=255, default="About CEPA")
    description = models.TextField(help_text="Main hero description")
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True, help_text="Hero background image")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Section'

    def __str__(self):
        return "About Page - Hero Section"

    def save(self, *args, **kwargs):
        if not self.pk and HeroSection.objects.exists():
            raise ValueError('Only one Hero Section instance is allowed')
        return super().save(*args, **kwargs)


class WhoWeAreSection(models.Model):
    """Who We Are section"""
    title = models.CharField(max_length=255, default="Who We Are")
    description = models.TextField(help_text="Section description")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Who We Are Section'
        verbose_name_plural = 'Who We Are Section'

    def __str__(self):
        return "About Page - Who We Are Section"

    def save(self, *args, **kwargs):
        if not self.pk and WhoWeAreSection.objects.exists():
            raise ValueError('Only one Who We Are Section instance is allowed')
        return super().save(*args, **kwargs)


class WhoWeAreFeature(models.Model):
    """Features for Who We Are section"""
    section = models.ForeignKey(WhoWeAreSection, on_delete=models.CASCADE, related_name='features')
    icon = models.CharField(max_length=10, help_text="Emoji icon")
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Who We Are Feature'
        verbose_name_plural = 'Who We Are Features'

    def __str__(self):
        return self.title


class StatCard(models.Model):
    """Statistics cards"""
    value = models.IntegerField(help_text="Numeric value (e.g., 10, 50, 100)")
    label = models.CharField(max_length=255, help_text="Label (e.g., 'Years of Impact', 'Policy Reports')")
    order = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Stat Card'
        verbose_name_plural = 'Stat Cards'

    def __str__(self):
        return f"{self.value}+ {self.label}"


class OurStorySection(models.Model):
    """Our Story section"""
    title = models.CharField(max_length=255, default="Our Story")
    description = models.TextField(help_text="Section description")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Our Story Section'
        verbose_name_plural = 'Our Story Section'

    def __str__(self):
        return "About Page - Our Story Section"

    def save(self, *args, **kwargs):
        if not self.pk and OurStorySection.objects.exists():
            raise ValueError('Only one Our Story Section instance is allowed')
        return super().save(*args, **kwargs)


class OurStoryCard(models.Model):
    """Cards for Our Story section (Vision, Mission, Values)"""
    section = models.ForeignKey(OurStorySection, on_delete=models.CASCADE, related_name='cards')
    icon = models.CharField(max_length=10, help_text="Emoji icon")
    title = models.CharField(max_length=255, help_text="e.g., 'Our Vision', 'Our Mission', 'Our Values'")
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Our Story Card'
        verbose_name_plural = 'Our Story Cards'

    def __str__(self):
        return self.title


class WhatSetsUsApartSection(models.Model):
    """What Sets CEPA Apart section"""
    title = models.CharField(max_length=255, default="What Sets CEPA Apart")
    description = models.TextField(help_text="Section description")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'What Sets Us Apart Section'
        verbose_name_plural = 'What Sets Us Apart Section'

    def __str__(self):
        return "About Page - What Sets Us Apart Section"

    def save(self, *args, **kwargs):
        if not self.pk and WhatSetsUsApartSection.objects.exists():
            raise ValueError('Only one What Sets Us Apart Section instance is allowed')
        return super().save(*args, **kwargs)


class WhatSetsUsApartCard(models.Model):
    """Cards for What Sets Us Apart section"""
    section = models.ForeignKey(WhatSetsUsApartSection, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'What Sets Us Apart Card'
        verbose_name_plural = 'What Sets Us Apart Cards'

    def __str__(self):
        return self.title


class CallToActionSection(models.Model):
    """Call to Action section"""
    title = models.CharField(max_length=255, default="Join Us in Building a Better Uganda")
    description = models.TextField(help_text="Section description")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Call to Action Section'
        verbose_name_plural = 'Call to Action Section'

    def __str__(self):
        return "About Page - Call to Action Section"

    def save(self, *args, **kwargs):
        if not self.pk and CallToActionSection.objects.exists():
            raise ValueError('Only one Call to Action Section instance is allowed')
        return super().save(*args, **kwargs)


class TeamMember(models.Model):
    """Team member for the Our Team section"""
    name = models.CharField(max_length=255, help_text="Full name")
    role = models.CharField(max_length=255, help_text="Job title/role")
    profile_image = models.ImageField(upload_to='team/', help_text="Team member photo")
    linkedin_url = models.URLField(max_length=500, blank=True, null=True, help_text="LinkedIn profile URL")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Show on website")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return f"{self.name} - {self.role}"


class Partner(models.Model):
    """Partner organization for the Partners section"""
    name = models.CharField(max_length=255, help_text="Partner organization name")
    full_name = models.CharField(max_length=500, blank=True, null=True, help_text="Full organization name (optional)")
    logo = models.ImageField(upload_to='partners/', help_text="Partner logo")
    website_url = models.URLField(max_length=500, blank=True, null=True, help_text="Partner website URL (optional)")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Show on website")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return self.name
