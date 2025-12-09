from rest_framework import serializers
from .models import HeroSlide
from django.conf import settings


class HeroSlideSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSlide
        fields = ['id', 'title', 'image', 'image_url', 'order', 'is_active']

    def get_image_url(self, obj):
        """Return full URL for the image"""
        if obj.image:
            return settings.FULL_MEDIA_URL + str(obj.image)
        return None