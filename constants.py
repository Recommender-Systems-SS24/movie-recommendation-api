# PLEASE ADJUST THE FOLLOWING 4 PATH CONSTANTS FOR YOUR LOCAL ENVIRONMENT!!!

# path to movies.csv from movielens ml-20m containing about 27k movies
# (or the movies.csv from ml-latest-small, containing about 9k movies)
MOVIES_CSV_FILE_PATH = '.\\resources\\movies_ratings\\movies.csv'
# path to ratings.csv from movielens ml-latest-small
RATINGS_CSV_FILE_PATH = '.\\resources\\movies_ratings\\ratings.csv'
# path to directory containing the json movie metadata files
MOVIES_METADATA_JSON_DIR_PATH = '.\\resources\\movies_details'
# path to directory containing the movie poster jpg files
MOVIES_POSTER_JPG_DIR_PATH = '.\\resources\\movies_posters'


# YOU DO NOT NEED TO CHANGE THE FOLLOWING 4 PATHS!!!

MOVIES_METADATA_PARQUET_FILE_PATH = '.\\resources\\output\\movies_metadata.parquet'
ITEM_USER_MATRIX_PARQUET_FILE_PATH = '.\\resources\\output\\item_user_matrix.parquet'
DESCRIPTION_COSINE_SIM_MATRIX_NPY_FILE_PATH = '.\\resources\\output\\description_cosine_sim_matrix.npy'
TITLE_COSINE_SIM_MATRIX_NPY_FILE_PATH = '.\\resources\\output\\title_cosine_sim_matrix.npy'
