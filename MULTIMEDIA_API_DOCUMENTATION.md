# Multimedia API Documentation

This document describes the multimedia API endpoints for podcasts, videos, and gallery management.

## Base URL
```
https://cepa-backend-production.up.railway.app/multimedia/
```

## Authentication
All endpoints require authentication (if configured).

## Podcasts API

### Endpoints

#### List All Podcasts
```http
GET /multimedia/podcasts/
```

**Response:**
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "title": "Podcast Title",
      "description": "Podcast description",
      "youtube_id": "video_id",
      "youtube_url": "https://youtube.com/watch?v=video_id",
      "thumbnail": "https://example.com/thumbnail.jpg",
      "duration": "15:30",
      "category": "Policy Digest Podcast",
      "guest": "Guest Name",
      "featured": true,
      "date": "2025-01-15",
      "embed_url": "https://www.youtube.com/embed/video_id?autoplay=1&rel=0",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

#### Get Featured Podcasts
```http
GET /multimedia/podcasts/featured/
```

#### Get Podcasts by Category
```http
GET /multimedia/podcasts/by_category/?category=Policy%20Digest
```

#### Get All Categories
```http
GET /multimedia/podcasts/categories/
```

#### Create Podcast
```http
POST /multimedia/podcasts/
Content-Type: application/json

{
  "title": "New Podcast Episode",
  "description": "Episode description",
  "youtube_id": "video_id_here",
  "youtube_url": "https://youtube.com/watch?v=video_id_here",
  "duration": "20:45",
  "category": "Policy Analysis",
  "guest": "Expert Name",
  "featured": false,
  "date": "2025-01-15"
}
```

## Videos API

### Endpoints

#### List All Videos
```http
GET /multimedia/videos/
```

**Response:**
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "title": "Video Title",
      "description": "Video description",
      "youtube_id": "video_id",
      "youtube_url": "https://youtube.com/watch?v=video_id",
      "thumbnail": "https://example.com/thumbnail.jpg",
      "duration": "18:20",
      "category": "Political Analysis",
      "featured": true,
      "date": "2025-01-15",
      "embed_url": "https://www.youtube.com/embed/video_id?autoplay=1&rel=0",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

#### Get Featured Videos
```http
GET /multimedia/videos/featured/
```

#### Get Videos by Category
```http
GET /multimedia/videos/by_category/?category=Political%20Analysis
```

#### Get All Categories
```http
GET /multimedia/videos/categories/
```

## Gallery API

### Gallery Groups

#### List All Gallery Groups
```http
GET /multimedia/gallery-groups/
```

**Response:**
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "title": "Gallery Group Title",
      "description": "Group description",
      "featured": true,
      "date": "2025-01-15",
      "image_count": 5,
      "thumbnail": "https://example.com/thumbnail.jpg",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

#### Get Featured Gallery Groups
```http
GET /multimedia/gallery-groups/featured/
```

#### Get Gallery Group with Images
```http
GET /multimedia/gallery-groups/{id}/
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Gallery Group Title",
  "description": "Group description",
  "featured": true,
  "date": "2025-01-15",
  "images": [
    {
      "id": "uuid",
      "title": "Image Title",
      "alt_text": "Alt text for accessibility",
      "image": "https://example.com/image.jpg",
      "caption": "Image caption",
      "order": 1,
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    }
  ],
  "image_count": 1,
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

#### Get Images for a Gallery Group
```http
GET /multimedia/gallery-groups/{id}/images/
```

#### Add Image to Gallery Group
```http
POST /multimedia/gallery-groups/{id}/add_image/
Content-Type: multipart/form-data

{
  "title": "Image Title",
  "alt_text": "Alt text",
  "image": <file>,
  "caption": "Image caption",
  "order": 1
}
```

### Gallery Images

#### List All Gallery Images
```http
GET /multimedia/gallery-images/
```

#### Filter Images by Gallery Group
```http
GET /multimedia/gallery-images/?group={group_id}
```

#### Get Featured Images
```http
GET /multimedia/gallery-images/featured/
```

## Data Models

### Podcast Model
- `id`: Unique identifier (UUID)
- `title`: Podcast episode title
- `description`: Episode description
- `youtube_id`: YouTube video ID for embedding
- `youtube_url`: Full YouTube URL (optional)
- `thumbnail`: Thumbnail image (optional)
- `duration`: Duration in MM:SS format
- `category`: Podcast category
- `guest`: Guest speaker name (optional)
- `featured`: Boolean for featured status
- `date`: Publication date
- `embed_url`: Auto-generated YouTube embed URL

### Video Model
- `id`: Unique identifier (UUID)
- `title`: Video title
- `description`: Video description
- `youtube_id`: YouTube video ID for embedding
- `youtube_url`: Full YouTube URL (optional)
- `thumbnail`: Thumbnail image (optional)
- `duration`: Duration in MM:SS format
- `category`: Video category
- `featured`: Boolean for featured status
- `date`: Publication date
- `embed_url`: Auto-generated YouTube embed URL

### GalleryGroup Model
- `id`: Unique identifier (UUID)
- `title`: Gallery group title
- `description`: Group description (optional)
- `featured`: Boolean for featured status
- `date`: Creation date
- `images`: Related gallery images (nested)

### GalleryImage Model
- `id`: Unique identifier (UUID)
- `group`: Foreign key to GalleryGroup
- `title`: Image title
- `alt_text`: Alt text for accessibility
- `image`: Image file
- `caption`: Image caption (optional)
- `order`: Display order within group

## File Uploads

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

### Upload Paths
- Podcast thumbnails: `podcasts/thumbnails/{podcast_id}/`
- Video thumbnails: `videos/thumbnails/{video_id}/`
- Gallery images: `gallery/images/{image_id}/`

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "A server error occurred."
}
```

## Usage Examples

### Frontend Integration

#### Fetching Featured Podcasts
```javascript
const response = await fetch('https://cepa-backend-production.up.railway.app/multimedia/podcasts/featured/');
const podcasts = await response.json();
```

#### Fetching Gallery with Images
```javascript
const response = await fetch('https://cepa-backend-production.up.railway.app/multimedia/gallery-groups/');
const galleryGroups = await response.json();
```

#### Creating a New Podcast
```javascript
const podcastData = {
  title: "New Episode",
  description: "Episode description",
  youtube_id: "video_id",
  duration: "15:30",
  category: "Policy Analysis",
  featured: true,
  date: "2025-01-15"
};

const response = await fetch('https://cepa-backend-production.up.railway.app/multimedia/podcasts/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(podcastData)
});
```
