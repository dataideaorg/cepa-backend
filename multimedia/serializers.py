from rest_framework import serializers
from main.utils import get_full_media_url
from .models import (
    Podcast, Video, GalleryGroup, GalleryImage,
    Poll, PollOption, PollVote, XPollEmbed,
    Trivia, TriviaQuestion, TriviaOption,
)


class PodcastSerializer(serializers.ModelSerializer):
    """Serializer for Podcast model"""
    embed_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Podcast
        fields = [
            'id', 'title', 'description', 'youtube_id', 'youtube_url', 
            'thumbnail', 'duration', 'category', 'guest', 'featured', 
            'date', 'embed_url', 'created_at', 'updated_at'
        ]


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Video model"""
    embed_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'youtube_id', 'youtube_url', 
            'thumbnail', 'duration', 'category', 'featured', 
            'date', 'embed_url', 'created_at', 'updated_at'
        ]


class GalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for GalleryImage model"""
    image = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'alt_text', 'image', 'caption', 'order',
            'created_at', 'updated_at'
        ]

    def get_image(self, obj):
        """Get absolute URL for the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class GalleryGroupSerializer(serializers.ModelSerializer):
    """Serializer for GalleryGroup model with nested images"""
    images = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()

    class Meta:
        model = GalleryGroup
        fields = [
            'id', 'title', 'description', 'featured', 'date',
            'images', 'image_count', 'created_at', 'updated_at'
        ]

    def get_images(self, obj):
        """Get images with proper context for absolute URLs"""
        images = obj.images.all().order_by('order', 'created_at')
        return GalleryImageSerializer(images, many=True, context=self.context).data

    def get_image_count(self, obj):
        """Get the number of images in this group"""
        return obj.images.count()


class GalleryGroupListSerializer(serializers.ModelSerializer):
    """Simplified serializer for GalleryGroup list view"""
    image_count = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryGroup
        fields = [
            'id', 'title', 'description', 'featured', 'date', 
            'image_count', 'thumbnail', 'created_at', 'updated_at'
        ]
    
    def get_image_count(self, obj):
        """Get the number of images in this group"""
        return obj.images.count()
    
    def get_thumbnail(self, obj):
        """Get the first image as thumbnail"""
        first_image = obj.images.first()
        if first_image and first_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None


class PollOptionSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True)
    vote_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = PollOption
        fields = ['id', 'text', 'order', 'vote_count', 'vote_percentage', 'created_at']


class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True, read_only=True)
    total_votes = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Poll
        fields = [
            'id', 'title', 'description', 'category', 'status', 'status_display',
            'start_date', 'end_date', 'allow_multiple_votes', 'show_results_before_voting',
            'featured', 'options', 'total_votes', 'is_active', 'created_at', 'updated_at',
        ]


class XPollEmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = XPollEmbed
        fields = ['id', 'title', 'embed_html', 'order', 'created_at', 'updated_at']


class TriviaOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriviaOption
        fields = ['id', 'text', 'is_correct', 'order', 'created_at']


class TriviaQuestionSerializer(serializers.ModelSerializer):
    options = TriviaOptionSerializer(many=True, read_only=True)

    class Meta:
        model = TriviaQuestion
        fields = ['id', 'question_text', 'answer_text', 'options', 'order', 'created_at']


class TriviaListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Trivia
        fields = ['id', 'title', 'description', 'image', 'order', 'question_count', 'created_at', 'updated_at']

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None

    def get_question_count(self, obj):
        return obj.questions.count()


class TriviaDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    questions = TriviaQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Trivia
        fields = ['id', 'title', 'description', 'image', 'order', 'questions', 'created_at', 'updated_at']

    def get_image(self, obj):
        if obj.image:
            return get_full_media_url(obj.image.url)
        return None
