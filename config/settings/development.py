from .base import *


ALLOWED_HOSTS = ['*']

# redirect URL
REDIRECT_URL = 'http://localhost:3000'


# email setiing
# with open('env/etc/email.txt') as email:
#     EMAIL_HOST_USER = email.readline().strip()
#     EMAIL_HOST_PASSWORD = email.readline().strip()

# django-debug-toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

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

# 추후 로컬 작업 할때는 s3가 아닌 로컬 작업용으로 변경 필요
with open(os.path.join(BASE_DIR, 'env/etc/s3.txt')) as f:
    AWS_ACCESS_KEY_ID = f.readline().strip()
    AWS_SECRET_ACCESS_KEY = f.readline().strip()
    AWS_REGION = f.readline().strip()
    AWS_STORAGE_BUCKET_NAME = f.readline().strip()

    AWS_S3_CUSTOM_DOMAIN = '%s.s3-%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_DEFAULT_ACL = 'public-read'
    # AWS_LOCATION = 'static' # 일단 media - image 부분만!
    AWS_MEDIA_LOCATION = 'media'

    # STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

    # STATICFILES_STORAGE = ''
    DEFAULT_FILE_STORAGE = 'config.storage_backends.PublicMediaStorage'


# enable http oauth token transport in requests-oauthlib
# WARNING: only set for dev env
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# drf-yasg
INSTALLED_APPS += ['drf_yasg']
