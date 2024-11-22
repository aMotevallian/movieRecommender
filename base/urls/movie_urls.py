from django.urls import path
from base.views.movie_views import MovieList, MovieDetail, ContentBasedRecommendationAPIView 

urlpatterns = [
    path('', MovieList.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('<int:id>/recommendations/', ContentBasedRecommendationAPIView.as_view(), name='content-based-recommendations'),
]
