def pearson_correlation(item_1, item_2):
    common_users = item_1.dropna().index.intersection(item_2.dropna().index)
    item1_ratings = item_1[common_users]
    item2_ratings = item_2[common_users]

    # a minimum of 3 common users is required
    if len(common_users) < 3:
        return 0

    mean_1 = sum(item1_ratings) / len(item1_ratings)
    mean_2 = sum(item2_ratings) / len(item2_ratings)
    numerator = sum((r_1 - mean_1) * (r_2 - mean_2) for r_1, r_2 in zip(item1_ratings, item2_ratings))
    sum_sq_1 = sum((r_1 - mean_1) ** 2 for r_1 in item1_ratings)
    sum_sq_2 = sum((r_2 - mean_2) ** 2 for r_2 in item2_ratings)
    denominator = (sum_sq_1 * sum_sq_2) ** 0.5

    if denominator == 0:
        return 0
    else:
        return numerator / denominator
