from enum import Enum


def actor_set_extractor(movie):
    movie_actors = set(movie['movielens_actors'])
    return movie_actors


def director_set_extractor(movie):
    movie_directors = set(movie['directors'])
    return movie_directors


def genre_set_extractor(movie):
    movie_genres = set(movie['movielens_genres'])
    return movie_genres


def keyword_set_extractor(movie):
    movie_keyword_ids = {item['id'] for item in movie['keywords']}
    return movie_keyword_ids


def writer_set_extractor(movie):
    movie_writers = set(movie['writers'])
    return movie_writers


class SetExtractor(Enum):
    ACTOR = 1
    DIRECTOR = 2
    GENRE = 3
    KEYWORD = 4
    WRITER = 5

    def extract(self, movie):
        if self == SetExtractor.ACTOR:
            return actor_set_extractor(movie)
        elif self == SetExtractor.DIRECTOR:
            return director_set_extractor(movie)
        elif self == SetExtractor.GENRE:
            return genre_set_extractor(movie)
        elif self == SetExtractor.KEYWORD:
            return keyword_set_extractor(movie)
        elif self == SetExtractor.WRITER:
            return writer_set_extractor(movie)


def intersection_cardinality(s1, s2):
    intersection = s1.intersection(s2)
    return len(intersection)


def jaccard_index(s1, s2):
    intersection = s1.intersection(s2)
    union = s1.union(s2)

    if len(union) > 0:
        return len(intersection) / len(union)

    return 0


def overlap_coefficient(s1, s2):
    intersection = s1.intersection(s2)
    min_card = min(len(s1), len(s2))

    if min_card > 0:
        return len(intersection) / min_card

    return 0


def dice_coefficient(s1, s2):
    intersection = s1.intersection(s2)
    card_sum = len(s1) + len(s2)

    if card_sum > 0:
        return (2 * len(intersection)) / card_sum

    return 0


def set_based_similarity(set_similarity_measure, set_extractor: SetExtractor):
    def func(other_movie, reference_movie):
        other_movie_feature_set = set_extractor.extract(other_movie)
        reference_movie_feature_set = set_extractor.extract(reference_movie)
        return set_similarity_measure(other_movie_feature_set, reference_movie_feature_set)

    return func
