from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer
from .models import Movie
from .serializers import MovieSerializer
from django.db.models import Q

# Register API
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer

# Login API
class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=400)

# Get a movie by ID
class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Get movies by genre, release date
class MovieList(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()
        genre = self.request.query_params.get('genre')
        release_date = self.request.query_params.get('release_date')
        if genre:
            queryset = queryset.filter(genres__icontains=genre)
        if release_date:
            queryset = queryset.filter(release_date=release_date)
        return queryset
