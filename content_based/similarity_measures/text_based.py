from loader import get_description_cosine_sim_matrix, get_movies_metadata, get_title_cosine_sim_matrix
import jellyfish
import Levenshtein


def description_cosine_similarity(other_movie, reference_movie):
    description_cosine_sim_matrix = get_description_cosine_sim_matrix()
    movie_metadata_df = get_movies_metadata()
    other_movie_idx = movie_metadata_df.index[movie_metadata_df['movieId'] == other_movie['movieId']][0]
    reference_movie_idx = movie_metadata_df.index[movie_metadata_df['movieId'] == reference_movie['movieId']][0]
    return description_cosine_sim_matrix[other_movie_idx][reference_movie_idx]


def title_cosine_similarity(other_movie, reference_movie):
    title_cosine_sim_matrix = get_title_cosine_sim_matrix()
    movie_metadata_df = get_movies_metadata()
    other_movie_idx = movie_metadata_df.index[movie_metadata_df['movieId'] == other_movie['movieId']][0]
    reference_movie_idx = movie_metadata_df.index[movie_metadata_df['movieId'] == reference_movie['movieId']][0]
    return title_cosine_sim_matrix[other_movie_idx][reference_movie_idx]


def title_levenshtein_similarity(other_movie, reference_movie):
    other_movie_title = other_movie['title']
    reference_movie_title = reference_movie['title']
    distance = Levenshtein.distance(other_movie_title, reference_movie_title)
    # the maximal levenshtein distance of two strings is the length of the longer string
    max_len = max(len(other_movie_title), len(reference_movie_title))

    if max_len > 0:
        return 1 - (distance / max_len)

    return 0


def title_jaro_winkler(other_movie, reference_movie):
    other_movie_title = other_movie['title']
    reference_movie_title = reference_movie['title']
    return jellyfish.jaro_winkler_similarity(other_movie_title, reference_movie_title)
