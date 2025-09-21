# Contact Form API Documentation

## Overview
The Contact API provides endpoints for managing contact form submissions. It includes public submission endpoints and admin management features.

## Base URL
```
https://cepa-backend-production.up.railway.app/contact/
```

## Endpoints

### 1. Submit Contact Form (Public)
**POST** `/submissions/submit/`

Submit a new contact form message.

#### Request Body
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+256700000000",
  "organization": "Test Organization",
  "subject": "general",
  "message": "This is a detailed message about your inquiry."
}
```

#### Required Fields
- `name` (string): Full name (minimum 2 characters)
- `email` (string): Valid email address
- `message` (string): Message content (minimum 10 characters)

#### Optional Fields
- `phone` (string): Phone number
- `organization` (string): Organization name
- `subject` (string): Subject category (default: "general")

#### Subject Options
- `general` - General Inquiry
- `partnership` - Partnership
- `media` - Media Inquiry
- `donation` - Donation
- `volunteer` - Volunteer
- `fellowship` - Fellowship Program
- `event` - Event Information
- `research` - Research Collaboration
- `other` - Other

#### Response
**Success (201 Created)**
```json
{
  "success": true,
  "message": "Thank you for your message. We will get back to you soon.",
  "submission_id": "uuid-string"
}
```

**Error (400 Bad Request)**
```json
{
  "success": false,
  "errors": {
    "email": ["Enter a valid email address."],
    "message": ["Please provide a message with at least 10 characters."]
  }
}
```

### 2. List Submissions (Admin Only)
**GET** `/submissions/`

Retrieve all contact submissions (requires authentication).

#### Query Parameters
- `search` (string): Search in name, email, organization, message, or subject
- `status` (string): Filter by status (new, in_progress, responded, closed)
- `priority` (string): Filter by priority (low, medium, high, urgent)
- `subject` (string): Filter by subject category
- `is_spam` (boolean): Filter by spam status
- `ordering` (string): Order by field (e.g., `-created_at` for newest first)

#### Response
```json
[
  {
    "id": "uuid-string",
    "name": "John Doe",
    "email": "john@example.com",
    "organization": "Test Organization",
    "subject": "general",
    "priority": "medium",
    "status": "new",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "responded_at": null,
    "response_time_hours": null,
    "is_old": false
  }
]
```

### 3. Get Submission Details (Admin Only)
**GET** `/submissions/{id}/`

Retrieve detailed information about a specific submission.

#### Response
```json
{
  "id": "uuid-string",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+256700000000",
  "organization": "Test Organization",
  "subject": "general",
  "message": "This is a detailed message...",
  "priority": "medium",
  "status": "new",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "is_spam": false,
  "admin_notes": "",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "responded_at": null
}
```

### 4. Update Submission (Admin Only)
**PATCH** `/submissions/{id}/`

Update submission status, priority, or admin notes.

#### Request Body
```json
{
  "priority": "high",
  "status": "in_progress",
  "admin_notes": "Assigned to team member for follow-up",
  "is_spam": false
}
```

### 5. Mark as Responded (Admin Only)
**POST** `/submissions/{id}/mark_responded/`

Mark a submission as responded to.

#### Response
```json
{
  "success": true,
  "message": "Submission marked as responded"
}
```

### 6. Mark as Closed (Admin Only)
**POST** `/submissions/{id}/mark_closed/`

Mark a submission as closed.

#### Response
```json
{
  "success": true,
  "message": "Submission marked as closed"
}
```

### 7. Get Statistics (Admin Only)
**GET** `/submissions/stats/`

Get contact submission statistics.

#### Response
```json
{
  "total": 150,
  "status_breakdown": {
    "new": 25,
    "in_progress": 10,
    "responded": 100,
    "closed": 15
  },
  "spam_count": 5,
  "recent_submissions": 20,
  "subject_breakdown": [
    {"subject": "general", "count": 50},
    {"subject": "partnership", "count": 30}
  ],
  "priority_breakdown": [
    {"priority": "medium", "count": 80},
    {"priority": "high", "count": 20}
  ]
}
```

### 8. Search Submissions (Admin Only)
**GET** `/submissions/search/?q=search_term`

Search submissions by name, email, organization, message, or subject.

#### Query Parameters
- `q` (string, required): Search term

#### Response
```json
[
  {
    "id": "uuid-string",
    "name": "John Doe",
    "email": "john@example.com",
    "organization": "Test Organization",
    "subject": "general",
    "priority": "medium",
    "status": "new",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "responded_at": null,
    "response_time_hours": null,
    "is_old": false
  }
]
```

## Features

### Spam Detection
The API includes basic spam detection that automatically flags submissions containing:
- Common spam keywords (viagra, casino, lottery, etc.)
- Suspicious patterns (repeated characters, short messages with URLs)
- Other spam indicators

### IP Tracking
All submissions are automatically tracked with:
- Client IP address
- User agent string
- Timestamp

### Admin Management
Admin users can:
- View all submissions with filtering and search
- Update submission status and priority
- Add admin notes
- Mark submissions as spam or not spam
- Track response times
- Generate statistics

### Status Workflow
1. **New** - Initial status for all submissions
2. **In Progress** - Being handled by admin
3. **Responded** - Response sent to user
4. **Closed** - Final status, no further action needed

### Priority Levels
- **Low** - Non-urgent inquiries
- **Medium** - Standard priority (default)
- **High** - Important inquiries
- **Urgent** - Critical issues requiring immediate attention

## Error Handling

### Common Error Responses

**400 Bad Request**
```json
{
  "success": false,
  "errors": {
    "field_name": ["Error message"]
  }
}
```

**401 Unauthorized**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**404 Not Found**
```json
{
  "detail": "Not found."
}
```

**500 Internal Server Error**
```json
{
  "detail": "A server error occurred."
}
```

## Rate Limiting
The API implements basic rate limiting to prevent abuse. Excessive requests may result in temporary blocking.

## Security Features
- Input validation and sanitization
- Spam detection
- IP address tracking
- User agent logging
- Admin-only access to sensitive operations
