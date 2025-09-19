from django.core.management.base import BaseCommand
from django.conf import settings
from resources.models import upload_to_blog_images, upload_to_event_images, upload_to_news_images, upload_to_publication_pdfs
import os


class Command(BaseCommand):
    help = 'Test upload path configuration and media directory setup'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing upload configuration...'))
        
        # Test media root configuration
        self.stdout.write(f'MEDIA_ROOT: {settings.MEDIA_ROOT}')
        self.stdout.write(f'MEDIA_URL: {settings.MEDIA_URL}')
        
        # Check if media directory exists
        if os.path.exists(settings.MEDIA_ROOT):
            self.stdout.write(self.style.SUCCESS(f'✓ Media directory exists: {settings.MEDIA_ROOT}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Media directory does not exist: {settings.MEDIA_ROOT}'))
            self.stdout.write('Creating media directory...')
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            self.stdout.write(self.style.SUCCESS('✓ Media directory created'))
        
        # Test upload path functions
        test_paths = {
            'Blog images': upload_to_blog_images(None, 'test.jpg'),
            'Event images': upload_to_event_images(None, 'test.jpg'),
            'News images': upload_to_news_images(None, 'test.jpg'),
            'Publication PDFs': upload_to_publication_pdfs(None, 'test.pdf'),
        }
        
        self.stdout.write('\nUpload path configuration:')
        for name, path in test_paths.items():
            full_path = os.path.join(settings.MEDIA_ROOT, path)
            directory = os.path.dirname(full_path)
            
            self.stdout.write(f'{name}: {path}')
            
            # Create directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created directory: {directory}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Directory exists: {directory}'))
        
        # Check Railway environment
        if os.environ.get('RAILWAY_ENVIRONMENT'):
            self.stdout.write(self.style.SUCCESS('\n✓ Railway environment detected'))
            self.stdout.write(f'Using Railway volume path: {settings.MEDIA_ROOT}')
        else:
            self.stdout.write(self.style.SUCCESS('\n✓ Local development environment'))
            self.stdout.write(f'Using local media path: {settings.MEDIA_ROOT}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Upload configuration test completed successfully!'))
