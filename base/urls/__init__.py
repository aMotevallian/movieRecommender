# base/urls/__init__.py
from django.urls import path, include

urlpatterns = [
    path('auth/', include('base.urls.auth_urls')),  # Include auth-related URLs
    path('movies/', include('base.urls.movie_urls')),  # Include movie-related URLs
]
