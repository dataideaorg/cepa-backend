"""
Utility functions for the main app.
"""
from django.conf import settings
from decouple import config


def get_full_media_url(relative_url):
    """
    Convert a relative media URL to a full backend URL.
    """
    if not relative_url:
        return None
    if relative_url.startswith('/media/'):
        relative_url = relative_url[7:]
    elif relative_url.startswith('media/'):
        relative_url = relative_url[6:]
    full_media_url = getattr(settings, 'FULL_MEDIA_URL', None)
    if full_media_url:
        full_media_url = full_media_url.rstrip('/')
        return f"{full_media_url}/{relative_url}"
    if settings.DEBUG:
        return f"http://localhost:8000{settings.MEDIA_URL}{relative_url}"
    backend_domain = config('BACKEND_DOMAIN', default='https://cepa-backend-production.up.railway.app')
    return f"{backend_domain}{settings.MEDIA_URL}{relative_url}"
