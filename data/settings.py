"""
Django settings for data project.

Generated by 'django-admin startproject' using Django 4.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from environs import Env

env = Env()
env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "account.apps.AccountConfig",
    "cart.apps.CartConfig",
    "shop.apps.ShopConfig",
    "orders.apps.OrdersConfig",
    "phonenumber_field",
    "payment.apps.PaymentConfig",
    "coupons.apps.CouponsConfig",
    "mathfilters",
    "crispy_forms",
    "whitenoise.runserver_nostatic",
    "crispy_bootstrap5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "data.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
                "shop.context_processors.search_form",
            ],
        },
    },
]

WSGI_APPLICATION = "data.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {"default": env.dj_db_url("DATABASE_URL")}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # new
STATIC_ROOT = BASE_DIR / "staticfiles"  # new
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# security.W016
CSRF_COOKIE_SECURE = True

# security.W012
SESSION_COOKIE_SECURE = True

# security.W008
SECURE_SSL_REDIRECT = False

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# redirect the user after login
LOGIN_REDIRECT_URL = "shop:product_list"
LOGOUT_REDIRECT_URL = "login"

# redirect the user url
LOGIN_URL = "login"
# url to redirect the user to logout
LOGOUT_URL = "logout"
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
CART_SESSION_ID = "cart"
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# MEDIA_URL = "media/"
# MEDIA_ROOT = BASE_DIR / "media"
CART_SESSION_ID = "cart"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "djangooservice@gmail.com"
EMAIL_HOST_PASSWORD = "ehwx wtil tmot mzgj"
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"  # new
CRISPY_TEMPLATE_PACK = "bootstrap5"  # new


# Stripe settings
STRIPE_PUBLISHABLE_KEY = "pk_test_51OP7chEYjOhYVEjd9yD40w6ppRQnZH8YjPqa1ANitGZEbN2PT4CWsCpDdORoumsv6Fg8sIj5HkBYMPtUPdulb2eE00rzWttGPl"  # Publishable key
STRIPE_SECRET_KEY = "sk_test_51OP7chEYjOhYVEjdhFFCOFNxQoqQ541CILkR8UuoeAXxxb7X8Y2YI3DcyEgkFYmo4E3nmcyJUbCS0QTYwRBnvaNI00kTcarRvl"  # Secret key
STRIPE_API_VERSION = "2022-08-01"
