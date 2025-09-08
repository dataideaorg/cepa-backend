# **Backend Migration Prompt for CEPA Resources**

## **Context & Objective**
You need to migrate the CEPA website's resource management system from frontend hardcoded data to a proper backend API. The frontend currently has hardcoded arrays of blog posts, news articles, publications, and events that need to be moved to a backend database with proper API endpoints.

## **Current Frontend Structure Analysis**

### **Resource Types & Data Structures**

**1. Blog Posts** (`/resources/blog/`)
```typescript
interface BlogPost {
  id: string;
  title: string;
  date: string;
  category: string;
  description: string;
  image: string;
  slug: string;
  featured: boolean;
  content?: string; // Full HTML content for detail pages
}
```

**2. News Articles** (`/resources/news/`)
```typescript
interface NewsArticle {
  id: string;
  title: string;
  date: string;
  category: string;
  description: string;
  image: string;
  slug: string;
  featured: boolean;
  content?: string; // Full HTML content for detail pages
}
```

**3. Publications** (`/resources/publications/`)
```typescript
interface Publication {
  id: string;
  title: string;
  type: string; // "Policy Brief", "Policy Paper", "Research Report", etc.
  date: string;
  description: string;
  category: string;
  url?: string; // External link
  pdf?: string; // PDF file path
  featured: boolean;
}
```

**4. Events** (`/resources/events/`)
```typescript
interface Event {
  id: string;
  title: string;
  date: string;
  time: string;
  location: string;
  category: string; // "Conference", "Meeting", "Workshop", "Seminar", "Training", "Validation Meeting"
  description: string;
  image: string;
  slug: string;
  featured: boolean;
  status: "upcoming" | "completed" | "cancelled";
}
```

### **Current Frontend Pages Structure**
- **List Pages**: `/resources/blog/`, `/resources/news/`, `/resources/publications/`, `/resources/events/`
- **Detail Pages**: `/resources/blog/[slug]/`, `/resources/news/[slug]/`, `/resources/events/[slug]/`
- **Homepage Integration**: Latest Updates section displays featured items from all resource types

## **Required Backend Implementation**

### **1. Database Schema**

Create tables for each resource type with the following structure:

