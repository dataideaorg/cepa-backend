import os
import zipfile
import tempfile
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


def get_folder_size(folder_path):
    """Calculate the total size of a folder in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    return total_size


def format_size(size_bytes):
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def count_files(folder_path):
    """Count total number of files in a folder recursively."""
    count = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        count += len(filenames)
    return count


@staff_member_required
def media_folders_list(request):
    """
    View to list all folders in the media directory.
    Only accessible to staff members.
    """
    media_root = settings.MEDIA_ROOT
    folders = []
    
    if os.path.exists(media_root):
        for item in sorted(os.listdir(media_root)):
            item_path = os.path.join(media_root, item)
            if os.path.isdir(item_path):
                folder_size = get_folder_size(item_path)
                file_count = count_files(item_path)
                folders.append({
                    'name': item,
                    'size': format_size(folder_size),
                    'size_bytes': folder_size,
                    'file_count': file_count,
                })
    
    context = {
        'folders': folders,
        'media_root': media_root,
        'title': 'Media Folder Downloads',
    }
    return render(request, 'admin/media_downloads.html', context)


@staff_member_required
def download_media_folder(request, folder_name):
    """
    View to download a specific media folder as a zip file.
    Only accessible to staff members.
    """
    media_root = settings.MEDIA_ROOT
    folder_path = os.path.join(media_root, folder_name)
    
    # Security check: ensure the folder exists and is within media root
    if not os.path.exists(folder_path):
        raise Http404(f"Folder '{folder_name}' not found")
    
    # Ensure we're not accessing files outside media root
    folder_path = os.path.abspath(folder_path)
    media_root = os.path.abspath(media_root)
    if not folder_path.startswith(media_root):
        raise Http404("Invalid folder path")
    
    if not os.path.isdir(folder_path):
        raise Http404(f"'{folder_name}' is not a directory")
    
    # Create a temporary zip file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
        zip_path = tmp_file.name
    
    try:
        # Create the zip file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate the archive name (relative path within the folder)
                    arcname = os.path.join(
                        folder_name,
                        os.path.relpath(file_path, folder_path)
                    )
                    zipf.write(file_path, arcname)
        
        # Read the zip file and return as response
        with open(zip_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{folder_name}.zip"'
            return response
    finally:
        # Clean up the temporary file
        if os.path.exists(zip_path):
            os.remove(zip_path)
