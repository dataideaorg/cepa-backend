# Contact API Documentation

This document describes the contact form and newsletter API endpoints for the CEPA website.

## Base URL
```
https://cepa-backend-production.up.railway.app/contact/
```

## Endpoints

### 1. Contact Form Submission
**Endpoint:** `POST /contact/contact/`

**Description:** Submit a contact form inquiry with automatic email notifications.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+256 700 123 456",  // Optional
  "organization": "Example Organization",  // Optional
  "subject": "Policy Research Inquiry",
  "message": "I'm interested in learning more about your research programs...",
  "inquiry_type": "research"  // Optional, defaults to "general"
}
```

**Inquiry Types:**
- `general` - General Inquiry (default)
- `partnership` - Partnership Opportunity
- `media` - Media Inquiry
- `research` - Research Collaboration
- `fellowship` - Fellowship Program
- `speaking` - Speaking Engagement
- `other` - Other

**Response (Success - 201):**
```json
{
  "message": "Contact form submitted successfully",
  "id": "uuid-string"
}
```

**Response (Error - 400):**
```json
{
  "field_name": ["Error message"],
  "email": ["This field is required."],
  "first_name": ["First name is required."]
}
```

**Features:**
- Automatic email notification to admin
- Confirmation email to user
- Form validation
- Inquiry type categorization
- Database storage for admin review

---

### 2. Newsletter Subscription
**Endpoint:** `POST /contact/newsletter/`

**Description:** Subscribe to the CEPA newsletter.

**Request Body:**
```json
{
  "email": "subscriber@example.com",
  "first_name": "Jane",  // Optional
  "last_name": "Smith"   // Optional
}
```

**Response (Success - 201):**
```json
{
  "message": "Newsletter subscription successful",
  "id": "uuid-string"
}
```

**Response (Error - 400):**
```json
{
  "email": ["This email is already subscribed to our newsletter."]
}
```

**Features:**
- Duplicate email prevention
- Welcome email with subscription confirmation
- Reactivation of previously unsubscribed emails
- Database storage for mailing list management

---

### 3. Contact List (Admin)
**Endpoint:** `GET /contact/contacts/`

**Description:** Retrieve all contact form submissions (for admin use).

**Response:**
```json
[
  {
    "id": "uuid-string",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+256 700 123 456",
    "organization": "Example Organization",
    "subject": "Policy Research Inquiry",
    "message": "I'm interested in learning more...",
    "inquiry_type": "research",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "is_responded": false
  }
]
```

---

### 4. Newsletter List (Admin)
**Endpoint:** `GET /contact/newsletters/`

**Description:** Retrieve all active newsletter subscriptions (for admin use).

**Response:**
```json
[
  {
    "id": "uuid-string",
    "email": "subscriber@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "is_active": true,
    "subscribed_at": "2024-01-15T10:30:00Z",
    "unsubscribed_at": null
  }
]
```

---

## Email Templates

The system includes three HTML email templates:

1. **Admin Notification** (`contact/emails/admin_notification.html`)
   - Sent to admin when contact form is submitted
   - Includes all form details in formatted layout
   - Professional styling with CEPA branding

2. **Contact Confirmation** (`contact/emails/contact_confirmation.html`)
   - Sent to user after contact form submission
   - Confirms receipt and provides response timeline
   - Includes CEPA contact information

3. **Newsletter Confirmation** (`contact/emails/newsletter_confirmation.html`)
   - Sent to new newsletter subscribers
   - Welcome message with subscription benefits
   - Social media links and unsubscribe information

---

## Database Models

### Contact Model
- `id` (Primary Key, UUID)
- `first_name` (CharField, required)
- `last_name` (CharField, required)
- `email` (EmailField, required)
- `phone` (CharField, optional)
- `organization` (CharField, optional)
- `subject` (CharField, required)
- `message` (TextField, required)
- `inquiry_type` (CharField, choices)
- `created_at` (DateTimeField, auto)
- `updated_at` (DateTimeField, auto)
- `is_responded` (BooleanField, default False)

### Newsletter Model
- `id` (Primary Key, UUID)
- `email` (EmailField, unique)
- `first_name` (CharField, optional)
- `last_name` (CharField, optional)
- `is_active` (BooleanField, default True)
- `subscribed_at` (DateTimeField, auto)
- `unsubscribed_at` (DateTimeField, optional)

---

## Admin Interface

Both models are registered in Django Admin with:
- List views with filtering and searching
- Bulk actions for newsletter management
- Field organization in logical sections
- Responsive status tracking

---

## Error Handling

- Email sending failures don't prevent form submission
- Validation errors return detailed field-specific messages
- Database connection issues are handled gracefully
- All errors are logged for debugging

---

## Testing

### Contact Form Test:
```bash
curl -X POST https://cepa-backend-production.up.railway.app/contact/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "subject": "Test Inquiry",
    "message": "This is a test message",
    "inquiry_type": "general"
  }'
```

### Newsletter Test:
```bash
curl -X POST https://cepa-backend-production.up.railway.app/contact/newsletter/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newsletter@example.com",
    "first_name": "Newsletter",
    "last_name": "Subscriber"
  }'
```
