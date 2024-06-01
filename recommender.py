import loader
import content_based.recommendations as cbr
from content_based.similarity_measures.text_based import title_cosine_similarity


def get_recommendations(movie_id):
    # TODO: use different recommendation algorithms
    rec_1 = cbr.get_similar_movies(movie_id, [{'weight': 1, 'measure': title_cosine_similarity}])
    rec_1_enriched = [enrich_with_data(rec[0]) for rec in rec_1]
    return [rec_1_enriched, rec_1_enriched, rec_1_enriched, rec_1_enriched, rec_1_enriched]


def enrich_with_data(movie_id):
    # TODO: add more data for display
    movie_metadata = loader.get_movies_metadata()
    title = movie_metadata.loc[movie_metadata['movieId'] == movie_id, 'title'].values
    return {
        'MovieID': movie_id,
        'Title': title[0] if len(title) > 0 else ''
    }


def get_random_recommendations():
    # get some random movies for testing
    recommendations = []
    for _ in range(5):
        movie_metadata = loader.get_movies_metadata()
        random_sample = movie_metadata.sample(n=5)
        random_movie_ids = random_sample['movieId'].tolist()
        recs = [enrich_with_data(movie_id) for movie_id in random_movie_ids]
        recommendations.append(recs)
    return recommendations

