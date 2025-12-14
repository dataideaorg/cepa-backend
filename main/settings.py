from pathlib import Path
import os
from dotenv import load_dotenv
from decouple import config

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent   
RAILWAY_ENVIRONMENT_NAME = os.environ.get('RAILWAY_ENVIRONMENT_NAME')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l3b%4)v91w8os3x1c-puq(bgi8k#=*npvap3v0cuwv**esqs28'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    "https://cepa-backend-production.up.railway.app",
    "https://master.d1o07tzlhd1qin.amplifyapp.com",
    "https://cepa.or.ug",
    "https://www.cepa.or.ug",
    "https://cepa.or.ug",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'ckeditor',
    'resources',
    'multimedia',
    'contact',
    'getinvolved',
    'fellowships',
    'focusareas',
    'chatbot',
    'about',
    'home',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Make sure this is at the top
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if os.environ.get('PGDATABASE'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['PGDATABASE'],
            'USER': os.environ['PGUSER'],
            'PASSWORD': os.environ['PGPASSWORD'],
            'HOST': os.environ['PGHOST'],
            'PORT': os.environ['PGPORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jumashafara0@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # Your email password or app password
DEFAULT_FROM_EMAIL = 'jumashafara0@gmail.com'
CONTACT_EMAIL = 'jumashafara0@gmail.com'
EMAIL_TIMEOUT = 10  # 10 second timeout for email sending 

# Static files collection directory for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
}

# CORS settings
CORS_ALLOW_CREDENTIALS = True

# Additional CORS settings for better compatibility
CORS_ALLOW_ALL_ORIGINS = False  # Use specific origins for security
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Media files configuration
MEDIA_URL = '/media/'

# Full media URL for absolute URLs in API responses
if RAILWAY_ENVIRONMENT_NAME:
    # Production: Use the Railway backend URL
    FULL_MEDIA_URL = 'https://cepa-backend-production.up.railway.app/media/'
else:
    # Development: Use local backend URL
    FULL_MEDIA_URL = 'http://localhost:8000/media/'

# Railway volume configuration
if RAILWAY_ENVIRONMENT_NAME:
    print(RAILWAY_ENVIRONMENT_NAME)
    # Railway volume is mounted at /data/media
    MEDIA_ROOT = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
    print(MEDIA_ROOT)
else:
    # Local development media directory
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure media directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Add media URL to CORS allowed origins for image access
CORS_ALLOWED_ORIGINS = [
    "https://master.d1o07tzlhd1qin.amplifyapp.com",
    "https://master.dpdvoaezt60xm.amplifyapp.com",
    "https://cepa.or.ug",
    "https://www.cepa.or.ug",
    "http://localhost:3000",  # For local frontend development
]

# CKEditor Configuration
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Standard',
        'height': 400,
        'width': '100%',
        'toolbar_Standard': [
            ['Styles', 'Format'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
        ],
        'stylesSet': [
            {'name': 'Heading 1', 'element': 'h1'},
            {'name': 'Heading 2', 'element': 'h2'},
            {'name': 'Heading 3', 'element': 'h3'},
            {'name': 'Heading 4', 'element': 'h4'},
            {'name': 'Paragraph', 'element': 'p'},
        ],
        'format_tags': 'p;h1;h2;h3;h4;pre',
        'removePlugins': 'elementspath',
        'resize_enabled': True,
    },
}


