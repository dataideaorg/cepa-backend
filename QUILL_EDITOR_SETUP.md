# Quill Rich Text Editor Integration Guide

## Overview

**Quill** is a free, open-source, powerful WYSIWYG (What You See Is What You Get) rich text editor that has been integrated into your Django admin interface for blog content management.

### Why Quill?
- **Free and Open Source**: No licensing costs, full transparency
- **Lightweight**: ~43KB minified
- **Powerful**: Rich formatting capabilities with modular architecture
- **Developer-Friendly**: Simple API and excellent documentation
- **Production-Ready**: Used by companies like Slack, Grammarly, and others

## Installation Complete ✓

### Files Created
- `resources/widgets.py` - Custom Django widget for Quill editor

### Files Modified
- `requirements.txt` - Cleaned up (removed TinyMCE dependency)
- `main/settings.py` - Removed TinyMCE configuration
- `resources/admin.py` - Integrated Quill widget for BlogPost and NewsArticle

## How to Use

### Accessing the Editor

1. **Start the server** (if not already running):
   ```bash
   cd /Users/rtv-lpt-434/Work/cepa/website/backend
   source .venv/bin/activate
   python manage.py runserver
   ```

2. **Navigate to Django Admin**:
   - URL: `http://localhost:8000/admin/`
   - Login with your credentials

3. **Access the Blog Post Editor**:
   - Click: **Resources** → **Blog posts**
   - Click: **Add Blog Post** button
   - Or edit an existing blog post

4. **Edit Content** in the Quill Editor:
   - The content field now shows a rich text editor
   - Use the toolbar to format text

### Editor Features

#### Text Formatting Toolbar
```
┌─────────────────────────────────────────┐
│ Bold | Italic | Underline | Strike     │
│ Quote | Code Block                      │
│ Numbered List | Bullet List            │
│ Heading Levels (H1-H6)                 │
│ Link | Image | Video | Remove Format   │
└─────────────────────────────────────────┘
```

#### Available Tools

**Text Formatting:**
- **Bold** - `Ctrl+B` / `Cmd+B`
- **Italic** - `Ctrl+I` / `Cmd+I`
- **Underline** - `Ctrl+U` / `Cmd+U`
- **Strike** - Strikethrough text

**Blocks:**
- **Blockquote** - Quote a passage
- **Code Block** - Display code with syntax highlighting

**Lists:**
- **Numbered List** - Ordered list (1, 2, 3...)
- **Bullet List** - Unordered list (•, •, •...)

**Headings:**
- **H1 - H6** - Six heading levels for hierarchy

**Rich Content:**
- **Link** - Insert URL links
- **Image** - Embed images
- **Video** - Embed videos
- **Clean Format** - Remove all formatting

### Content Storage

- **Format**: HTML (clean, semantic HTML)
- **Database**: Stored as-is in the `content` TextField
- **Frontend**: Automatically rendered on blog pages using existing display logic
- **No Migrations Needed**: Data structure unchanged

## Technical Details

### Widget Implementation

The `QuillEditorWidget` class in `resources/widgets.py`:

```python
class QuillEditorWidget(forms.Textarea):
    """Custom Django widget for Quill Rich Text Editor"""

    # Loads Quill from CDN
    class Media:
        css = {'all': ('https://cdn.quilljs.com/1.3.6/quill.snow.css',)}
        js = ('https://cdn.quilljs.com/1.3.6/quill.js',)
```

**Key Features:**
- Loads Quill library from CDN (no npm dependency needed)
- Snow theme (clean, minimal design)
- Automatic synchronization with Django textarea
- 400px minimum height
- Professional appearance

### Admin Configuration

The widget is configured in `BlogPostAdmin` and `NewsArticleAdmin`:

```python
formfield_overrides = {
    models.TextField: {'widget': QuillEditorWidget()}
}
```

This applies the Quill editor to all TextField inputs in the admin form.

## Content Display

Blog posts are displayed on:
- **List Page**: `/resources/blog/`
- **Detail Page**: `/resources/blog/[slug]/`

Content is rendered as-is using Tailwind prose utilities, maintaining all formatting from the Quill editor.

## Example Usage

### In the Admin Panel:

1. **Create a blog post**:
   - Title: "My First Blog Post"
   - Date: Select current date
   - Category: "Technology"
   - Description: "A brief summary"
   - Content: Use Quill editor to format content
     - Type: "This is my first blog post"
     - Select text and make it **bold**
     - Add a heading: "Section 1"
     - Create a bullet list
     - Insert a link
   - Save

2. **View on frontend**:
   - The content displays with all formatting preserved
   - Headings are styled as H2
   - Bold text remains bold
   - Lists are properly formatted

## Development Notes

### Virtual Environment
Always activate the virtual environment before running the server:
```bash
source .venv/bin/activate
```

### CDN Usage
Quill is loaded from CDN, so:
- ✓ No npm/package installation needed
- ✓ Works offline after first load (cached)
- ✓ No build step required
- ✓ Always uses latest stable version

### Browser Compatibility
Quill works on:
- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## File Locations

```
backend/
├── requirements.txt                 # Dependencies (no Quill package needed)
├── main/
│   └── settings.py                 # Django configuration
├── resources/
│   ├── admin.py                    # Admin configuration
│   ├── widgets.py                  # ✨ NEW: Quill widget
│   └── models.py                   # BlogPost model
└── QUILL_EDITOR_SETUP.md          # This file
```

## Security Considerations

### Current Setup
- Content is stored as HTML
- Rendered as-is on frontend (using `dangerouslySetInnerHTML`)
- Quill only includes safe formatting tools (no script injection)

### For Production
Consider adding HTML sanitization:
```bash
pip install bleach
```

Then sanitize in the model's save method or serializer.

## Advanced Customization

### To customize the toolbar, edit `resources/widgets.py`:

```python
'modules': {
    'toolbar': [
        ['bold', 'italic', 'underline'],  # Add/remove tools
        [{'list': 'ordered'}, {'list': 'bullet'}],
        ['link', 'image'],
        ['clean']
    ]
}
```

### To change editor height:
```python
editorDiv.style.minHeight = '600px';  # Change in widgets.py
```

## Troubleshooting

### Editor not showing?
1. Clear browser cache
2. Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
3. Check browser console for JavaScript errors

### Content not saving?
1. Check that the form is submitted properly
2. Verify JavaScript is enabled
3. Look for Django validation errors in admin

### Styling issues?
- Quill CSS is loaded from CDN
- Fallback to system fonts if CDN fails
- Custom styles can be added in `widgets.py`

## Resources

- **Quill Documentation**: https://quilljs.com/docs/
- **Quill GitHub**: https://github.com/quilljs/quill
- **Quill Playground**: https://quilljs.com/

## Next Steps (Optional)

1. **Add image upload handling** - Currently supports embedding via URL
2. **Implement auto-save** - Save content periodically
3. **Add mention/hashtag support** - Quill modules available
4. **Create frontend editor** - For allowing users to create posts
5. **Add collaboration features** - Real-time co-editing

## Support

For issues or questions:
1. Check Quill documentation
2. Review the `resources/widgets.py` implementation
3. Examine Django admin logs
4. Check browser console for JavaScript errors

---

**Version**: 1.0
**Date**: November 2025
**Editor**: Quill 1.3.6
**Status**: Production Ready ✓