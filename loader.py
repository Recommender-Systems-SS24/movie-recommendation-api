import numpy as np
import pandas as pd

import constants

_movies_metadata_df = None
_item_user_matrix_df = None
_description_cosine_sim_matrix = None
_title_cosine_sim_matrix = None


def get_movies_metadata():
    if _movies_metadata_df is None:
        read_movies_metadata_file()
    return _movies_metadata_df


def get_item_user_matrix():
    if _item_user_matrix_df is None:
        read_item_user_matrix_file()
    return _item_user_matrix_df


def get_description_cosine_sim_matrix():
    if _description_cosine_sim_matrix is None:
        read_description_cosine_sim_matrix()
    return _description_cosine_sim_matrix


def get_title_cosine_sim_matrix():
    if _title_cosine_sim_matrix is None:
        read_title_cosine_sim_matrix()
    return _title_cosine_sim_matrix


def read_movies_metadata_file():
    global _movies_metadata_df
    _movies_metadata_df = pd.read_parquet(constants.MOVIES_METADATA_PARQUET_FILE_PATH)
    print(_movies_metadata_df.head())
    print(_movies_metadata_df.shape)


def read_item_user_matrix_file():
    global _item_user_matrix_df
    _item_user_matrix_df = pd.read_parquet(constants.ITEM_USER_MATRIX_PARQUET_FILE_PATH)
    print(_item_user_matrix_df.head())
    print(_item_user_matrix_df.shape)


def read_description_cosine_sim_matrix():
    global _description_cosine_sim_matrix
    _description_cosine_sim_matrix = np.load(constants.DESCRIPTION_COSINE_SIM_MATRIX_NPY_FILE_PATH)


def read_title_cosine_sim_matrix():
    global _title_cosine_sim_matrix
    _title_cosine_sim_matrix = np.load(constants.TITLE_COSINE_SIM_MATRIX_NPY_FILE_PATH)
