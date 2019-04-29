"""
Django settings for Gx project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4+(ys*#u21-#_h54i!po#wm5g5=k-87-jp)_p-8c)iir8=j^s1'

# SECURITY WARNING: don't run with debug turned on in production!
# debug改为False后就不会提供静态文件服务了，那么就需要通过nginx
DEBUG = False

ALLOWED_HOSTS = ['47.99.114.195',"www.gongxietech.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.users',
    'apps.word',
    'apps.cms',
    'apps.news',
    'apps.culture',
    'apps.product',
    'apps.ueditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Gx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins':['django.templatetags.static'],
        },
    },
]
AUTH_USER_MODEL='users.Users'
WSGI_APPLICATION = 'Gx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'company_data',
        'USER':'gongxie',
        'PASSWORD':'cym19911206',
        'HOST':'47.99.114.195',
        'PORT':'3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)
# 配置media路径，在django中一般会将文件存放在media中，media可以在任何文件夹中，不一定在项目文件中。
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')

# 在settings.py文件中指定redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "item_ImgCaptcha": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    "item_session": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/2",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
}

# 在setting.py文件中加入如下配置：
# 配置日志器，记录网站的日志信息
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已存在的日志器
    'disable_existing_loggers': False,
    # 指定日志的格式
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(client_message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(client_message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/dj_blog.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'inter_log': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
# 将用户的session保存到redis中
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 指定缓存redis的别名
SESSION_CACHE_ALIAS = "item_session"

# docker设置
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': '127.0.0.1:8002'
    },
}


# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:8002/',  # 此处为elasticsearch运行的服务器ip地址，端口号默认为9200
        'INDEX_NAME': 'gx',  # 指定elasticsearch建立的索引库的名称
    },
}
# 当数据库改变时，会自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# FASTDFS域名信息
FASTDFS_SERVER_DOMAIN = "http://47.99.114.195:8888/"



# 七牛云相关配置
QINIU_ACCESS_KEY="5ixiJHJFv_euNuH47dr2SCN4wWcGOyJA7RDVKEHt"
QINIU_SECRET_KEY="FMfUTWJwPkyGkJkQMb2fA_Dy1E2OASYETUs6TThC"
QINIU_BUCKET_NAME='mblog'
QINIU_DOMAIN='http://www.gongxietech.com/'


# 1、 配置服务器的ueditor
UEDITOR_UPLOAD_TO_SERVER = True
UEDITOR_UPLOAD_PATH =MEDIA_ROOT
UEDITOR_CONFIG_PATH = os.path.join(BASE_DIR,'static','ueditor','config.json')

# 2、上传到qiniu的ueditor配置
UEDITOR_QINIU_ACCESS_KEY=QINIU_ACCESS_KEY
UEDITOR_QINIU_SECRET_KEY=QINIU_SECRET_KEY
UEDITOR_QINIU_BUCKET_NAME=QINIU_BUCKET_NAME
UEDITOR_QINIU_DOMAIN=QINIU_DOMAIN
UEDITOR_UPLOAD_TO_QINIU=True