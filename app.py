from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

import collaborative_filtering

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # No CORS policy for local development

# Load the dataset
movies = pd.read_csv('movies_dataset/movies.dat', delimiter='::', header=None, engine='python',
                     names=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1')

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '').lower()
    if query:
        # Search for movies that contain the query string in their title
        results = movies[movies['Title'].str.lower().str.contains(query, na=False)]
        results = results[['MovieID', 'Title', 'Genres']].to_dict(orient='records')
    else:
        results = []
    return jsonify(results)

@app.route('/like', methods=['POST'])
def like_movie():
    data = request.json
    movie_id = data['movie_id']
    user_id = data['user_id']
    collaborative_filtering.like_movie(user_id, movie_id)
    return jsonify({'status': 'success'})

@app.route('/recommend', methods=['GET'])
def recommend_movies():
    user_id = request.args.get('user_id')
    recommendations = collaborative_filtering.get_recommendations(user_id)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
