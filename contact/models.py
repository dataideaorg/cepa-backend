from django.db import models

class Contact(models.Model):
    INQUIRY_CHOICES = [
        ('general', 'General Inquiry'),
        ('donate', 'Donation Inquiry'),
        ('career', 'Career Opportunities'),
        ('fellowships', 'Fellowship Programs'),
        ('membership', 'Membership'),
        ('announcements', 'Announcements'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    organization = models.CharField(max_length=100, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_CHOICES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}" 
    
class Newsletter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Feedback(models.Model):
    """Model to store user feedback from Citizens Voice page"""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"