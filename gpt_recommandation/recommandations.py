from groq import Groq
from loader import get_movies_metadata
import json


def fetch_api(reference_movie_df):
    prompt = "I need a recommendation of 10 movies that are similar to the given movie. Please provide the response in JSON format with each movie having a title and a similarity measure score. The JSON format should look like this: [{\"title\": \"MovieTitle1\", \"similarity_measure\": score1}, {\"title\": \"MovieTitle2\", \"similarity_measure\": score2}, ...]. Just give the json and no more inforamtion  The given movie is " + reference_movie_df

    API_KEY = "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"

    client = Groq(api_key=API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content


def get_similar_movies(reference_movie_id):
    
    movies_df = get_movies_metadata()

    reference_movie_df = movies_df.loc[movies_df['movieId'] == reference_movie_id]
    assert reference_movie_df.shape[0] == 1, "There are several movies with the same movie id"
    reference_movie = reference_movie_df.squeeze()

    similarity_scores = []
    rep = ""

    try:
        answer = fetch_api(reference_movie['title'])
        rep = json.loads(answer)
    except:
        print("error")
    
    for index in rep:
        try:
            title = index['title'].lower()
            search_results_df = movies_df[movies_df['title'].str.lower().str.contains(title, na=False)]
            if len(search_results_df) > 0:
                # Make sure only movies are recommended that are present in the movies_df
                movie_id = search_results_df.iloc[0]['movieId']
            else:
                print("There is no movie with the title in the dataframe.")
                continue

            similarity_scores.append((int(movie_id),index['similarity_measure']))
        except:
            pass

    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    return similarity_scores[:5]