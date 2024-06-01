
def genre_custom_similarity(other_movie, reference_movie):
    other_movie_genres_primary, other_movie_genres_secondary = get_primary_and_secondary_genre_sets(other_movie)
    reference_movie_genres_primary, reference_movie_genres_secondary =(
        get_primary_and_secondary_genre_sets(reference_movie))

    score = 0

    for genre in other_movie_genres_primary:
        if genre in reference_movie_genres_primary:
            # the genre is a primary genre for both movies
            score += 3
        elif genre in reference_movie_genres_secondary:
            # the genre is a primary genre for one movie and a secondary genre for the other movie
            score += 1

    for genre in other_movie_genres_secondary:
        if genre in reference_movie_genres_primary:
            # the genre is a primary genre for one movie and a secondary genre for the other movie
            score += 1
        elif genre in reference_movie_genres_secondary:
            # the genre is a secondary genre for both movies
            score += 2

    return score


def get_primary_and_secondary_genre_sets(movie):
    movie_movielens_genres = set(movie['movielens_genres'])
    movie_tmdb_genres = set(movie['tmdb_genres'])
    movie_imdb_genres = set(movie['imdb_genres'])

    genres_intersection = movie_movielens_genres.intersection(movie_tmdb_genres, movie_imdb_genres)
    genres_union = movie_movielens_genres.union(movie_tmdb_genres, movie_imdb_genres)
    genres_diff = genres_union.difference(genres_intersection)

    return genres_intersection, genres_diff



