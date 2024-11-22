from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from ...models import Movie, MovieSimilarity

class Command(BaseCommand):
    help = 'Precompute cosine similarity for all movies and store in the database'

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        movies_df = pd.DataFrame(list(movies.values('id', 'overview', 'genres', 'keywords')))
        movies_df['content'] = movies_df['overview'] + ' ' + movies_df['genres'] + ' ' + movies_df['keywords']

        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['content'])
        cosine_sim = cosine_similarity(tfidf_matrix)

        # Clear previous similarity data
        MovieSimilarity.objects.all().delete()

        for idx, movie_id in enumerate(movies_df['id']):
            for sim_idx, score in enumerate(cosine_sim[idx]):
                if idx != sim_idx:
                    MovieSimilarity.objects.create(
                        movie_from_id=movie_id,
                        movie_to_id=movies_df.iloc[sim_idx]['id'],
                        similarity_score=score
                    )

        self.stdout.write(self.style.SUCCESS('Successfully precomputed and saved cosine similarities.'))
