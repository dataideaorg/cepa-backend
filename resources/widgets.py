from django import forms
from django.utils.safestring import mark_safe
import json


class QuillEditorWidget(forms.Textarea):
    """
    Custom Django widget for Quill Rich Text Editor
    Free and open-source WYSIWYG editor
    Displays toolbar on top with content editor below
    """

    class Media:
        css = {
            'all': (
                'https://cdn.quilljs.com/1.3.6/quill.snow.css',
            )
        }
        js = (
            'https://cdn.quilljs.com/1.3.6/quill.js',
        )

    def _get_css(self):
        """Return CSS to ensure vertical layout"""
        return """
        <style>
        /* Quill vertical layout - CRITICAL overrides */
        .quill-container-wrapper {
            display: flex !important;
            flex-direction: column !important;
            width: 100% !important;
            gap: 0 !important;
        }

        /* Toolbar at top */
        .quill-container-wrapper .ql-toolbar {
            order: -1 !important;
            width: 100% !important;
            border-radius: 4px 4px 0 0 !important;
            background-color: #f5f5f5 !important;
            padding: 8px !important;
            border-bottom: 2px solid #ddd !important;
        }

        /* Editor content below */
        .quill-container-wrapper .ql-container {
            order: 1 !important;
            min-height: 400px !important;
            border-radius: 0 0 4px 4px !important;
            border: 1px solid #ddd !important;
            border-top: none !important;
        }

        /* Content area styling */
        .quill-container-wrapper .ql-editor {
            min-height: 380px !important;
            padding: 15px !important;
        }

        .quill-container-wrapper .ql-editor.ql-blank::before {
            color: #999 !important;
            font-style: italic !important;
        }
        </style>
        """

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'quill-editor',
            'data-theme': 'snow',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Get the base textarea
        html = super().render(name, value, attrs, renderer)

        # Generate a unique ID for this editor
        editor_id = attrs.get('id', f'id_{name}') if attrs else f'id_{name}'

        # Quill configuration with toolbar on top
        quill_config = {
            'theme': 'snow',
            'modules': {
                'toolbar': [
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{'list': 'ordered'}, {'list': 'bullet'}],
                    [{'header': [1, 2, 3, 4, 5, 6, False]}],
                    ['link', 'image', 'video'],
                    ['clean']
                ]
            },
            'placeholder': 'Write your content here...',
            'readOnly': False,
        }

        # Create JavaScript to initialize Quill
        js_code = f"""
        <script>
        (function() {{
            // Wait for Quill to load
            if (typeof Quill !== 'undefined') {{
                // Initialize Quill editor
                const editor = new Quill('#{editor_id}_editor', {json.dumps(quill_config)});

                // Get the hidden textarea
                const textarea = document.getElementById('{editor_id}');

                // Sync Quill content to textarea on input
                editor.on('text-change', function() {{
                    textarea.value = editor.root.innerHTML;
                    // Trigger change event for Django admin
                    const event = new Event('change', {{ bubbles: true }});
                    textarea.dispatchEvent(event);
                }});

                // Set initial content if textarea has value
                if (textarea.value) {{
                    editor.root.innerHTML = textarea.value;
                }}

                // Hide the original textarea
                textarea.style.display = 'none';
            }} else {{
                console.warn('Quill library not loaded');
            }}
        }})();
        </script>
        """

        # Create the Quill editor container with wrapper class for CSS styling
        editor_html = f'''
        <div id="{editor_id}_editor" class="quill-container-wrapper"></div>
        '''

        # Combine CSS, editor HTML, hidden textarea, and JavaScript
        return mark_safe(self._get_css() + editor_html + html + js_code)