# CEPA Resources API Documentation

## Overview
This API provides access to CEPA's resources including blog posts, news articles, publications, and events. All endpoints return JSON data with pagination support.

## Base URL
```
http://localhost:8000/resources/
```

## Authentication
Currently, the API is open for read operations. Admin operations (POST, PUT, DELETE) require authentication (to be implemented).

## Response Format

### List Endpoints
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [...]
}
```

### Single Item Response
```json
{
  "id": "...",
  "title": "...",
  // ... all fields
}
```

## Endpoints

### Blog Posts

#### Get All Blog Posts
```
GET /resources/blog/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)
- `category`: Filter by category
- `featured`: Filter by featured status (true/false)
- `search`: Search in title, description, content
- `ordering`: Order by field (prefix with - for descending)

**Example:**
```
GET /resources/blog/?category=Education&featured=true&search=policy
```

#### Get Featured Blog Posts
```
GET /resources/blog/featured/
```

#### Get Blog Post by Slug
```
GET /resources/blog/by_slug/{slug}/
```

#### Get Single Blog Post
```
GET /resources/blog/{id}/
```

#### Create Blog Post (Admin)
```
POST /resources/blog/
Content-Type: application/json

{
  "id": "unique-id",
  "title": "Blog Post Title",
  "date": "January 2024",
  "category": "Education",
  "description": "Blog post description",
  "image": "/blog/image.jpg",
  "slug": "blog-post-slug",
  "featured": false,
  "content": "Full HTML content"
}
```

#### Update Blog Post (Admin)
```
PUT /resources/blog/{id}/
```

#### Delete Blog Post (Admin)
```
DELETE /resources/blog/{id}/
```

### News Articles

#### Get All News Articles
```
GET /resources/news/
```
**Query Parameters:** Same as blog posts

#### Get Featured News Articles
```
GET /resources/news/featured/
```

#### Get News Article by Slug
```
GET /resources/news/by_slug/{slug}/
```

#### Get Single News Article
```
GET /resources/news/{id}/
```

#### Create/Update/Delete News Article (Admin)
```
POST /resources/news/
PUT /resources/news/{id}/
DELETE /resources/news/{id}/
```

### Publications

#### Get All Publications
```
GET /resources/publications/
```
**Query Parameters:**
- `type`: Filter by publication type (Policy Brief, Policy Paper, Research Report, Analysis)
- `category`: Filter by category
- `featured`: Filter by featured status
- `search`: Search in title, description

#### Get Featured Publications
```
GET /resources/publications/featured/
```

#### Get Single Publication
```
GET /resources/publications/{id}/
```

#### Create/Update/Delete Publication (Admin)
```
POST /resources/publications/
PUT /resources/publications/{id}/
DELETE /resources/publications/{id}/
```

### Events

#### Get All Events
```
GET /resources/events/
```
**Query Parameters:**
- `category`: Filter by category (Conference, Meeting, Workshop, Seminar, Training, Validation Meeting)
- `status`: Filter by status (upcoming, completed, cancelled)
- `featured`: Filter by featured status
- `search`: Search in title, description, location

#### Get Featured Events
```
GET /resources/events/featured/
```

#### Get Upcoming Events
```
GET /resources/events/upcoming/
```

#### Get Past Events
```
GET /resources/events/past/
```

#### Get Event by Slug
```
GET /resources/events/by_slug/{slug}/
```

#### Get Single Event
```
GET /resources/events/{id}/
```

#### Create/Update/Delete Event (Admin)
```
POST /resources/events/
PUT /resources/events/{id}/
DELETE /resources/events/{id}/
```

### Homepage

#### Get Latest Updates
```
GET /resources/homepage/latest/
```

Returns featured items from all resource types:
```json
{
  "featured_blog_posts": [...],
  "featured_news_articles": [...],
  "featured_publications": [...],
  "featured_events": [...]
}
```

## Data Models

### BlogPost
```json
{
  "id": "string (primary key)",
  "title": "string",
  "date": "string",
  "category": "string",
  "description": "string",
  "image": "string (URL path)",
  "slug": "string (unique)",
  "featured": "boolean",
  "content": "string (HTML, optional)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### NewsArticle
```json
{
  "id": "string (primary key)",
  "title": "string",
  "date": "string",
  "category": "string",
  "description": "string",
  "image": "string (URL path)",
  "slug": "string (unique)",
  "featured": "boolean",
  "content": "string (HTML, optional)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Publication
```json
{
  "id": "string (primary key)",
  "title": "string",
  "type": "string (Policy Brief|Policy Paper|Research Report|Analysis)",
  "date": "string",
  "description": "string",
  "category": "string",
  "url": "string (URL, optional)",
  "pdf": "string (file path, optional)",
  "featured": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Event
```json
{
  "id": "string (primary key)",
  "title": "string",
  "date": "string",
  "time": "string",
  "location": "string",
  "category": "string",
  "description": "string",
  "image": "string (URL path)",
  "slug": "string (unique)",
  "featured": "boolean",
  "status": "string (upcoming|completed|cancelled)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Error Responses

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Examples

### Get all featured blog posts
```bash
curl http://localhost:8000/resources/blog/featured/
```

### Search for road safety content
```bash
curl "http://localhost:8000/resources/blog/?search=road%20safety"
```

### Get upcoming events
```bash
curl http://localhost:8000/resources/events/upcoming/
```

### Get homepage latest updates
```bash
curl http://localhost:8000/resources/homepage/latest/
```

## Database Status
- **Blog Posts**: 10 items (3 featured)
- **News Articles**: 10 items (3 featured)
- **Publications**: 6 items (3 featured)
- **Events**: 8 items (2 featured, 2 upcoming, 6 completed)

## Next Steps
1. Implement authentication for admin operations
2. Add file upload functionality for images and PDFs
3. Implement caching for better performance
4. Add rate limiting
5. Create admin panel for content management
