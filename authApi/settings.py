
from datetime import timedelta

from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-lb*z8ca18#1a14dqacollu-q&rhsj-54_=67m@*7pbnly9r3qw"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$sj&*m3(8xsk)=_3p3dg(@+l77k09f+pfkn9r34!+_y&t5u$9^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SITE_ID = 1
ROOT_URLCONF = "authApi.urls"
WSGI_APPLICATION = "authApi.wsgi.application"
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

ALLOWED_HOSTS = ['*']

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework_simplejwt',
    'authApi',
    'services.user',
    
    # 'django.contrib.sites',

    'oauth2_provider',
    # 'social_django',
    # 'dj_rest_auth',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'rest_framework.authtoken', 
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',

    ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    #     'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    # ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  
    ],
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'allauth.account.middleware.AccountMiddleware',  # Add this line
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB2', 
        'USER': 'root', 
        'PASSWORD': '123456789', 
        'HOST': 'localhost',  
        'PORT': '3306',  
        # 'OPTIONS': {
        #     'auth_plugin': 'mysql_native_password',  # Use a compatible auth plugin
        # },
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'SIGNING_KEY': SECRET_KEY,
}

AUTH_USER_MODEL = 'user.User'

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': '991449275840-4h0hnlitc12de8l7g0gve0c852rms4ki.apps.googleusercontent.com',
#             'secret': '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',
#             'key': ''
#         },
#         'SCOPE': ['profile', 'email'], 
#         'AUTH_PARAMS': {
#             'access_type': 'offline',
#         },
#     }
# }

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
SOCIALACCOUNT_LOGIN_ON_GET = True

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 600,
    'REFRESH_TOKEN_EXPIRE_SECONDS': 3600,
    'SCOPES': {
        'read': 'Read access',
        'write': 'Write access',
    }
}
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
]
