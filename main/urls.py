from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resources/', include('resources.urls')),
    path('multimedia/', include('multimedia.urls')),
    path('contact/', include('contact.urls')),
]

# Serve media files
if settings.DEBUG or settings.RAILWAY_ENVIRONMENT_NAME:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
