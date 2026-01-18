from pathlib import Path
import os

# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================
SECRET_KEY = 'django-insecure-0mbnzuj!9+b^4=kt#c^#)58v!0=%!c7!*l(#s68#nqi2avwqr7'

# ✅ Development mode
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    'axes',  # 🔐 Phase 6: Brute force protection

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'widget_tweaks',

    # Project apps
    'accounts',
    'courts',
    'bookings',
    'logs',
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 🔐 Axes middleware (MUST be last)
    'axes.middleware.AxesMiddleware',
]

# =========================
# URL CONFIG
# =========================
ROOT_URLCONF = 'config.urls'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # REQUIRED by Axes
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =========================
# WSGI
# =========================
WSGI_APPLICATION = 'config.wsgi.application'

# =========================
# DATABASE
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# =========================
# DEFAULT PRIMARY KEY
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# AUTH REDIRECTS
# =========================
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# =========================
# AUTHENTICATION BACKENDS
# =========================
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',              # Axes first
    'django.contrib.auth.backends.ModelBackend',
]

# =========================
# AXES — USER-BASED ACCOUNT LOCKOUT (FIXED)
# =========================
AXES_FAILURE_LIMIT = 5              # Lock after 5 failed attempts
AXES_COOLOFF_TIME = 0.25            # 15 minutes
AXES_RESET_ON_SUCCESS = True

AXES_ONLY_USER_FAILURES = True      # ✅ LOCK PER USERNAME ONLY
AXES_LOCK_OUT_BY_IP = False
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = False
AXES_LOCK_OUT_BY_USER_OR_IP = False

AXES_ENABLE_ADMIN = True
AXES_VERBOSE = True

AXES_LOCKOUT_TEMPLATE = 'account_locked.html'

# =========================
# LOGGING — SECURITY AUDIT
# =========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'security.log'),
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# =========================
# SECURITY HEADERS
# =========================
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

# =========================
# COOKIES (DEV MODE)
# =========================
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
