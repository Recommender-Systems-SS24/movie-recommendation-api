import loader
import content_based.recommendations as cbr
import collaborative_filtering.recommendations as cfr
from content_based.similarity_measures.custom import genre_custom_similarity
from content_based.similarity_measures.set_based import set_based_similarity, jaccard_index, SetExtractor, \
    intersection_cardinality
from content_based.similarity_measures.text_based import description_cosine_similarity, title_levenshtein_similarity
import gpt_recommandation.recommandations as gpt


def get_recommendations(movie_id, list_number):
    if list_number:
        if list_number == 1:
            return get_recommendation_list_1(movie_id)
        elif list_number == 2:
            return get_recommendation_list_2(movie_id)
        elif list_number == 3:
            return get_recommendation_list_3(movie_id)
        elif list_number == 4:
            return get_recommendation_list_4(movie_id)
        elif list_number == 5:
            return get_recommendation_list_5(movie_id)


def get_recommendation_list_1(movie_id):
    rec = gpt.get_similar_movies(movie_id)
    if len(rec) < 5:
        # it is not always possible to retrieve 5 movie recommendations from the API
        print("director set and writer set intersection cardinality was used for movie with id {}".format(movie_id))
        rec = cbr.get_similar_movies(movie_id, [
            {'weight': 0.5, 'measure': set_based_similarity(intersection_cardinality, SetExtractor.DIRECTOR)},
            {'weight': 0.5, 'measure': set_based_similarity(intersection_cardinality, SetExtractor.WRITER)}])
        rec_enriched = [enrich_with_data(rec[0]) for rec in rec]
        return {'Name': 'Intersection Cardinality Directors and Writers', 'List': rec_enriched}
    rec_enriched = [enrich_with_data(rec[0]) for rec in rec]
    return {'Name': 'GPT Recommendations', 'List': rec_enriched}


def get_recommendation_list_2(movie_id):
    rec = cbr.get_similar_movies(movie_id, [{'weight': 1, 'measure': genre_custom_similarity}])
    rec_enriched = [enrich_with_data(rec[0]) for rec in rec]
    return {'Name': 'Genres - Custom Similarity', 'List': rec_enriched}


def get_recommendation_list_3(movie_id):
    rec = cbr.get_similar_movies(movie_id, [{'weight': 1,
                                             'measure': set_based_similarity(jaccard_index, SetExtractor.KEYWORD)}])
    rec_enriched = [enrich_with_data(rec[0]) for rec in rec]
    return {'Name': 'Keywords - Jaccard Index', 'List': rec_enriched}


def get_recommendation_list_4(movie_id):
    rec = cbr.get_similar_movies(movie_id, [{'weight': 1, 'measure': title_levenshtein_similarity}])
    rec_enriched = [enrich_with_data(rec[0]) for rec in rec]
    return {'Name': 'Title - Levenshtein Distance', 'List': rec_enriched}


def get_recommendation_list_5(movie_id):
    rec = cbr.get_similar_movies(movie_id, [{'weight': 1, 'measure': description_cosine_similarity}])
    rec_enriched = [enrich_with_data(rec[0]) for rec in rec]
    return {'Name': 'Description - TF-IDF, Cosine Similarity', 'List': rec_enriched}


# def get_recommendation_list_5(movie_id):
#     rec = cfr.get_movie_recommendations(movie_id)
#     if len(rec) < 5:
#         # it is not always possible to use collaborative filtering, because a smaller ratings.csv is not
#         # from a smaller dataset
#         print("director set and writer set intersection cardinality was used for movie with id {}".format(movie_id))
#         rec = cbr.get_similar_movies(movie_id, [
#             {'weight': 0.5, 'measure': set_based_similarity(intersection_cardinality, SetExtractor.DIRECTOR)},
#             {'weight': 0.5, 'measure': set_based_similarity(intersection_cardinality, SetExtractor.WRITER)}])
#         rec_enriched = [enrich_with_data(rec[0]) for rec in rec]
#         return {'Name': 'Intersection Cardinality Directors and Writers', 'List': rec_enriched}
#     rec_enriched = [enrich_with_data(rec[0]) for rec in rec]
#     return {'Name': 'Collaborative filteríng', 'List': rec_enriched}


def enrich_with_data(movie_id):
    movie_metadata = loader.get_movies_metadata()
    title = movie_metadata.loc[movie_metadata['movieId'] == movie_id, 'title'].values
    genres = movie_metadata.loc[movie_metadata['movieId'] == movie_id, 'movielens_genres'].values
    rating = movie_metadata.loc[movie_metadata['movieId'] == movie_id, 'rating'].values
    return {
        'MovieID': movie_id,
        'Title': title[0] if len(title) > 0 else '',
        'Genres': list(genres[0]) if len(genres) > 0 else '',
        'Rating': rating[0] if len(rating) > 0 else 0,
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
