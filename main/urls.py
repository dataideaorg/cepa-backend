from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='landing_page.html'), name='landing-page'),
    path('admin/', admin.site.urls),
    path('admin/media-folders/', views.media_folders_list, name='media_folders_list'),
    path('admin/media-folders/download/<str:folder_name>/', views.download_media_folder, name='download_media_folder'),
    path('resources/', include('resources.urls')),
    path('multimedia/', include('multimedia.urls')),
    path('contact/', include('contact.urls')),
    path('getinvolved/', include('getinvolved.urls')),
    path('fellowships/', include('fellowships.urls')),
    path('focus-area/', include('focusareas.urls')),
    path('about/', include('about.urls')),
    path('home/', include('home.urls')),
    path('chatbot/', include('chatbot.urls')),
]

# Serve media files
if settings.DEBUG or settings.RAILWAY_ENVIRONMENT_NAME:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
