from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import logging
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import ContactSubmission
from .serializers import (
    ContactSubmissionSerializer, 
    ContactSubmissionCreateSerializer,
    ContactSubmissionListSerializer,
    ContactSubmissionUpdateSerializer
)

logger = logging.getLogger(__name__)

class ContactSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContactSubmissionCreateSerializer
        elif self.action == 'list':
            return ContactSubmissionListSerializer
        elif self.action in ['update', 'partial_update']:
            return ContactSubmissionUpdateSerializer
        return ContactSubmissionSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_authenticated:
            return ContactSubmission.objects.all()
        return ContactSubmission.objects.none()  # Non-authenticated users can't list submissions
    
    def perform_create(self, serializer):
        """Create a new contact submission"""
        # Get client IP and user agent
        ip_address = self.get_client_ip()
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        # Basic spam detection
        is_spam = self.detect_spam(serializer.validated_data)
        
        submission = serializer.save(
            ip_address=ip_address,
            user_agent=user_agent,
            is_spam=is_spam
        )
        
        # Send email notifications with proper error handling
        try:
            # Check if email settings are properly configured
            if not settings.CONTACT_EMAIL_RECIPIENTS:
                print("Warning: CONTACT_EMAIL_RECIPIENTS not configured, skipping email sending")
            else:
                # Create simple email content
                admin_subject = f"New Contact Form Submission: {submission.get_subject_display()}"
                if submission.is_spam:
                    admin_subject = f"[SPAM] {admin_subject}"
                
                admin_message = f"""
New contact form submission received:

Name: {submission.name}
Email: {submission.email}
Phone: {submission.phone or 'Not provided'}
Organization: {submission.organization or 'Not provided'}
Subject: {submission.get_subject_display()}
Priority: {submission.get_priority_display()}
Spam Status: {'Yes' if submission.is_spam else 'No'}

Message:
{submission.message}

Submitted at: {submission.created_at}
IP Address: {submission.ip_address}
                """.strip()
                
                # Send email to admin
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    settings.CONTACT_EMAIL_RECIPIENTS,
                    fail_silently=True  # Don't fail the form submission if email fails
                )
                
                # Send confirmation email to user (only if not spam)
                if not is_spam:
                    user_subject = f"Thank you for contacting CEPA - {submission.get_subject_display()}"
                    user_message = f"""
Dear {submission.name},

Thank you for contacting CEPA. We have received your message regarding "{submission.get_subject_display()}" and will get back to you within 24 hours.

Your submission details:
- Subject: {submission.get_subject_display()}
- Submitted: {submission.created_at}

If you have any urgent inquiries, please contact us directly at info@cepa.or.ug or call +256 414 123 456.

Best regards,
CEPA Team
                    """.strip()
                    
                    send_mail(
                        user_subject,
                        user_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [submission.email],
                        fail_silently=True  # Don't fail the form submission if email fails
                    )
                
        except Exception as e:
            print(f"Error sending email: {e}")
            # Don't fail the form submission if email sending fails
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    def detect_spam(self, data):
        """Basic spam detection"""
        message = data.get('message', '').lower()
        name = data.get('name', '').lower()
        
        # Simple spam indicators
        spam_keywords = ['viagra', 'casino', 'lottery', 'winner', 'congratulations', 'click here', 'free money']
        
        # Check for spam keywords in message
        for keyword in spam_keywords:
            if keyword in message:
                return True
        
        # Check for suspicious patterns
        if len(message) < 20 and 'http' in message:
            return True
        
        # Check for repeated characters
        if any(char * 5 in message for char in 'abcdefghijklmnopqrstuvwxyz'):
            return True
        
        return False
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def submit(self, request):
        """Public endpoint for submitting contact forms"""
        serializer = ContactSubmissionCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Get client IP and user agent
            ip_address = self.get_client_ip()
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Basic spam detection
            is_spam = self.detect_spam(serializer.validated_data)
            
            submission = serializer.save(
                ip_address=ip_address,
                user_agent=user_agent,
                is_spam=is_spam
            )
            
            # Send email notifications with proper error handling
            try:
                # Check if email settings are properly configured
                if not settings.CONTACT_EMAIL_RECIPIENTS:
                    print("Warning: CONTACT_EMAIL_RECIPIENTS not configured, skipping email sending")
                else:
                    # Create simple email content
                    admin_subject = f"New Contact Form Submission: {submission.get_subject_display()}"
                    if submission.is_spam:
                        admin_subject = f"[SPAM] {admin_subject}"
                    
                    admin_message = f"""
New contact form submission received:

Name: {submission.name}
Email: {submission.email}
Phone: {submission.phone or 'Not provided'}
Organization: {submission.organization or 'Not provided'}
Subject: {submission.get_subject_display()}
Priority: {submission.get_priority_display()}
Spam Status: {'Yes' if submission.is_spam else 'No'}

Message:
{submission.message}

Submitted at: {submission.created_at}
IP Address: {submission.ip_address}
                    """.strip()
                    
                    # Send email to admin
                    send_mail(
                        admin_subject,
                        admin_message,
                        settings.DEFAULT_FROM_EMAIL,
                        settings.CONTACT_EMAIL_RECIPIENTS,
                        fail_silently=True  # Don't fail the form submission if email fails
                    )
                    
                    # Send confirmation email to user (only if not spam)
                    if not is_spam:
                        user_subject = f"Thank you for contacting CEPA - {submission.get_subject_display()}"
                        user_message = f"""
Dear {submission.name},

Thank you for contacting CEPA. We have received your message regarding "{submission.get_subject_display()}" and will get back to you within 24 hours.

Your submission details:
- Subject: {submission.get_subject_display()}
- Submitted: {submission.created_at}

If you have any urgent inquiries, please contact us directly at info@cepa.or.ug or call +256 414 123 456.

Best regards,
CEPA Team
                        """.strip()
                        
                        send_mail(
                            user_subject,
                            user_message,
                            settings.DEFAULT_FROM_EMAIL,
                            [submission.email],
                            fail_silently=True  # Don't fail the form submission if email fails
                        )
                    
            except Exception as e:
                print(f"Error sending email: {e}")
                # Don't fail the form submission if email sending fails
            
            return Response({
                'success': True,
                'message': 'Thank you for your message. We will get back to you soon.',
                'submission_id': submission.id
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def mark_responded(self, request, pk=None):
        """Mark a submission as responded to"""
        try:
            submission = self.get_object()
            submission.mark_as_responded()
            return Response({
                'success': True,
                'message': 'Submission marked as responded'
            })
        except ContactSubmission.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Submission not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def mark_closed(self, request, pk=None):
        """Mark a submission as closed"""
        try:
            submission = self.get_object()
            submission.mark_as_closed()
            return Response({
                'success': True,
                'message': 'Submission marked as closed'
            })
        except ContactSubmission.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Submission not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get contact submission statistics"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Basic stats
        total = ContactSubmission.objects.count()
        new = ContactSubmission.objects.filter(status='new').count()
        in_progress = ContactSubmission.objects.filter(status='in_progress').count()
        responded = ContactSubmission.objects.filter(status='responded').count()
        closed = ContactSubmission.objects.filter(status='closed').count()
        spam = ContactSubmission.objects.filter(is_spam=True).count()
        
        # Recent submissions (last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        recent = ContactSubmission.objects.filter(created_at__gte=week_ago).count()
        
        # Subject breakdown
        subject_stats = ContactSubmission.objects.values('subject').annotate(
            count=Count('subject')
        ).order_by('-count')
        
        # Priority breakdown
        priority_stats = ContactSubmission.objects.values('priority').annotate(
            count=Count('priority')
        ).order_by('-count')
        
        return Response({
            'total': total,
            'status_breakdown': {
                'new': new,
                'in_progress': in_progress,
                'responded': responded,
                'closed': closed
            },
            'spam_count': spam,
            'recent_submissions': recent,
            'subject_breakdown': list(subject_stats),
            'priority_breakdown': list(priority_stats)
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search contact submissions"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        submissions = ContactSubmission.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(organization__icontains=query) |
            Q(message__icontains=query) |
            Q(subject__icontains=query)
        ).order_by('-created_at')
        
        serializer = ContactSubmissionListSerializer(submissions, many=True)
        return Response(serializer.data)