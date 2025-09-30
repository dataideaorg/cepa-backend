# Announcements API Documentation

## Base URL
```
https://cepa-backend-production.up.railway.app/getinvolved/
```

## Endpoints

### 1. List All Announcements
Get a paginated list of all announcements.

**Endpoint:** `GET /getinvolved/announcements/`

**Query Parameters:**
- `page` (integer, optional): Page number for pagination (default: 1)
- `page_size` (integer, optional): Number of items per page (default: 10, max: 100)
- `type` (string, optional): Filter by announcement type (`General`, `Event`, `Program`, `Partnership`, `Achievement`, `Policy`, `Urgent`)
- `priority` (string, optional): Filter by priority (`low`, `medium`, `high`, `urgent`)
- `is_active` (boolean, optional): Filter by active status
- `featured` (boolean, optional): Filter by featured status
- `search` (string, optional): Search in title, summary, and content
- `ordering` (string, optional): Order results by field (prefix with `-` for descending)
  - Options: `created_at`, `published_date`, `priority`, `title`

**Response:**
```json
{
  "count": 10,
  "next": "https://cepa-backend-production.up.railway.app/getinvolved/announcements/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-string",
      "title": "Important Program Update",
      "type": "Program",
      "priority": "high",
      "summary": "We are pleased to announce updates to our governance training program...",
      "content": "Full detailed content of the announcement goes here...",
      "published_date": "2025-09-01",
      "expiry_date": "2025-12-31",
      "is_active": true,
      "featured": true,
      "image": "https://cepa-backend-production.up.railway.app/media/announcements/images/program.jpg",
      "slug": "important-program-update",
      "external_link": "https://example.com/more-info",
      "created_at": "2025-09-01T10:00:00Z",
      "updated_at": "2025-09-01T10:00:00Z"
    }
  ]
}
```

### 2. Get Announcement by ID
Get a specific announcement by its ID.

**Endpoint:** `GET /getinvolved/announcements/{id}/`

**Response:** Same as single item in results array above

### 3. Get Announcement by Slug
Get a specific announcement by its slug.

**Endpoint:** `GET /getinvolved/announcements/slug/{slug}/`

**Example:** `GET /getinvolved/announcements/slug/important-program-update/`

**Response:** Same as single item in results array above

### 4. Get Featured Announcements
Get all featured and active announcements.

**Endpoint:** `GET /getinvolved/announcements/featured/`

**Response:** Array of announcements

### 5. Get Active Announcements
Get all active announcements (not expired).

**Endpoint:** `GET /getinvolved/announcements/active/`

**Description:** Returns announcements where:
- `is_active` is `true`
- Either `expiry_date` is null OR `expiry_date` is greater than or equal to today

**Response:** Array of announcements

### 6. Get Urgent Announcements
Get urgent priority announcements that are active and not expired.

**Endpoint:** `GET /getinvolved/announcements/urgent/`

**Response:** Array of announcements

### 7. Get Announcements by Type
Get announcements filtered by type.

**Endpoint:** `GET /getinvolved/announcements/by_type/?type={type}`

**Query Parameters:**
- `type` (string, required): Announcement type (`General`, `Event`, `Program`, `Partnership`, `Achievement`, `Policy`, `Urgent`)

**Example:** `GET /getinvolved/announcements/by_type/?type=Program`

**Response:** Array of announcements

## Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique identifier for the announcement |
| title | string | Announcement title |
| type | string | Type of announcement (General, Event, Program, Partnership, Achievement, Policy, Urgent) |
| priority | string | Priority level (low, medium, high, urgent) |
| summary | text | Brief summary or excerpt |
| content | text | Full announcement content |
| published_date | date | Date the announcement was published (YYYY-MM-DD) |
| expiry_date | date (optional) | Optional expiry date for time-sensitive announcements (YYYY-MM-DD) |
| is_active | boolean | Whether the announcement is currently active |
| featured | boolean | Whether the announcement is featured |
| image | string (URL, optional) | Image URL for the announcement |
| slug | string | URL-friendly version of the title |
| external_link | string (URL, optional) | Optional external link for more information |
| created_at | datetime | Timestamp when created |
| updated_at | datetime | Timestamp when last updated |

## Announcement Types

| Type | Description |
|------|-------------|
| General | General announcements and updates |
| Event | Event-related announcements |
| Program | Program updates and changes |
| Partnership | Partnership announcements |
| Achievement | Achievements and awards |
| Policy | Policy updates and changes |
| Urgent | Urgent notices requiring immediate attention |

## Priority Levels

| Priority | Use Case |
|----------|----------|
| low | General information, not time-sensitive |
| medium | Standard announcements |
| high | Important announcements requiring attention |
| urgent | Critical announcements requiring immediate action |

## Example Usage

### Get all active announcements
```bash
curl https://cepa-backend-production.up.railway.app/getinvolved/announcements/active/
```

### Get featured announcements
```bash
curl https://cepa-backend-production.up.railway.app/getinvolved/announcements/featured/
```

### Get urgent announcements
```bash
curl https://cepa-backend-production.up.railway.app/getinvolved/announcements/urgent/
```

### Search for program-related announcements
```bash
curl "https://cepa-backend-production.up.railway.app/getinvolved/announcements/?type=Program"
```

### Get high-priority announcements
```bash
curl "https://cepa-backend-production.up.railway.app/getinvolved/announcements/?priority=high"
```

### Search announcements by keyword
```bash
curl "https://cepa-backend-production.up.railway.app/getinvolved/announcements/?search=governance"
```

### Get announcements ordered by priority (urgent first)
```bash
curl "https://cepa-backend-production.up.railway.app/getinvolved/announcements/?ordering=-priority"
```

## Error Responses

### 404 Not Found
```json
{
  "error": "Announcement not found"
}
```

### 400 Bad Request
```json
{
  "error": "Type parameter is required"
}
```

## Notes
- All dates are in ISO 8601 format
- Image URLs are absolute URLs to the media server
- The API supports CORS for frontend access
- Pagination is included in all list endpoints
- Search is case-insensitive and searches across multiple fields
- Announcements with `expiry_date` set will only appear in `active` endpoint if the date hasn't passed
- The `active` endpoint automatically filters out expired announcements
