from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from .models import ContactSubmission
import logging

logger = logging.getLogger(__name__)

class ContactEmailService:
    """Service for sending contact form emails"""
    
    @staticmethod
    def send_contact_notification(submission: ContactSubmission):
        """Send email notification for new contact submission"""
        try:
            # Get admin URL for the submission
            admin_url = f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}{reverse('admin:contact_contactsubmission_change', args=[submission.id])}"
            
            # Prepare context for email templates
            context = {
                'submission': submission,
                'admin_url': admin_url,
            }
            
            # Render email templates
            html_content = render_to_string('contact/emails/contact_submission.html', context)
            text_content = render_to_string('contact/emails/contact_submission.txt', context)
            
            # Create email subject based on priority and spam status
            subject_parts = ['New Contact Form Submission']
            
            if submission.is_spam:
                subject_parts.append('[SPAM FLAGGED]')
            
            if submission.priority == 'urgent':
                subject_parts.append('[URGENT]')
            elif submission.priority == 'high':
                subject_parts.append('[HIGH PRIORITY]')
            
            subject_parts.append(f'- {submission.get_subject_display()}')
            subject = ' '.join(subject_parts)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=settings.CONTACT_EMAIL_RECIPIENTS,
            )
            
            # Attach HTML version
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            
            logger.info(f"Contact notification email sent for submission {submission.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send contact notification email for submission {submission.id}: {str(e)}")
            return False
    
    @staticmethod
    def send_auto_reply(submission: ContactSubmission):
        """Send auto-reply to the person who submitted the form"""
        try:
            # Prepare context for auto-reply
            context = {
                'submission': submission,
                'name': submission.name.split()[0] if submission.name else 'Valued Visitor',
            }
            
            # Render auto-reply templates
            html_content = render_to_string('contact/emails/auto_reply.html', context)
            text_content = render_to_string('contact/emails/auto_reply.txt', context)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=f"Thank you for contacting CEPA - {submission.get_subject_display()}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[submission.email],
            )
            
            # Attach HTML version
            email.attach_alternative(html_content, "text/html")
            
            # Send email
            email.send()
            
            logger.info(f"Auto-reply email sent to {submission.email} for submission {submission.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send auto-reply email for submission {submission.id}: {str(e)}")
            return False
