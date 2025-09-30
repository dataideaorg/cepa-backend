# Career Opportunities API Documentation

## Base URL
```
https://cepa-backend-production.up.railway.app/getinvolved/
```

## Endpoints

### 1. List All Career Opportunities
Get a paginated list of all career opportunities.

**Endpoint:** `GET /getinvolved/career/`

**Query Parameters:**
- `page` (integer, optional): Page number for pagination (default: 1)
- `page_size` (integer, optional): Number of items per page (default: 10, max: 100)
- `type` (string, optional): Filter by opportunity type (`Full-time`, `Internship`, `Fellowship`, `Consultancy`, `Part-time`)
- `status` (string, optional): Filter by status (`open`, `closed`)
- `featured` (boolean, optional): Filter by featured status
- `location` (string, optional): Filter by location
- `search` (string, optional): Search in title, description, requirements, and responsibilities
- `ordering` (string, optional): Order results by field (prefix with `-` for descending)
  - Options: `created_at`, `posted_date`, `deadline`, `title`

**Response:**
```json
{
  "count": 10,
  "next": "https://cepa-backend-production.up.railway.app/getinvolved/career/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-string",
      "title": "Policy Research Analyst",
      "type": "Full-time",
      "location": "Kampala, Uganda",
      "department": "Research & Policy",
      "description": "We are seeking a Policy Research Analyst...",
      "responsibilities": "- Conduct policy research\n- Analyze data\n- Write reports",
      "requirements": "- Master's degree in relevant field\n- 3+ years experience",
      "how_to_apply": "Send your CV and cover letter to careers@cepa.or.ug",
      "deadline": "2025-12-31",
      "posted_date": "2025-01-01",
      "status": "open",
      "featured": true,
      "image": "https://cepa-backend-production.up.railway.app/media/career/images/analyst.jpg",
      "slug": "policy-research-analyst",
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

### 2. Get Career Opportunity by ID
Get a specific career opportunity by its ID.

**Endpoint:** `GET /getinvolved/career/{id}/`

**Response:** Same as single item in results array above

### 3. Get Career Opportunity by Slug
Get a specific career opportunity by its slug.

**Endpoint:** `GET /getinvolved/career/slug/{slug}/`

**Example:** `GET /getinvolved/career/slug/policy-research-analyst/`

**Response:** Same as single item in results array above

### 4. Get Featured Career Opportunities
Get all featured and open career opportunities.

**Endpoint:** `GET /getinvolved/career/featured/`

**Response:** Array of career opportunities

### 5. Get Open Career Opportunities
Get all open career opportunities.

**Endpoint:** `GET /getinvolved/career/open/`

**Response:** Array of career opportunities

### 6. Get Career Opportunities by Type
Get career opportunities filtered by type.

**Endpoint:** `GET /getinvolved/career/by_type/?type={type}`

**Query Parameters:**
- `type` (string, required): Opportunity type (`Full-time`, `Internship`, `Fellowship`, `Consultancy`, `Part-time`)

**Example:** `GET /getinvolved/career/by_type/?type=Internship`

**Response:** Array of career opportunities

## Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique identifier for the opportunity |
| title | string | Job title or position name |
| type | string | Type of opportunity (Full-time, Internship, Fellowship, Consultancy, Part-time) |
| location | string | Location of the position |
| department | string (optional) | Department or team name |
| description | text | Full description of the position |
| responsibilities | text | Key responsibilities and duties |
| requirements | text | Required qualifications and skills |
| how_to_apply | text | Application instructions |
| deadline | date | Application deadline (YYYY-MM-DD) |
| posted_date | date | Date the opportunity was posted (YYYY-MM-DD) |
| status | string | Current status (open or closed) |
| featured | boolean | Whether the opportunity is featured |
| image | string (URL, optional) | Image URL for the opportunity |
| slug | string | URL-friendly version of the title |
| created_at | datetime | Timestamp when created |
| updated_at | datetime | Timestamp when last updated |

## Example Usage

### Get all open opportunities
```bash
curl https://cepa-backend-production.up.railway.app/getinvolved/career/open/
```

### Search for internships in Kampala
```bash
curl "https://cepa-backend-production.up.railway.app/getinvolved/career/?type=Internship&location=Kampala,%20Uganda"
```

### Get featured opportunities
```bash
curl https://cepa-backend-production.up.railway.app/getinvolved/career/featured/
```

### Search opportunities by keyword
```bash
curl "https://cepa-backend-production.up.railway.app/getinvolved/career/?search=policy%20research"
```

## Error Responses

### 404 Not Found
```json
{
  "error": "Career opportunity not found"
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
