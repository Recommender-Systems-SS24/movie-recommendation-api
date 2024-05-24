from flask import Flask, request, jsonify
import collaborative_filtering

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query')
    results = collaborative_filtering.search_movies(query)
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
