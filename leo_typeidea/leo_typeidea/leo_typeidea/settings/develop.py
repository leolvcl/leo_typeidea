from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'leo_typeidea_db',
        'USER': 'root',
        'PASSWORD': 'lion',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        # 'CONN_MAX_AGE': 5 * 60,
        # 'OPTIONS': {'charset': 'utf8mb4'}
    }
}
INSTALLED_APPS += [
    'silk',
]
MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
]
INTERNAL_IPS = ['127.0.0.1']
# DEBUG_TOOLBAR_CONFIG = {
#     'JQUERT_URL': 'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js'
# }
# DEBUG_TOOLBAR_PANELS = {
#     'debug_toolbar_line_profiler.panel.ProfilingPanel'
# }
# from debug_toolbar_line_profiler.panel import ProfilingPanel