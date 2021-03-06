"""
Django settings for invoicemis project.

Generated by 'django-admin startproject' using Django 3.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2g_6t$i7=!d+ydfps*%@v&e#g+l&w&y_+3uy)2@i0@s#br7q2p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'constance',
    'mainapp',


    'djmoney',
    'crispy_forms',
    'rest_framework',
    'jsonify',
    'bootstrap_modal_forms',
    'widget_tweaks',
    'sweetify',
    'django_countries',
    'django_filters',
    'dynamic_fields',
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

ROOT_URLCONF = 'invoicemis.urls'

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

WSGI_APPLICATION = 'invoicemis.wsgi.application'



AUTH_USER_MODEL = 'mainapp.CustomUser' # changes the built user model to ours


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'quotation_mis',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Maseru'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mainapp/static/images')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = 'login'
LOGOUT_URL ='logout'
LOGIN_REDIRECT_URL ='system_dashboard'

CURRENCIES = ('MWK',)

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

CONSTANCE_ADDITIONAL_FIELDS = {
'image_field': ['django.forms.ImageField', {}],
'float_field': ['django.forms.FloatField', {}],
}

CONSTANCE_CONFIG = {
'SHOP_NAME':('DALY CREATIONS','You are Home!!' ),
'TAG_LINE':('The best in Town!!', 'The best Shop in Town'),
'ADDRESS':('P.O. Box 418','Address' ),
'LOCATION':('Lilongwe','Lilongwe' ),
'COUNTRY':('Malawi','Malawi' ),
'TEL':('+ 265 000 000',' Tel'),
'FAX':('+ 265 000 000',' Fax'),
'CEL':('+ 265 000 000',' Cel'),
'EMAIL':('mcatechmw@mcatech.mw','MCATECH'),
'TAX_NAME':(16.5,'VAT','float_field'),
'LABOUR_COST':(15.0,'Labour','float_field'),
'MARKUP_A':(38.0,'Markup A','float_field'),
'MARKUP_B':(35.0,'Markup B','float_field'),
'MARKUP_C':(30.0,'Markup C','float_field'),
'LOGO_IMAGE': ('images.png', 'Company logo', 'image_field'),
}

CONSTANCE_CONFIG_FIELDSETS = {
'Shop Options': ('SHOP_NAME','LOGO_IMAGE','TAG_LINE','ADDRESS','LOCATION','TEL','FAX','EMAIL','CEL','COUNTRY'),
'Invoice Options': ('TAX_NAME','LABOUR_COST','MARKUP_A','MARKUP_B','MARKUP_C'),
}