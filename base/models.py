from django.db import models

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    status = models.CharField(max_length=50)
    release_date = models.DateField()
    revenue = models.BigIntegerField()
    runtime = models.IntegerField()
    adult = models.BooleanField(default=False)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    budget = models.BigIntegerField()
    homepage = models.URLField(blank=True, null=True)
    imdb_id = models.CharField(max_length=15, blank=True, null=True)
    original_language = models.CharField(max_length=5)
    original_title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    genres = models.CharField(max_length=255)  # you can normalize this with a separate Genre model
    production_companies = models.TextField(blank=True, null=True)
    production_countries = models.TextField(blank=True, null=True)
    spoken_languages = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
from django.core.validators import MinValueValidator, MaxValueValidator

class MovieTFIDF(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    tfidf_vector = models.TextField()

    def __str__(self):
        return f"TF-IDF vector for {self.movie.title}"

class MovieSimilarity(models.Model):
    movie_from = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='similarities_from')
    movie_to = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='similarities_to')
    similarity_score = models.FloatField()
