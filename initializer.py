import json
import os
import constants

import numpy as np
import pandas as pd

from loader import get_movies_metadata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def initialize_description_rf_idf_cosine_sim():
    movie_metadata_df = get_movies_metadata()
    tfidf = TfidfVectorizer(stop_words='english')
    movie_metadata_df['description'] = movie_metadata_df['description'].fillna('')
    tfidf_matrix = tfidf.fit_transform(movie_metadata_df['description'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    np.save(constants.DESCRIPTION_COSINE_SIM_MATRIX_NPY_FILE_PATH, cosine_sim)


def initialize_title_tf_idf_cosine_sim():
    movie_metadata_df = get_movies_metadata()
    tfidf = TfidfVectorizer(stop_words='english')
    movie_metadata_df['title'] = movie_metadata_df['title'].fillna('')
    tfidf_matrix = tfidf.fit_transform(movie_metadata_df['title'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    np.save(constants.TITLE_COSINE_SIM_MATRIX_NPY_FILE_PATH, cosine_sim)


def parse_movie_json(json_data):
    """Extract necessary fields from a single movie JSON."""
    movielens_id = json_data.get('movielensId', None)

    # Extract keywords
    keywords = json_data.get('tmdb', {}).get('keywords', [])
    # keyword_ids = [kw['id'] for kw in keywords]

    # Extract directors
    directors = json_data.get('imdb', {}).get('directors', [])

    # Extract writers
    writers = json_data.get('imdb', {}).get('writers', [])

    # Extract movielens genres
    movielens_genres = json_data.get('movielens', {}).get('genres', [])

    # Extract tmdb genres
    tmdb_genres = json_data.get('tmdb', {}).get('genres', [])
    tmdb_genres_names = [genre['name'] for genre in tmdb_genres]

    # Extract imdb genres
    imdb_genres = json_data.get('imdb', {}).get('genres', [])

    # Extract actor ids
    # actors = json_data.get('tmdb', {}).get('credits', {}).get('cast', [])
    # first three actors are considered lead actors
    # actor_ids = [actor['id'] for actor in actors][:3]

    # Extract movielens actors
    movielens_actors = json_data.get('movielens', {}).get('actors', [])

    # Extract title
    title = json_data.get('movielens', {}).get('title', '')

    description = json_data.get('movielens', {}).get('plotSummary', '')

    return {
        'movieId': movielens_id,
        'title': title,
        'keywords': keywords,
        'directors': directors,
        'writers': writers,
        'movielens_genres': movielens_genres,
        'tmdb_genres': tmdb_genres_names,
        'imdb_genres': imdb_genres,
        'movielens_actors': movielens_actors,
        'description': description
    }


def construct_movie_metadata_dataframe_from_ids(directory_path, movie_ids):
    """Construct a DataFrame for movies in the movie_ids list for which there is a metadata
    JSON file in the given directory."""
    all_movies_data = []

    for filename in movie_ids:
        file_path = os.path.join(directory_path, str(filename) + '.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                movie_data = parse_movie_json(json_data)
                all_movies_data.append(movie_data)
        except FileNotFoundError:
            print(f"The file at {file_path} was not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file at {file_path}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    df = pd.DataFrame(all_movies_data)
    return df


def initialize_movie_metadata(movies_file_path, directory_path):
    movies_df = pd.read_csv(movies_file_path)
    print(movies_df.head())
    print(movies_df.shape)
    print(movies_df['movieId'].max())
    # only include movies that are listed in the movies.csv (from movielens ml-20m) AND for which there is a
    # json file containing necessary metadata
    movies_metadata_df = construct_movie_metadata_dataframe_from_ids(directory_path, movies_df['movieId'].tolist())
    print(movies_metadata_df.head())
    print(movies_metadata_df.shape)
    movies_metadata_df.to_parquet(constants.MOVIES_METADATA_PARQUET_FILE_PATH, index=False)


def initialize_item_user_matrix(ratings_file_path):
    ratings_df = pd.read_csv(ratings_file_path)
    ratings_df.drop(columns=['timestamp'], inplace=True)
    print(ratings_df.head())
    print(ratings_df.shape)
    item_user_matrix_df = pd.pivot_table(ratings_df, index='movieId', columns='userId', values='rating')
    print(item_user_matrix_df.head(10))
    print(item_user_matrix_df.shape)
    item_user_matrix_df.to_parquet(constants.ITEM_USER_MATRIX_PARQUET_FILE_PATH)


if __name__ == '__main__':
    # please make sure you have pyarrow and fastparquet installed - 'pip install pyarrow fastparquet'
    initialize_movie_metadata(constants.MOVIES_CSV_FILE_PATH, constants.MOVIES_METADATA_JSON_DIR_PATH)
    initialize_item_user_matrix(constants.RATINGS_CSV_FILE_PATH)
    initialize_title_tf_idf_cosine_sim()
    initialize_description_rf_idf_cosine_sim()
