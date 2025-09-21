from django.core.management.base import BaseCommand
from django.conf import settings
from contact.models import ContactSubmission
from contact.services import ContactEmailService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test email sending functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test email to',
            default='test@example.com'
        )
        parser.add_argument(
            '--create-submission',
            action='store_true',
            help='Create a test submission and send emails',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing email configuration...'))
        
        # Check email settings
        self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"CONTACT_EMAIL_RECIPIENTS: {settings.CONTACT_EMAIL_RECIPIENTS}")
        
        if options['create_submission']:
            # Create a test submission
            self.stdout.write(self.style.SUCCESS('Creating test submission...'))
            
            submission = ContactSubmission.objects.create(
                name='Test User',
                email=options['email'],
                phone='+256700000000',
                organization='Test Organization',
                subject='general',
                message='This is a test message to verify email functionality.',
                priority='medium',
                ip_address='127.0.0.1',
                user_agent='Test Command'
            )
            
            self.stdout.write(f"Created submission: {submission.id}")
            
            # Test sending notification email
            self.stdout.write(self.style.SUCCESS('Sending notification email...'))
            if ContactEmailService.send_contact_notification(submission):
                self.stdout.write(self.style.SUCCESS('✓ Notification email sent successfully'))
            else:
                self.stdout.write(self.style.ERROR('✗ Failed to send notification email'))
            
            # Test sending auto-reply email
            self.stdout.write(self.style.SUCCESS('Sending auto-reply email...'))
            if ContactEmailService.send_auto_reply(submission):
                self.stdout.write(self.style.SUCCESS('✓ Auto-reply email sent successfully'))
            else:
                self.stdout.write(self.style.ERROR('✗ Failed to send auto-reply email'))
            
            # Clean up test submission
            submission.delete()
            self.stdout.write(self.style.SUCCESS('Test submission cleaned up'))
        
        else:
            self.stdout.write(self.style.WARNING('Use --create-submission to test email sending'))
        
        self.stdout.write(self.style.SUCCESS('Email test completed!'))
