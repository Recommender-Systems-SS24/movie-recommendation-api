from collaborative_filtering.similarity_measures.pearson import pearson_correlation
from loader import get_item_user_matrix


def get_movie_recommendations(reference_movie_id):
    similarity_scores = []

    # each row represents a movie, each column a user
    item_user_matrix_df = get_item_user_matrix()

    try:
        reference_movie = item_user_matrix_df.loc[reference_movie_id]
    except KeyError:
        return []

    for index, movie_row in item_user_matrix_df.iterrows():
        if index == reference_movie_id:
            continue
        similarity_score = pearson_correlation(reference_movie, movie_row)
        similarity_scores.append((index, similarity_score))

    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    return similarity_scores[:5]


