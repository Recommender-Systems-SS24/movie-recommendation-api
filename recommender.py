import loader
import content_based.recommendations as cbr
import collaborative_filtering.recommendations as cfr
from content_based.similarity_measures.custom import genre_custom_similarity
from content_based.similarity_measures.set_based import set_based_similarity, jaccard_index, SetExtractor, \
    intersection_cardinality
from content_based.similarity_measures.text_based import title_cosine_similarity, description_cosine_similarity


def get_recommendations(movie_id):
    # TODO: choose final recommendations algorithms to be used in the presentation
    rec_1 = cbr.get_similar_movies(movie_id, [{'weight': 1,
                                               'measure': set_based_similarity(jaccard_index, SetExtractor.KEYWORD)}])
    rec_1_enriched = [enrich_with_data(rec[0]) for rec in rec_1]

    rec_2 = cfr.get_movie_recommendations(movie_id)
    if len(rec_2) < 1:
        # it is not possible to perform item-based collaborative filtering for all methods, as cf is done with a
        # smaller dataset
        print("director set intersection cardinality was used for movie with id {}".format(movie_id))
        rec_2 = cbr.get_similar_movies(movie_id, [
            {'weight': 1, 'measure': set_based_similarity(intersection_cardinality, SetExtractor.DIRECTOR)}])
    rec_2_enriched = [enrich_with_data(rec[0]) for rec in rec_2]

    rec_3 = cbr.get_similar_movies(movie_id, [{'weight': 1, 'measure': genre_custom_similarity}])
    rec_3_enriched = [enrich_with_data(rec[0]) for rec in rec_3]

    rec_4 = cbr.get_similar_movies(movie_id, [{'weight': 1, 'measure': title_cosine_similarity}])
    rec_4_enriched = [enrich_with_data(rec[0]) for rec in rec_4]

    rec_5 = cbr.get_similar_movies(movie_id, [{'weight': 1, 'measure': description_cosine_similarity}])
    rec_5_enriched = [enrich_with_data(rec[0]) for rec in rec_5]

    return [rec_1_enriched, rec_2_enriched, rec_3_enriched, rec_4_enriched, rec_5_enriched]


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
