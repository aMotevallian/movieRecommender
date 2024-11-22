from rest_framework import generics
from ..models import Movie
from ..serializers import MovieSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Q
import pickle
import pandas as pd
class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieList(generics.ListAPIView):
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination  
    page_size = 10
    def get_queryset(self):
        queryset = Movie.objects.all()
        genre = self.request.query_params.get('genre')
        release_year = self.request.query_params.get('release_date')
        search = self.request.query_params.get('search')  

        if genre:
            queryset = queryset.filter(genres__icontains=genre) 
        if release_year:
            queryset = queryset.filter(release_date__year=release_year)
        if search:
            queryset = queryset.filter(
                Q(title__contains=search) | Q(overview__contains=search)
            )
        return queryset

class ContentBasedRecommendationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        movie_id = kwargs.get('id')
        print(f"Fetching recommendations for movie ID: {movie_id}")

        movies = Movie.objects.all()
        movies_df = pd.DataFrame(list(movies.values('id', 'title', 'overview', 'genres', 'keywords')))

        try:
            target_movie = movies_df[movies_df['id'] == movie_id].iloc[0]
            print(f"Found movie: {target_movie['title']}")
        except IndexError:
            print(f"Movie with ID {movie_id} not found.")
            return Response({"error": "Movie not found"}, status=404)

        # Combine the content features
        movies_df['content'] = movies_df['overview'] + ' ' + movies_df['genres'] + ' ' + movies_df['keywords']

        # TF-IDF vectorization and cosine similarity
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['content'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Get similarity scores
        target_idx = movies_df[movies_df['id'] == movie_id].index[0]
        similarity_scores = list(enumerate(cosine_sim[target_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Get the top 10 similar movies
        similar_movie_indices = [i[0] for i in similarity_scores[1:11]]
        similar_movies = movies_df.iloc[similar_movie_indices]
        similar_movie_ids = similar_movies['id'].tolist()

        # Query the recommended movies
        recommended_movies = Movie.objects.filter(id__in=similar_movie_ids)
        serializer = MovieSerializer(recommended_movies, many=True)

        return Response(serializer.data)
    

