"""
Django settings for DjangoDev03 project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import datetime
import djcelery

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sys.path为模块导入的搜索路径所在的列表
sys.path.append(os.path.join(BASE_DIR, "apps"))
# sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bv89uqnh8m9il#0zkgs%57z14jtvb_c9cii$+19_dh!#%ivhmp'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

# ALLOWED_HOSTS = ["外网ip", "localhost", "127.0.0.1"]
# 设置可以用于访问项目的地址(ip、域名)
# 默认只能使用本地地址访问项目
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'corsheaders',
    'djcelery',
    # 应用名.apps.应用名首字母大写Config
    # 'apps.projects.apps.ProjectsConfig',
    'projects.apps.ProjectsConfig',
    # 'interfaces',
    'interfaces.apps.InterfacesConfig',
    'users.apps.UsersConfig',
    'testcases.apps.TestcasesConfig',
    'configures.apps.ConfiguresConfig',
    'testsuits.apps.TestsuitsConfig',
    'envs.apps.EnvsConfig',
    'debugtalks.apps.DebugtalksConfig',
    'reports.apps.ReportsConfig',
    'summary.apps.SummaryConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 需要添加在CommonMiddleware中间件之前
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS_ORIGIN_ALLOW_ALL为True, 指定所有域名(ip)都可以访问后端接口, 默认为False
CORS_ORIGIN_ALLOW_ALL = True
X_FRAME_OPTIONS = 'ALLOWALL'
# CORS_ORIGIN_WHITELIST指定能够访问后端接口的ip或域名列表
# CORS_ORIGIN_WHITELIST = [
#     "http://127.0.0.1:8080",
#     "http://localhost:8080",
#     "http://192.168.1.63:8080",
#     "http://127.0.0.1:9000",
#     "http://localhost:9000",
# ]

# 允许跨域时携带Cookie, 默认为False
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'DjangoDev03.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'DjangoDev03.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',  # Django 默认的数据库为sqlite3
        # 指定数据库引擎
        'ENGINE': 'django.db.backends.mysql',
        # 指定数据库名
        'NAME': 'test_3',
        # 数据数据用户名
        'USER': 'root',
        'PASSWORD': '123456',  # 数据库密码
        'HOST': 'localhost',  # 数据库主机域名或者ip
        'PORT': 3306  # 数据库的端口
    },
    'db': {
        # 'ENGINE': 'django.db.backends.sqlite3',  # Django 默认的数据库为sqlite3
        # 指定数据库引擎
        'ENGINE': 'django.db.backends.mysql',
        # 指定数据库名
        'NAME': 'test_3',
        # 数据数据用户名
        'USER': 'root',
        'PASSWORD': '123456',  # 数据库密码
        'HOST': 'localhost',  # 数据库主机域名或者ip
        'PORT': 3306  # 数据库的端口
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # 默认响应渲染类
    'DEFAULT_RENDERER_CLASSES': (
        # json渲染器为第一优先级
        'rest_framework.renderers.JSONRenderer',
        # 可浏览的API渲染器为第二优先级
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # django_filters.rest_framework.backends.DjangoFilterBackend
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ],
    # DEFAULT_PAGINATION_CLASS全局指定分页引擎类
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.ManualPageNumberPagination',
    # 一定要指定, 每一页获取的条数
    'PAGE_SIZE': 10,

    # 指定用于支持coreapi的Schema
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    # 1. 指定认证类(指定的是认证的方式)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 指定使用JWT Token认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # DRF框架默认情况下, 使用的是用户会话认证
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],

    # 2. 授权类(指定的是认证成功之后, 能干嘛!)
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     # DRF框架默认的权限为AllowAny(允许所有用户来访问)
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
}

JWT_AUTH = {
    # 默认token的过期时间为5分钟, 可以指定过期时间为1天
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 修改token值的前缀
    # 前端在传递token值时, Authorization作为key, 值为:token前缀 token
    # 'JWT_AUTH_HEADER_PREFIX': 'Bearer',

    # 指定返回前端数据的处理函数
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'utils.jwt_handler.jwt_response_payload_handler',
}



# 日志配置
BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(BASE_LOG_DIR):
    os.mkdir(BASE_LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - [%(levelname)s] - %(name)s - [msg]%(message)s - [%(filename)s:%(lineno)d ]'
        },
        'simple': {
            'format': '%(asctime)s - [%(levelname)s] - [msg]%(message)s'
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
            'filename': os.path.join(BASE_DIR, "logs/test.log"),  # 日志文件的位置
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        'test': {  # 定义了一个名为test的日志器
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'DEBUG',  # 日志器接收的最低日志级别
        },
    }
}

# 在全局配置文件中, 添加全局变量信息
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# 在全局配置文件中, 指定用例存放的目录
SUITES_DIR = os.path.join(BASE_DIR, 'suites')

# 1. 创建STATIC_ROOT, 存放静态文件的目录
STATIC_ROOT = os.path.join(BASE_DIR, "static")


EMAIL_SEND_USERNAME = '1069504984@qq.com'  # 定时任务报告发送邮箱，支持163,qq,sina,企业qq邮箱等，注意需要开通smtp服务
EMAIL_SEND_PASSWORD = 'hgjwdyonvegybgai'     # 邮箱密码
djcelery.setup_loader()

CELERY_ENABLE_UTC = True
# CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_TIMEZONE = TIME_ZONE
# CELERY_ENABLE_UTC = False
# # CELERY_TIMEZONE = 'Asia/Shanghai'

BROKER_URL = 'amqp://guest@localhost//'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_RESULT_BACKEND = 'django-db'# 任务元数据保存到数据库中

CELERY_ACCEPT_CONTENT = ['application/json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

# CELERY_TASK_RESULT_EXPIRES = 86400  # celery任务执行结果的超时时间， 此配置注释后，任务结果不会定时清理

CELERYD_CONCURRENCY = 1  # celery worker的并发数

CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker执行了多少任务就会销毁