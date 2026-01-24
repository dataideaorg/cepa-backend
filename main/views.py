import os
import zipfile
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.text import slugify


@staff_member_required
def media_folders_list(request):
    """List all folders in the media directory"""
    media_root = settings.MEDIA_ROOT
    
    if not os.path.exists(media_root):
        folders = []
    else:
        # Get all top-level directories in media folder
        folders = [
            item for item in os.listdir(media_root)
            if os.path.isdir(os.path.join(media_root, item))
        ]
        folders.sort()
    
    context = {
        'folders': folders,
        'media_root': media_root,
    }
    return render(request, 'admin/media_folders_list.html', context)


@staff_member_required
def download_media_folder(request, folder_name):
    """Download a folder from media directory as a zip file"""
    # Security: prevent directory traversal by removing any path separators
    folder_name = os.path.basename(folder_name)
    
    media_root = settings.MEDIA_ROOT
    folder_path = os.path.join(media_root, folder_name)
    
    # Security check: ensure the folder is within media_root
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        raise Http404("Folder not found")
    
    # Ensure the folder path is within media_root (prevent directory traversal)
    real_media_root = os.path.realpath(media_root)
    real_folder_path = os.path.realpath(folder_path)
    
    if not real_folder_path.startswith(real_media_root):
        raise Http404("Invalid folder path")
    
    # Create a zip file in memory
    response = HttpResponse(content_type='application/zip')
    zip_filename = f"{slugify(folder_name)}.zip"
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
    
    with zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Walk through the folder and add all files to the zip
        for root, dirs, files in os.walk(folder_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                # Skip hidden files
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                # Get relative path from folder_path
                arcname = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname)
    
    return response
