from loader import get_movies_metadata


def get_similar_movies(reference_movie_id, similarity_measures):
    similarity_scores = []

    movies_df = get_movies_metadata()

    reference_movie_df = movies_df.loc[movies_df['movieId'] == reference_movie_id]
    assert reference_movie_df.shape[0] == 1, "There are several movies with the same movie id"
    reference_movie = reference_movie_df.squeeze()

    for index, movie_row in movies_df.iterrows():
        if movie_row['movieId'] == reference_movie_id:
            continue

        weighted_score = 0
        for similarity_measure in similarity_measures:
            score = similarity_measure['measure'](reference_movie, movie_row)
            weight = similarity_measure['weight']
            weighted_score = weighted_score + weight * score

        similarity_scores.append((movie_row['movieId'], weighted_score))

    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    return similarity_scores[:5]
