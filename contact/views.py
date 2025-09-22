from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ContactSerializer, NewsletterSerializer
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@api_view(['POST'])
def contact_form(request):
    serializer = ContactSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the contact form submission
        contact = serializer.save()
        
        # Prepare context for email templates
        context = {
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
            'organization': contact.organization,
            'subject': contact.subject,
            'message': contact.message,
            'inquiry_type': contact.get_inquiry_type_display()
        }
        
        try:
            # Send email to admin
            admin_subject = f"New Contact Form Submission: {contact.subject}"
            admin_message = f"""
New contact form submission received:

Name: {contact.name}
Email: {contact.email}
Phone: {contact.phone or 'Not provided'}
Organization: {contact.organization or 'Not provided'}
Inquiry Type: {contact.get_inquiry_type_display()}
Subject: {contact.subject}

Message:
{contact.message}

Submitted at: {contact.created_at}
            """
            
            admin_email = EmailMultiAlternatives(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [getattr(settings, 'CONTACT_EMAIL', 'info@cepa.or.ug'), 'jumashafara0@gmail.com']
            )
            admin_email.send()
            
            # Send confirmation email to user
            user_subject = "Thank you for contacting CEPA"
            user_message = f"""
Dear {contact.name},

Thank you for contacting the Center for Policy Analysis (CEPA). We have received your message and will get back to you as soon as possible.

Your inquiry details:
Subject: {contact.subject}
Inquiry Type: {contact.get_inquiry_type_display()}

We appreciate your interest in our work and look forward to engaging with you.

Best regards,
CEPA Team
            """
            
            user_email = EmailMultiAlternatives(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [contact.email]
            )
            user_email.send()
            
        except Exception as e:
            print(f"Error sending email: {e}")
            # Still return success even if email fails
            return Response({'message': 'Contact form submitted successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'message': 'Contact form submitted successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def newsletter_form(request):
    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        newsletter = serializer.save()
        
        try:
            # Send confirmation email to newsletter subscriber
            subject = "Welcome to CEPA Newsletter"
            message = f"""
Dear Subscriber,

Thank you for subscribing to the Center for Policy Analysis (CEPA) newsletter!

You will now receive regular updates about:
- Our latest research and policy analysis
- Upcoming events and workshops
- Publications and reports
- Governance and democracy initiatives

We appreciate your interest in our work and look forward to keeping you informed about our activities.

Best regards,
CEPA Team
            """
            
            email = EmailMultiAlternatives(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [newsletter.email]
            )
            email.send()
            
        except Exception as e:
            print(f"Error sending newsletter confirmation: {e}")
        
        return Response({'message': 'Newsletter subscription successful'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)