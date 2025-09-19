# Railway Deployment Configuration

## Volume Configuration

### 1. Create Volume in Railway Dashboard
- Go to your Railway project dashboard
- Navigate to your Django service
- Click on "Volumes" tab
- Create a new volume with:
  - **Mount Path**: `/data/media`
  - **Size**: Choose appropriate size for your media files (e.g., 1GB or more)

### 2. Environment Variables
Set the following environment variables in Railway:

```
RAILWAY_ENVIRONMENT=production
RAILWAY_RUN_UID=0
```

- `RAILWAY_ENVIRONMENT`: Enables Railway-specific configuration in settings.py
- `RAILWAY_RUN_UID=0`: Ensures proper permissions for volume access

### 3. Database Configuration
Ensure these PostgreSQL environment variables are set (Railway usually sets these automatically):
```
PGDATABASE=your_database_name
PGUSER=your_database_user
PGPASSWORD=your_database_password
PGHOST=your_database_host
PGPORT=your_database_port
```

### 4. Other Environment Variables
```
DEBUG=false
SECRET_KEY=your_production_secret_key
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

## File Structure on Railway

With the volume mounted at `/data/media`, your uploaded files will be stored as:
- Blog images: `/data/media/blog/images/`
- Event images: `/data/media/events/images/`
- News images: `/data/media/news/images/`
- Publication PDFs: `/data/media/publications/pdfs/`

## Local Development vs Production

### Local Development
- Media files stored in: `backend/media/`
- Uses SQLite database
- Debug mode enabled

### Railway Production
- Media files stored in: `/data/media/` (persistent volume)
- Uses PostgreSQL database
- Debug mode disabled
- Static files served by WhiteNoise

## Deployment Commands

The following commands will be run automatically by Railway:
```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

## Verification

After deployment, verify the volume is working:
1. Upload a file through your Django admin or API
2. Check that the file persists after redeployment
3. Ensure files are accessible via the media URL

