from pathlib import Path
from datetime import timedelta
import os
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {'1', 'true', 'yes', 'on'}


def env_list(name: str, default: str = '') -> list[str]:
    return [item.strip().rstrip('/') for item in os.getenv(name, default).split(',') if item.strip()]


SECRET_KEY = os.getenv('SECRET_KEY', 'dev-only-secret-key-change-me')
# Railway'da DEBUG avtomatik o'chiq (xatolar sahifasida maxfiy ma'lumot chiqmasin), localda yoqiq.
ON_RAILWAY = bool(os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('RAILWAY_ENVIRONMENT_NAME'))
DEBUG = env_bool('DEBUG', not ON_RAILWAY)
if ON_RAILWAY and SECRET_KEY == 'dev-only-secret-key-change-me':
    import warnings
    warnings.warn('SECRET_KEY Railway Variables ichida o\'rnatilmagan: uzun tasodifiy qiymat yozing.')

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', '127.0.0.1,localhost,.railway.app,.up.railway.app,0.0.0.0')
railway_public_domain = os.getenv('RAILWAY_PUBLIC_DOMAIN')
if railway_public_domain and railway_public_domain not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(railway_public_domain)
if DEBUG and '*' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('*')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'accounts',
    'olympiad',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASE
# Railway'da Postgres uchun DATABASE_URL ishlatiladi.
# Localda yoki DATABASE_URL noto'g'ri/bo'sh bo'lsa SQLite fallback ishlaydi.
database_url = os.getenv('DATABASE_URL', '').strip()
if database_url and not database_url.startswith('${{'):
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,
            # Uzilib qolgan ulanish qayta ishlatilib, so'rov xato bermasligi uchun.
            conn_health_checks=True,
            ssl_require=env_bool('DB_SSL_REQUIRE', False),
        )
    }
else:
    if ON_RAILWAY:
        import warnings
        warnings.warn("DATABASE_URL topilmadi: Railway'da SQLite ishlayapti, deploy qilinganda ma'lumotlar o'chadi. PostgreSQL ulang.")
    # SQLite faqat local sinov uchun. Ko'p o'quvchi bir vaqtda yozganda "database is locked"
    # bo'lmasligi uchun WAL rejimi, kutish vaqti va IMMEDIATE tranzaksiyalar yoqilgan.
    # Olimpiada kuni Railway'da albatta PostgreSQL (DATABASE_URL) ishlating.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 20,
                'transaction_mode': 'IMMEDIATE',
                'init_command': 'PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;',
            },
        }
    }

# Imtihon savollari har bir jarayon xotirasida qisqa muddat saqlanadi:
# yuzlab o'quvchi bir vaqtda kirganda baza bir xil savollarni qayta-qayta o'qimaydi.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'olympiad-cache',
        'TIMEOUT': 60,
        'OPTIONS': {'MAX_ENTRIES': 2000},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Frontend Netlify, backend Railway bo'lganida CORS shu yerdan boshqariladi.
CORS_ALLOW_ALL_ORIGINS = env_bool('CORS_ALLOW_ALL_ORIGINS', False)
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = env_list(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173'
)

# Preview yoki yangi Netlify domen olganda CORS xatolari chiqmasligi uchun.
# Kuchliroq xavfsizlik xohlasangiz Railway Variables ichida CORS_ALLOW_NETLIFY=False qilib,
# CORS_ALLOWED_ORIGINS ga faqat o'zingizning Netlify domeningizni yozing.
CORS_ALLOWED_ORIGIN_REGEXES = []
if env_bool('CORS_ALLOW_NETLIFY', True):
    CORS_ALLOWED_ORIGIN_REGEXES.append(r'^https://[a-zA-Z0-9-]+\.netlify\.app$')

CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS', ','.join(CORS_ALLOWED_ORIGINS))
if env_bool('CORS_ALLOW_NETLIFY', True) and 'https://*.netlify.app' not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append('https://*.netlify.app')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE', not DEBUG)
CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE', not DEBUG)
