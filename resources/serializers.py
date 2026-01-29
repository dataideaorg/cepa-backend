from rest_framework import serializers
from .models import BlogPost, NewsArticle, Publication, Event, BlogComment, NewsComment


class BlogCommentSerializer(serializers.ModelSerializer):
    """Serializer for BlogComment model"""

    class Meta:
        model = BlogComment
        fields = ['id', 'post', 'author_name', 'author_email', 'body', 'created_at']
        read_only_fields = ['id', 'post', 'created_at']


class NewsCommentSerializer(serializers.ModelSerializer):
    """Serializer for NewsComment model"""

    class Meta:
        model = NewsComment
        fields = ['id', 'article', 'author_name', 'author_email', 'body', 'created_at']
        read_only_fields = ['id', 'article', 'created_at']


class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model"""

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'date', 'category', 'description',
            'image', 'slug', 'featured', 'content', 'views_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'views_count']


class NewsArticleSerializer(serializers.ModelSerializer):
    """Serializer for NewsArticle model"""

    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'date', 'category', 'description',
            'image', 'slug', 'featured', 'content', 'views_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'views_count']


class PublicationSerializer(serializers.ModelSerializer):
    """Serializer for Publication model"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'type', 'date', 'description', 'category',
            'url', 'pdf', 'image', 'image_url', 'featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        """Return absolute URL for publication image if available"""
        if obj.image:
            from django.conf import settings
            base_url = settings.FULL_MEDIA_URL.rstrip('/') if hasattr(settings, 'FULL_MEDIA_URL') else settings.MEDIA_URL.rstrip('/')
            image_path = str(obj.image).lstrip('/')
            return f"{base_url}/{image_path}"
        return None


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'date', 'time', 'location', 'category', 
            'description', 'image', 'slug', 'featured', 'status', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class HomepageLatestSerializer(serializers.Serializer):
    """Serializer for homepage latest updates combining all resource types"""
    featured_blog_posts = BlogPostSerializer(many=True, read_only=True)
    featured_news_articles = NewsArticleSerializer(many=True, read_only=True)
    featured_publications = PublicationSerializer(many=True, read_only=True)
    featured_events = EventSerializer(many=True, read_only=True)
