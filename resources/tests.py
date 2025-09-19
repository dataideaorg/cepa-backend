from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os
import tempfile
from datetime import date, time
from PIL import Image
from .models import BlogPost, NewsArticle, Event, Publication


class ImageUploadTestCase(TestCase):
    """Test cases for image upload functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary image file for testing
        self.test_image = self.create_test_image()
    
    def create_test_image(self):
        """Create a temporary test image"""
        # Create a temporary image file
        image = Image.new('RGB', (100, 100), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name, 'JPEG')
        temp_file.seek(0)
        
        # Create Django uploadedfile
        with open(temp_file.name, 'rb') as f:
            uploaded_file = SimpleUploadedFile(
                name='test_image.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
        
        # Clean up temp file
        os.unlink(temp_file.name)
        return uploaded_file
    
    def test_blogpost_image_upload(self):
        """Test BlogPost image upload"""
        blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            date=date(2025, 9, 19),
            category="Test",
            description="Test description",
            image=self.test_image,
            slug="test-blog-post"
        )
        
        self.assertTrue(blog_post.image)
        self.assertTrue(blog_post.image.name.startswith('blog/images/'))
        
        # Check if file exists in media directory
        full_path = os.path.join(settings.MEDIA_ROOT, blog_post.image.name)
        self.assertTrue(os.path.exists(full_path))
    
    def test_news_article_image_upload(self):
        """Test NewsArticle image upload"""
        news_article = NewsArticle.objects.create(
            title="Test News Article",
            date=date(2025, 9, 19),
            category="Test",
            description="Test description",
            image=self.create_test_image(),
            slug="test-news-article"
        )
        
        self.assertTrue(news_article.image)
        self.assertTrue(news_article.image.name.startswith('news/images/'))
    
    def test_event_image_upload(self):
        """Test Event image upload"""
        event = Event.objects.create(
            title="Test Event",
            date=date(2025, 9, 19),
            time=time(10, 0),
            location="Test Location",
            category="Test",
            description="Test description",
            image=self.create_test_image(),
            slug="test-event"
        )
        
        self.assertTrue(event.image)
        self.assertTrue(event.image.name.startswith('events/images/'))
    
    def test_publication_pdf_upload(self):
        """Test Publication PDF upload"""
        # Create a temporary PDF file
        pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
        pdf_file = SimpleUploadedFile(
            name='test_publication.pdf',
            content=pdf_content,
            content_type='application/pdf'
        )
        
        publication = Publication.objects.create(
            title="Test Publication",
            type="Policy Brief",
            date=date(2025, 9, 19),
            description="Test description",
            category="Test",
            pdf=pdf_file
        )
        
        self.assertTrue(publication.pdf)
        self.assertTrue(publication.pdf.name.startswith('publications/pdfs/'))
    
    def test_uuid_generation(self):
        """Test that UUID is automatically generated for new objects"""
        blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            date=date(2025, 9, 19),
            category="Test",
            description="Test description",
            slug="test-blog-post-uuid"
        )
        
        self.assertTrue(blog_post.id)
        self.assertEqual(len(blog_post.id), 36)  # UUID4 length
    
    def test_date_field_functionality(self):
        """Test that date fields work properly"""
        # Test BlogPost date field
        blog_post = BlogPost.objects.create(
            title="Date Test Blog Post",
            date=date(2025, 12, 25),
            category="Test",
            description="Testing date functionality",
            slug="date-test-blog"
        )
        
        self.assertEqual(blog_post.date, date(2025, 12, 25))
        self.assertEqual(blog_post.date.year, 2025)
        self.assertEqual(blog_post.date.month, 12)
        self.assertEqual(blog_post.date.day, 25)
        
        # Test Event date and time fields
        event = Event.objects.create(
            title="Date Test Event",
            date=date(2025, 12, 31),
            time=time(23, 59),
            location="Test Location",
            category="Test",
            description="Testing date and time functionality",
            slug="date-test-event"
        )
        
        self.assertEqual(event.date, date(2025, 12, 31))
        self.assertEqual(event.time, time(23, 59))
        self.assertEqual(event.time.hour, 23)
        self.assertEqual(event.time.minute, 59)
        
        # Test filtering by date
        events_on_date = Event.objects.filter(date=date(2025, 12, 31))
        self.assertEqual(events_on_date.count(), 1)
        self.assertEqual(events_on_date.first(), event)
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up any uploaded files
        for model in [BlogPost, NewsArticle, Event, Publication]:
            for obj in model.objects.all():
                if hasattr(obj, 'image') and obj.image:
                    if os.path.exists(obj.image.path):
                        os.remove(obj.image.path)
                if hasattr(obj, 'pdf') and obj.pdf:
                    if os.path.exists(obj.pdf.path):
                        os.remove(obj.pdf.path)
