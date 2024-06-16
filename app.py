from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
import pandas as pd
import os
import json

import constants
import loader
import recommender

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # No CORS policy for local development


@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '').lower()
    movie_metadata = loader.get_movies_metadata()
    if query:
        # Search for movies that contain the query string in their title
        results = movie_metadata[movie_metadata['title'].str.lower().str.contains(query, na=False)]
        results = results[['movieId', 'title']].rename(columns={'movieId': 'MovieID', 'title': 'Title'})
        results = results[['MovieID', 'Title']].to_dict(orient='records')
    else:
        results = []
    return jsonify(results)


@app.route('/recommend', methods=['GET'])
def recommend_movies():
    movie_id = request.args.get('movieID')
    list_number = request.args.get('listNr')
    print('recoms for id ' + movie_id)
    if list_number:
        print('list number ' + list_number)
        list_number = int(list_number)
    recommendations = recommender.get_recommendations(int(movie_id), list_number)
    # recommendations = recommender.get_random_recommendations()
    return jsonify(recommendations)


@app.route('/poster', methods=['GET'])
def get_image():
    movie_id = request.args.get('movieID', '').lower()
    # Assuming images are stored as {movie_id}.jpg
    image_path = os.path.join(constants.MOVIES_POSTER_JPG_DIR_PATH, f'{movie_id}.jpg')
    if os.path.exists(image_path):
        return send_from_directory(constants.MOVIES_POSTER_JPG_DIR_PATH, f'{movie_id}.jpg')
    else:
        abort(404, description="Poster not found")


@app.route('/details', methods=['GET'])
def get_details():
    movie_id = request.args.get('movieID', '').lower()
    # Assuming details are stored as {movie_id}.json
    details_path = os.path.join(constants.MOVIES_METADATA_JSON_DIR_PATH, f'{movie_id}.json')
    if os.path.exists(details_path):
        with open(details_path, 'r', encoding='utf-8') as details_file:
            details_data = json.load(details_file)
            return jsonify(details_data)
    else:
        abort(404, description="Details not found")


if __name__ == '__main__':
    app.run(debug=True)
