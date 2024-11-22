from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('base.urls.auth_urls')),  # Authentication-related URLs
    path('api/movies/', include('base.urls.movies_urls')),  # Movie-related URLs
]