**Blog Posts Table**
```sql
CREATE TABLE blog_posts (
  id VARCHAR(255) PRIMARY KEY,
  title TEXT NOT NULL,
  date VARCHAR(50) NOT NULL,
  category VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  image VARCHAR(500) NOT NULL,
  slug VARCHAR(500) UNIQUE NOT NULL,
  featured BOOLEAN DEFAULT FALSE,
  content LONGTEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**News Articles Table**
```sql
CREATE TABLE news_articles (
  id VARCHAR(255) PRIMARY KEY,
  title TEXT NOT NULL,
  date VARCHAR(50) NOT NULL,
  category VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  image VARCHAR(500) NOT NULL,
  slug VARCHAR(500) UNIQUE NOT NULL,
  featured BOOLEAN DEFAULT FALSE,
  content LONGTEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Publications Table**
```sql
CREATE TABLE publications (
  id VARCHAR(255) PRIMARY KEY,
  title TEXT NOT NULL,
  type VARCHAR(100) NOT NULL,
  date VARCHAR(50) NOT NULL,
  description TEXT NOT NULL,
  category VARCHAR(100) NOT NULL,
  url VARCHAR(1000),
  pdf VARCHAR(500),
  featured BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Events Table**
```sql
CREATE TABLE events (
  id VARCHAR(255) PRIMARY KEY,
  title TEXT NOT NULL,
  date VARCHAR(50) NOT NULL,
  time VARCHAR(50) NOT NULL,
  location VARCHAR(200) NOT NULL,
  category VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  image VARCHAR(500) NOT NULL,
  slug VARCHAR(500) UNIQUE NOT NULL,
  featured BOOLEAN DEFAULT FALSE,
  status ENUM('upcoming', 'completed', 'cancelled') DEFAULT 'upcoming',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### **2. API Endpoints Required**

**Blog Posts API**
```
GET /api/blog - Get all blog posts (with pagination, filtering, search)
GET /api/blog/featured - Get featured blog posts
GET /api/blog/[slug] - Get single blog post by slug
POST /api/blog - Create new blog post (admin)
PUT /api/blog/[id] - Update blog post (admin)
DELETE /api/blog/[id] - Delete blog post (admin)
```

**News Articles API**
```
GET /api/news - Get all news articles (with pagination, filtering, search)
GET /api/news/featured - Get featured news articles
GET /api/news/[slug] - Get single news article by slug
POST /api/news - Create new news article (admin)
PUT /api/news/[id] - Update news article (admin)
DELETE /api/news/[id] - Delete news article (admin)
```

**Publications API**
```
GET /api/publications - Get all publications (with pagination, filtering, search)
GET /api/publications/featured - Get featured publications
GET /api/publications/[id] - Get single publication by ID
POST /api/publications - Create new publication (admin)
PUT /api/publications/[id] - Update publication (admin)
DELETE /api/publications/[id] - Delete publication (admin)
```

**Events API**
```
GET /api/events - Get all events (with pagination, filtering, search)
GET /api/events/featured - Get featured events
GET /api/events/upcoming - Get upcoming events
GET /api/events/past - Get past events
GET /api/events/[slug] - Get single event by slug
POST /api/events - Create new event (admin)
PUT /api/events/[id] - Update event (admin)
DELETE /api/events/[id] - Delete event (admin)
```

**Homepage API**
```
GET /api/homepage/latest - Get latest updates for homepage (featured items from all resource types)
```

### **3. Data Migration Requirements**

**Extract and migrate all existing data from these frontend files:**
- `app/resources/blog/page.tsx` - Blog posts array
- `app/resources/news/page.tsx` - News articles array  
- `app/resources/publications/page.tsx` - Publications array
- `app/resources/events/page.tsx` - Events array
- `app/resources/blog/[slug]/page.tsx` - Blog post content
- `app/resources/news/[slug]/page.tsx` - News article content
- `app/resources/events/[slug]/page.tsx` - Event details
- `app/page.tsx` - Homepage latest updates data

### **4. API Response Format**

**List Endpoints Response:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 50,
    "totalPages": 5
  },
  "filters": {
    "category": "Education",
    "featured": true
  }
}
```

**Single Item Response:**
```json
{
  "data": {
    "id": "...",
    "title": "...",
    // ... all fields
  }
}
```

### **5. Frontend Integration Requirements**

After backend implementation, the frontend will need to:
1. Replace all hardcoded arrays with API calls
2. Implement loading states and error handling
3. Add pagination for list pages
4. Implement search and filtering functionality
5. Update the homepage to fetch latest updates from the API

### **6. Additional Features to Implement**

**Search & Filtering:**
- Full-text search across titles and descriptions
- Category filtering
- Date range filtering
- Featured items filtering

**Admin Panel:**
- CRUD operations for all resource types
- Image upload functionality
- Rich text editor for content
- Publication status management

**SEO Optimization:**
- Meta tags for each resource
- Structured data markup
- Sitemap generation

### **7. File Upload Requirements**

**Image Handling:**
- Upload and store images for blog posts, news articles, and events
- Generate multiple image sizes (thumbnails, medium, large)
- Store image metadata (alt text, dimensions, etc.)

**PDF Handling:**
- Upload and store PDF files for publications
- Generate PDF previews/thumbnails
- Track download statistics

### **8. Performance Considerations**

- Implement caching for frequently accessed data
- Use database indexing for search and filtering
- Optimize image delivery (WebP format, lazy loading)
- Implement pagination to handle large datasets

## **Success Criteria**

1. ✅ All hardcoded data successfully migrated to database
2. ✅ All API endpoints functional and tested
3. ✅ Frontend successfully integrated with backend APIs
4. ✅ Admin panel allows full CRUD operations
5. ✅ Search and filtering functionality working
6. ✅ Homepage latest updates dynamically populated
7. ✅ All existing functionality preserved
8. ✅ Performance optimized with proper caching
9. ✅ SEO-friendly URLs and meta tags maintained

## **Next Steps After Backend Completion**

Once the backend is ready, provide:
1. API documentation with all endpoints
2. Database schema and sample data
3. Authentication/authorization setup for admin operations
4. File upload configuration details
5. Environment variables and configuration requirements

Integrate these APIs and remove all hardcoded data arrays in the frontend.