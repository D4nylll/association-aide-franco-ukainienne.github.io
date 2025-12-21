pip install djangorestframework djangorestframework-simplejwt dj-rest-auth django-allauth


INSTALLED_APPS = [
    # ... стандартні додатки ...
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # Провайдер Google
    'django.contrib.sites',
]

SITE_ID = 1

# Налаштування JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'

# Налаштування Google (через адмінку або тут)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}



# views.py
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/google/callback/" # Ваша URL-адреса
    client_class = OAuth2Client



# urls.py
from django.urls import path, include
from .views import GoogleLogin

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
]


Крок 5: Google Cloud Console
Зайдіть у Google Cloud Console.

Створіть проект та OAuth 2.0 Client ID.

Додайте Authorized redirect URIs (наприклад, http://127.0.0.1:8000/accounts/google/login/callback/).

В адмінці Django у розділі Social Accounts -> Social Applications додайте новий запис для Google, вказавши Client ID та Secret Key.


{
    "access_token": "ТОКЕН_ЯКИЙ_ВИДАВ_GOOGLE"
}

{
    "access": "eyJhbGciOi...",
    "refresh": "eyJhbGciOi...",
    "user": { "pk": 1, "username": "..." }
}

