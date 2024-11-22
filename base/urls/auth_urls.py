from django.urls import path
from base.views.auth_views import RegisterAPI, LoginAPI  ,LogoutAPI
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('validateToken/', TokenValidateAPI.as_view(), name='validateToken'),
    path('logout/', LogoutAPI.as_view(), name='logout'),

]
