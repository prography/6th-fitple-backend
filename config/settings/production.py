from .base import *
import os

# For the deployment checklist automatically, you should use a command 'python manage.py check --deploy'

DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# email setiing
with open('env/etc/email.txt') as email:
    EMAIL_HOST_USER = email.readline().strip()
    EMAIL_HOST_PASSWORD = email.readline().strip()

with open('env/etc/db.txt') as db_info:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': db_info.readline().strip(),
            'USER': db_info.readline().strip(),
            'PASSWORD': db_info.readline().strip(),
            'HOST': db_info.readline().strip(),
            'PORT': db_info.readline().strip(),
            'ATOMIC_REQUESTS': True,
        }
    }
    # redirect URL
    REDIRECT_URL = 'https://myUrl.com'
# email setting
#     EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
#     EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

# HTTPS for the security
# make ensure the browser to use HTTPS instead of HTTP for the cookie
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# for preventing XSS (Cross-site Scripting)
SECURE_BROWSER_XSS_FILTER = True  # X-XSS-Protection:1, mode=block
SECURE_CONTENT_TYPE_NOSNIFF = True  # CSP(Content Security Policy)
X_FRAME_OPTIONS = 'DENY'  # If there is a good reason for your site to serve other parts of itself in a frame, you should change it to 'SAMEORIGIN' (DEFAULT) (or maybe 'ALLOW FROM example.com')

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 3  # to first use a small value for testing (one hour). Once you confirm that all assets are served securely on your site, increase this value so that infrequent visitors will be protected (1 year)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # for subdomains
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = False  # the SecurityMiddleware redirects all non-HTTPS request to HTTPS

# Error reporting
ADMINS = [
    ('paikend', 'paikend@gmail.com'),
]
MANAGERS = ADMINS
# an email address of an account to send error reporting emails
SERVER_EMAIL = 'paikend@gmail.com'

# External File Storages (django-storages + aws S3(boto3))
INSTALLED_APPS += ['storages', ]

# Administrator1
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
#
# AWS_STORAGE_BUCKET_NAME = 's3-name'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
#

# DEFAULT_FILE_STORAGE = 'config.storage_backends.PrivateMediaStorage'
#
# AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
# PRIVATE_FILE_STORAGE = 'config.storage_backends.PrivateMediaStorage'
#
# AWS_S3_REGION_NAME = 'ap-northeast-2'
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_DEFAULT_ACL = None

with open(os.path.join(BASE_DIR, 'env/etc/s3.txt')) as f:
    AWS_ACCESS_KEY_ID = f.readline().strip()
    AWS_SECRET_ACCESS_KEY = f.readline().strip()
    AWS_REGION = f.readline().strip()
    AWS_STORAGE_BUCKET_NAME = f.readline().strip()

    AWS_S3_CUSTOM_DOMAIN = '%s.s3-%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
    AWS_PRIVATE_MEDIA_LOCATION = 'media/private'

    AWS_DEFAULT_ACL = 'public-read'
    # AWS_LOCATION = 'static' # 일단 media - image 부분만!
    AWS_MEDIA_LOCATION = 'media'

    # STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

    # STATICFILES_STORAGE = ''
    DEFAULT_FILE_STORAGE = 'config.storage_backends.PublicMediaStorage'

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://f1829f86313b4cf4beb1c87cbacc8582@o327642.ingest.sentry.io/5271277",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
