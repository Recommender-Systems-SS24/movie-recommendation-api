import time
import recommender


def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time of {func.__name__}: {execution_time:.4f} seconds")
    return result


if __name__ == '__main__':
    movie_id = 42
    rec_list_1 = measure_execution_time(recommender.get_recommendation_list_1, movie_id)
    print(rec_list_1)
    rec_list_2 = measure_execution_time(recommender.get_recommendation_list_2, movie_id)
    print(rec_list_2)
    rec_list_3 = measure_execution_time(recommender.get_recommendation_list_3, movie_id)
    print(rec_list_3)
    rec_list_4 = measure_execution_time(recommender.get_recommendation_list_4, movie_id)
    print(rec_list_4)
    rec_list_5 = measure_execution_time(recommender.get_recommendation_list_5, movie_id)
    print(rec_list_5)

