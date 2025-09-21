# Email Setup Guide for CEPA Contact Form

## Overview
This guide explains how to configure Gmail SMTP for sending contact form notifications and auto-replies.

## Prerequisites
- Gmail account
- App Password (not regular password)

## Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification if not already enabled

## Step 2: Generate App Password
1. Go to Google Account settings
2. Navigate to Security > 2-Step Verification
3. Scroll down to "App passwords"
4. Select "Mail" as the app
5. Generate a 16-character app password
6. Copy this password (you'll need it for EMAIL_HOST_PASSWORD)

## Step 3: Configure Environment Variables

### For Railway Deployment
Add these environment variables in your Railway dashboard:

```bash
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=noreply@cepa.or.ug
CONTACT_EMAIL_RECIPIENTS=info@cepa.or.ug,admin@cepa.or.ug
```

### For Local Development
Create a `.env` file in your backend directory:

```bash
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=noreply@cepa.or.ug
CONTACT_EMAIL_RECIPIENTS=info@cepa.or.ug,admin@cepa.or.ug
```

## Step 4: Test Email Configuration

### Test with Management Command
```bash
cd backend
poetry run python manage.py test_email --create-submission --email=test@example.com
```

### Test with Contact Form
1. Submit a contact form on the website
2. Check if you receive:
   - Admin notification email
   - Auto-reply email to the submitter

## Email Templates

### Admin Notification Email
- **Recipients**: Email addresses in `CONTACT_EMAIL_RECIPIENTS`
- **Content**: Full submission details, spam warnings, admin actions
- **Templates**: 
  - HTML: `contact/templates/contact/emails/contact_submission.html`
  - Text: `contact/templates/contact/emails/contact_submission.txt`

### Auto-Reply Email
- **Recipients**: The person who submitted the form
- **Content**: Thank you message, next steps, contact information
- **Templates**:
  - HTML: `contact/templates/contact/emails/auto_reply.html`
  - Text: `contact/templates/contact/emails/auto_reply.txt`

## Email Features

### Spam Detection
- Automatic spam flagging based on content analysis
- Spam submissions don't trigger auto-reply emails
- Admin notifications include spam warnings

### Priority Handling
- Urgent/High priority submissions get special email formatting
- Subject lines include priority indicators

### Admin Actions
- Direct links to admin panel for each submission
- Response time tracking
- Submission status management

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify you're using an App Password, not your regular Gmail password
   - Ensure 2-Factor Authentication is enabled

2. **SMTP Connection Error**
   - Check EMAIL_HOST and EMAIL_PORT settings
   - Verify EMAIL_USE_TLS is True

3. **Emails Not Sending**
   - Check Django logs for error messages
   - Verify environment variables are set correctly
   - Test with the management command

4. **Emails Going to Spam**
   - Add your domain to SPF records
   - Configure DKIM for your domain
   - Use a professional "from" email address

### Logging
Email sending errors are logged to Django's logger. Check logs for detailed error messages.

## Security Considerations

1. **Environment Variables**
   - Never commit email credentials to version control
   - Use environment variables for all sensitive data

2. **App Passwords**
   - Use unique app passwords for each environment
   - Rotate app passwords regularly

3. **Email Content**
   - Be careful with user input in email templates
   - Sanitize data before including in emails

## Production Recommendations

1. **Use a Professional Email Service**
   - Consider using SendGrid, Mailgun, or AWS SES for production
   - Better deliverability and tracking

2. **Email Queuing**
   - Implement Celery for background email processing
   - Prevents blocking the web request

3. **Monitoring**
   - Set up email delivery monitoring
   - Track bounce rates and spam complaints

## Support
For issues with email configuration, check:
1. Django logs for error messages
2. Gmail account security settings
3. Environment variable configuration
4. Network connectivity to Gmail SMTP servers
