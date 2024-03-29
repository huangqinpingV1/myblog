"""
Django settings for DjangoBlog project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qt@1a8ed_^g_@ha9s2zpineqra#+_3c0=-#x&a1-v4@#x1gpp0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['1.12.250.75','localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #站点地图相关
    'django.contrib.sitemaps',
    #增加blog应用
    'blog',
    #增加accounts应用，账号相关
    'accounts',
    #增加comments应用，评论相关
    'comments',
    #增加pagedown应用
    'pagedown',
    #增加oauth验证
    'oauth',
    #站内搜索
    'haystack',
    #site app
    'django.contrib.sites',
    #jss,css压缩相关
    'compressor',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #中间件
    'blog.middleware.OnlineMiddleware'
]

ROOT_URLCONF = 'DjangoBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #模板相关
                'blog.context_processors.seo_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoBlog.wsgi.application'

#搜索相关设置
HAYSTACK_CONNECTIONS ={
        'default': {
                #搜索引擎文件在blog应用下
                'ENGINE':'blog.whoosh_cn_backend.WhooshEngine',
                'PATH':os.path.join(BASE_DIR,'whoosh_index'),
            }
        }
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
#允许使用用户名或密码登录
AUTHENTICATION_BACKENDS =['accounts.user_login_backend.EmailOrUsernameModelBackend']
#
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        #mysql数据库配置
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydjangoblog',
        'USER': 'adminhqp',
        'PASSWORD': 'hello123+',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

#变更语言
#ANGUAGE_CODE = 'en-us'
ANGUAGE_CODE =  'zh-hans'
#变更地区
#IME_ZONE = 'UTC'
TME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES = BASE_DIR/'static'
STATIC_ROOT =os.path.join(BASE_DIR,'collectedstatic')
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.BlogUser'
LOGIN_URL = '/login/'
#TimeFormat
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d'
SITE_NAME = '测试一下'
#网站网址
SITE_URL = 'http://127.0.0.1:8080'
SITE_DESCRIPTION = '简单的Django应用.'
SITE_SEO_DESCRIPTION ="Django Demo"
SITE_SEO_KEYWORDS ="linux,appache,mysql,服务器,ubuntu,shell,web,csharp,.net,asp,mac,switf"
ARTICLE_SUB_LENGTH = 300

SHOW_GOOGLE_ADSENSE = True
#新增bootstrap颜色样式
BOOTSTRAP_COLOR_TYPES = [
        'default','primary','success','info','warning','danger'
        ]
#侧边栏文章数
SIDEBAR_ARTICLE_COUNT = 10
#侧边栏评论数目
SIDEBAR_COMMENT_COUNT =5
#分页
PAGINATE_BY = 10
#http缓存时间
CACHE_CONTROL_MAX_AGE  = 2592000
#缓存设置,缓存进程运行在localhost端口11211.
CACHES  = {
        #本地缓存设置
        'default':{
                'BACKEND':'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION':'unique-snowflake',
            }

}
CACHE_MIDDLE_WARE_SECONDS =60*60*10
CACHE_MIDDLEWARE_KEY_PREFIX ='djangoblog'
CACHE_MIDDLEWARE_ALIAS = 'default'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS  = 'default'

OAHUTH ={
    'sina':{
        'appkey':'3161614143',
        'appsecret':'ee17c099317f872eeddb25204ea46721',
        'callbackurl':'http://blog.lylinux.org/oauth/authorize?type=weibo',
        },
    "google":{
        'appkey':os.environ.get('GOOGLE_APP_KEY'),
        'appsecret':os.environ.get('GOOGLE_APP_SECRET'),
        'callbackurl':'http://www.lylinux.net/oauth/authorize?type=google'
        },
    'github':{
        'appkey':os.environ.get('GITHUB_APP_KEY'),
        'appsecret':os.environ.get('GITHUB_APP_SECRET'),
        'callbackurl':'http://www.lylinux.net/oauth/authorize?type=github'
        }
}


SITE_ID = 1
BAIDU_NOTIFY_URL="http://data.zz.baidu.com/urls?site=https://www.lylinux.net&token=1uAOGrMsUm5syDGn&type=original"
#email配置
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
#EMAIL_USE_SSL =True
EMAIL_HOST="smtp.example.qq.com"
EMAIL_PORT= 587
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = os.environ.get('DJANGO_EMAIL_USER')
ADMINS = [('huangqinping','xxxxxxx@qq.com')]
#logging相关
LOG_PATH = os.path.join(BASE_DIR,'logs')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH,exist_ok=True)

LOGGING = {
        'version':1,
        'disable_existing_loggers':False,
        'root':{
            'level':'INFO',
            'handlers':['console','log_file'],
            },
        'formatters':{
            'verbose':{
                'format':'[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d %(module)s]',
                }
            },
        'filters':{
            'require_debug_false':{
                '()':'django.utils.log.RequireDebugFalse'
                },
            'require_debug_true':{
                '()':'django.utils.log.RequireDebugTrue'
                },
            },
        'handlers':{
            'log_file':{
                    'level':'INFO',
                    'class':'logging.handlers.TimedRotatingFileHandler',
                    'filename':os.path.join(LOG_PATH,'djangoblog.log'),
                    'when':'D',
                    'formatter':'verbose',
                    'interval':1,
                    'delay':True,
                    'backupCount':5,
                    'encoding':'utf-8'
                },
            'console':{
                    'level':'DEBUG',
                    'filters':['require_debug_true'],
                    'class':'logging.StreamHandler',
                    'formatter':'verbose',
                },
            'null':{
                    'class':'logging.NullHandler',
                },
            'mail_admins':{
                    'level':'ERROR',
                    'filters':['require_debug_false'],
                    'class':'django.utils.log.AdminEmailHandler'
                    }
            },
        'loggers':{
            'djangoblog':{
                'handlers':['log_file','console'],
                'level':'INFO',
                'propagate':True,
                },
            'django.request':{
                'handlers':['mail_admins'],
                'level':'ERROR',
                'propagate':False,
                }
            },
}
#配置STATICFILES_FINDERS
STATICFILES_FINDERS = {
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
        }
#添加django-compressor配置
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS =[
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS =[
        'compressor.filters.jsmin.JSMinFilter'
]
