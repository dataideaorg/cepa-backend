from rest_framework import serializers
from .models import BlogPost, NewsArticle, Publication, Event


class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model"""
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'date', 'category', 'description', 
            'image', 'slug', 'featured', 'content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NewsArticleSerializer(serializers.ModelSerializer):
    """Serializer for NewsArticle model"""
    
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'date', 'category', 'description', 
            'image', 'slug', 'featured', 'content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PublicationSerializer(serializers.ModelSerializer):
    """Serializer for Publication model"""
    
    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'type', 'date', 'description', 'category', 
            'url', 'pdf', 'featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


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
