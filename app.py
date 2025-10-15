from flask import Flask, request, jsonify, render_template
from recommendation_model import get_recommendations

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    try:
        recommendations = get_recommendations(title)
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)


# #######################################################################################################################
# 1) cd "C:\Users\taran\OneDrive\Documents\Projects\movie_recommender"
# 2) python app.py

# 3) Test Titles
#     harry potter and the prisoner of azkaban 
#     harry potter and the goblet of fire
#     bad boys
#     avatar
#     the godfather
#     gladiator
#     sherlock holmes
# #######################################################################################################################